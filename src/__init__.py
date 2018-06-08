#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" This module runs the frontend app of iteratec's Observerhive.

    The app implements a simple webservice where the user can either register
    projects at a Conductor Service, check his or her registrations or turn
    on and off receiving event messages for the registered projects.
"""

import os
import socket
import json
import requests
# import signal
# from multiprocessing import Process
from flask import redirect, render_template, request, \
    url_for, Response, session
from flask_login import LoginManager, current_user, login_required, \
    login_user, logout_user
from src.myflask import FlaskApp
from src.models import User, Anonymous, Registration, RegistrationSerializer, \
    Project
from src.loggers import setup_flask_logging, setup_gunicorn_logging

__author__ = "Masud Afschar"
__status__ = "Development"

# create the application instance
app = FlaskApp(__name__)
# set configurations of this app
app.config.from_object("src.config.ProductionConfig")

# check how app is run and set logging appropriately
if "SERVER_SOFTWARE" in os.environ:
    if "gunicorn" in os.environ["SERVER_SOFTWARE"]:
        logger = setup_gunicorn_logging(app)
else:
    LOG_LEVEL = "INFO"
    logger = setup_flask_logging(LOG_LEVEL)

# configure login manager
login_manager = LoginManager()
login_manager.init_app(app)
# redirect to login page if user is not authenticated
login_manager.login_view = "login"
# produce an anonymous user to use when no one is logged in
login_manager.anonymous_user = Anonymous


def split_registrations(list_of_registrations):
    list_of_registrations.sort(key=lambda registration: registration.service)

    sub_list = []
    main_list = []
    previous = list_of_registrations[0]

    for registration in list_of_registrations:
        if previous.service == registration.service:
            sub_list.append(registration)
        else:
            main_list.append(sub_list)
            sub_list = [registration]
        previous = registration

    main_list.append(sub_list)
    return main_list


@login_manager.user_loader
def user_loader(username):
    """Callback function for reloading a user from the session.

        The function takes the username and returns a user object
        or None if the user does not exist.
    """

    users = app.users
    if username not in users:
        return

    user = User()
    user.id = username
    user.registrations = app.load_config(username)
    return user


@login_manager.request_loader
def request_loader(request):
    """Callback function for reloading a user from a Flask request.

        The function takes the Flask request and returns a user object
        or None if the user does not exist.
    """

    if 'user_id' in session:
        logger.info(session['user_id'])
        user = User()
        user.id = session['user_id']
        user.registrations = app.load_config(user.id)
        return user
    return


@app.route('/', methods=['GET', 'POST'])
def home():
    """Renders the homepage template.
    """

    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    else:
        return redirect(url_for('show_registrations'))


@app.route('/login/', methods=['GET', 'POST'])
def login():
    """Render the login page and check login credentials.

       The function renders the login form and checks if username
       does exist and the provided password is correct when the user
       submits his or her data.
    """

    from .forms import LoginForm

    form = LoginForm(request.form)
    if form.validate_on_submit():
        username = request.form['username']
        user = User()
        user.id = username
        login_user(user, remember=True)
        logger.info(username + ' successfully logged in.')
        response = redirect(request.args.get("next") or url_for("home"))
        return response
    else:
        return render_template('login.html', form=form)


@app.route('/logout/', methods=['GET', 'POST'])
@login_required
def logout():
    """Log the current user out.

       Calls the logout_user() function of flask_login and
       redirects to the homepage of this app.
    """

    # remove the username from the session if it is there
    out_user = current_user.get_id()
    logout_user()
    logger.info(out_user + ' has been logged out.')
    return redirect(url_for('home'))


@app.route('/register/', methods=['GET', 'POST'])
def register():
    """Render the form to register a new user.

       The function renders the registration form and stores its values
       if the current user submitted the form.
    """

    from .forms import RegisterForm

    form = RegisterForm(request.form)

    if form.validate_on_submit():
        username = request.form['username']
        password = request.form['password1']
        app.add_user_and_password(username, password)
        logger.info('Created account for ' + username + '.')

        if "rememberMe" in request.form:
            user = User()
            user.id = username
            session['username'] = username
            session['registrations'] = []
            login_user(user, remember=True)
            logger.info('Logged ' + username + ' in after account creation.')

        return redirect(url_for('home'))

    return render_template('signup.html', form=form)


@app.route('/check-usernames/', methods=['POST'])
def check_username():
    """Check if POSTed username does already exist.

    :return: true if username already in use
    """

    users = app.users
    username = request.data.decode('utf-8')

    if username in users:
        return Response('true')
    else:
        return Response('false')


@app.route('/profile/', methods=['GET', 'POST'])
@login_required
def show_registrations():
    """Retrieve all registered projects of the current user and show them.

       The function retrieves the current users stored configurations and
       passes them to the corresponding template.
    """

    username = current_user.get_id()
    registrations = current_user.registrations
    if registrations:
        registrations = split_registrations(registrations)
    return render_template("show_entries.html", registrations=registrations,
                           username=username, active=(username in app.active_users))


@app.route('/profile/add-follow/', methods=['POST'])
@login_required
def register_project():
    """Register a project at Conductor service if not done already.

       The function checks all projects in the users config file and if
       a project does not have an id already it will try register it
       at the specified Conductor Service.
    """

    registration_id = request.json["id"]
    service = request.json["service"]
    project_name = request.json["project_name"]
    project_url = request.json["project_url"]
    event = request.json["event"]

    if registration_id is None:
        return Response('Received empty value for ID of registration.')
    if service is None:
        return Response('Received empty value for service.')
    if project_name is None:
        return Response('Received empty value for project name.')
    if project_url is None:
        return Response('Received empty value for project url.')
    if event is None:
        return Response('Received empty value for event.')

    new_follower = Registration(registration_id=registration_id,
                                service=service, project_name=project_name,
                                project_url=project_url, event=event,
                                active=True)

    registrations = current_user.registrations
    registrations.remove(new_follower)
    registrations.append(new_follower)

    registrations = list(map(RegistrationSerializer.deserialize_registration,
                             registrations))

    app.save_config(current_user.id, registrations)

    return Response('Saved registration.')


@app.route('/profile/remove-follow/', methods=['POST'])
@login_required
def deregister_project():
    """Deregister a project at Conductor service if not done already.

       The function checks all projects in the users config file and if
       a project does not have an id already it will try register it
       at the specified Conductor Service.
    """

    registration_id = request.json["id"]
    service = request.json["service"]
    project_name = request.json["project_name"]
    project_url = request.json["project_url"]
    event = request.json["event"]

    if registration_id is None:
        return Response('Received empty value for ID of registration.')
    if service is None:
        return Response('Received empty value for service.')
    if project_name is None:
        return Response('Received empty value for project name.')
    if project_url is None:
        return Response('Received empty value for project url.')
    if event is None:
        return Response('Received empty value for event.')

    new_follower = Registration(registration_id=registration_id,
                                service=service, project_name=project_name,
                                project_url=project_url, event=event,
                                active=False)

    registrations = current_user.registrations
    registrations.remove(new_follower)
    registrations.append(new_follower)

    registrations = list(map(RegistrationSerializer.deserialize_registration,
                             registrations))

    app.save_config(current_user.id, registrations)

    return Response('Removed registration.')


@app.route('/profile/activate/', methods=['POST'])
@login_required
def activate_user_setup():
    """Set the active flag to True.

       The active flag indicates if a user is currently interested in
       receiving events for the project he has registered for.
    """

    projects_list = app.load_config(current_user.get_id())
    active_projects_set = set()
    for project in projects_list:
        if project['_active']:
            active_project = Project(project['project_url'], project['event'], project)
            active_projects_set.add(active_project)
    app.active_users[current_user.get_id()] = active_projects_set
    logger.info('Activated messages for user '
                + current_user.get_id() + '.')
    return Response('200')


@app.route('/profile/deactivate/', methods=['POST'])
@login_required
def deactivate_user_setup():
    """Set the active flag to False.

       The active flag indicates if a user is currently interested in
       receiving events for the project he has registered for.
    """

    app.active_users.pop(current_user.get_id(), None)
    logger.info('Deactivated messages for user '
                + current_user.get_id() + '.')
    return Response('200')


@app.route('/profile/edit/', methods=['GET', 'POST'])
@login_required
def edit_registrations():
    """Retrieve all registered projects of the current user and show them.

       The function retrieves the current users stored configurations and
       passes them to the corresponding template so that the user can
       manipulate them if wished.
    """

    username = current_user.get_id()
    if request.method == 'GET':
        registrations = current_user.registrations
        if registrations:
            registrations = split_registrations(current_user.registrations)
        return render_template("edit_registration.html",
                               registrations=registrations,
                               username=username)
    else:
        attributes = ['id', 'service', 'projectName',
                      'repository', 'eventType', 'active']

        for attribute in attributes:
            if not request.form.getlist(attribute):
                return Response('Received missing attribute '
                                + attribute + '.')

        new_registrations = []
        for i, entries in enumerate(zip(request.form.getlist('id'),
                                        request.form.getlist('service'),
                                        request.form.getlist('projectName'),
                                        request.form.getlist('repository'),
                                        request.form.getlist('eventType'),
                                        request.form.getlist('active'))):
            entries = list(entries)
            if entries[0] == "None":
                callback_address = "http://" + socket.gethostname() + ":9090"
                data = {"projectUrl": entries[3],
                        "eventType": entries[4],
                        "project": entries[2],
                        "callback": callback_address}
                response = requests.post(entries[1], json=data)
                entries[0] = response.text

            new_registration = Registration(registration_id=entries[0],
                                            service=entries[1],
                                            project_name=entries[2],
                                            project_url=entries[3],
                                            event=entries[4],
                                            active=entries[5])
            print(entries[5])
            new_registrations.append(new_registration)

        new_registrations = list(map(RegistrationSerializer.deserialize_registration,
                                     new_registrations))

        app.save_config(username, new_registrations)
        return redirect('/profile/')


@app.route('/profile/delete/', methods=['POST'])
@login_required
def delete_account():
    """Delete the account of the given user.

    :return: HTTP response 302 and redirect to home endpoint.
    """
    username = current_user.get_id()
    app.delete_user(username)
    logger.info('Deleted account of user ' + username + '.')
    logout_user()
    logger.info('Logged ' + username + ' out after account deletion.')
    return Response('Account successfully deleted.')


@app.route('/change-credentials/', methods=['GET', 'POST'])
@login_required
def change_password():
    """Render the form to change password of current user.

       The function retrieves the form to change one's password and
       renders it. If the current user submitted the form, the function
       hashes the password and stores it in the users file of the app.
    """

    from .forms import ChangeCredentialsForm

    username = current_user.get_id()
    form = ChangeCredentialsForm(request.form)

    if form.validate_on_submit():
        logger.info(username + " wants to change something.")
        if request.form['username'] != username:
            logger.info("User " + username + " wants to change the username.")
            app.rename_user(username, request.form['username'],
                            request.form['newPassword1'])
        else:
            logger.info("Changing password of user " + username + ".")
            app.add_user_and_password(request.form['username'],
                                      request.form['newPassword1'])

        logger.info("Successfully changed credentials of "
                    + username + '.')
        return redirect(url_for('home'))

    else:
        return render_template('change-credentials.html',
                               form=form,
                               username=username)


@app.route('/event/', methods=['POST'])
def render_event():
    """Catch POSTed data and process it.

       The function checks what kind of information was sent and
       forwards it to the notify class to process it.
    """
    event = request.json
    if event is None:
        return Response('Received empty POST.')
    logger.info('Received a ' + event['eventType'] + ' to show.')

    # for pid in app.active_processes:
    # os.kill(pid, signal.SIGKILL)
    # app.active_processes.remove(pid)

    # event_process = Process(target=handle_event,
    #                         kwargs={'type': event['eventType'],
    #                                 'active_users': app.active_users})
    # event_process.start()

    # app.active_processes.append(event_process.pid)

    return Response('Received POSTed event.')


@app.route('/active-users/', methods=['GET'])
def return_active_users():
    return Response(json.dumps(app.active_users))


if __name__ == '__main__':
    app.run()
