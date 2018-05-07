#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" This module runs the frontend app of iteratec's Observerhive.

    The app implements a simple webservice where the user can either register
    projects at a Conductor Service, check his or her registrations or turn
    on and off receiving event messages for the registered projects.
"""

import os
from flask import Flask, redirect, render_template, request, \
    url_for, Response, g, session
import flask_login
from bcrypt import hashpw, gensalt
from .models import User, Anonymous
from src.user_configs.configloader import load_config, save_config
from .loggers import setup_flask_logging, setup_gunicorn_log
import json
from threading import Thread

# from lights.led_blinker import Blink


__author__ = "Masud Afschar"
__status__ = "Development"

# create the application instance
app = Flask(__name__)
# set configurations of this app
app.config.from_object("src.config.ProductionConfig")

# check how app is run and set logging appropriately
if "SERVER_SOFTWARE" in os.environ:
    if "gunicorn" in os.environ["SERVER_SOFTWARE"]:
        logger = setup_gunicorn_log(app)
else:
    LOG_LEVEL = "INFO"
    logger = setup_flask_logging(LOG_LEVEL)

# configure login manager
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
# redirect to login page if user is not authenticated
login_manager.login_view = "login"
# produce an anonymous user to use when no one is logged in
login_manager.anonymous_user = Anonymous


def get_users():
    """Opens the users file containing all usernames and passwords.

       Provides the dictionary with usernames and corresponding passwords
       of all users for the current application context.
    """

    if 'users' not in g:
        cwd = os.path.dirname(os.path.abspath(__file__))
        with open(cwd + '/users.json') as registered_users:
            users = json.load(registered_users)
        g.users = users
    return g.users


def add_user_and_password(username, password):
    users = get_users()
    users[username] = hashpw(password.encode('utf-8'),
                             gensalt()).decode('utf-8')
    cwd = os.path.dirname(os.path.abspath(__file__))
    with open(cwd + "/users.json", "w") as outfile:
        json.dump(users, outfile, sort_keys=True, indent=4)


@app.teardown_appcontext
def close_userfile(error):
    """Closes the users file at the end of a request.
    """

    if 'users' in g:
        g.pop('users', None)


@login_manager.user_loader
def user_loader(username):
    """Callback function for reloading a user from the session.

        The function takes the username and returns a user object
        or None if the user does not exist.
    """

    users = get_users()
    if username not in users:
        return

    user = User()
    user.id = username
    return user


@login_manager.request_loader
def request_loader(request):
    """Callback function for reloading a user from the session.

        The function takes the Flask request and returns a user object
        or None if the user does not exist.
    """

    if 'username' in session:
        user = User()
        user.id = session['username']
        return user
    return


@app.route('/', methods=['GET', 'POST'])
def home():
    """Renders the homepage template.
    """

    if not flask_login.current_user.is_authenticated:
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
        usrname = request.form['username']
        user = User()
        user.id = usrname
        session['username'] = usrname
        flask_login.login_user(user)
        logger.info(usrname + ' successfully logged in.')
        response = redirect(request.args.get("next") or url_for("home"))
        return response
    else:
        return render_template('login.html', form=form)


@app.route('/logout/', methods=['GET', 'POST'])
@flask_login.login_required
def logout():
    """Log the current user out.

       Calls the logout_user() function of flask_login and
       redirects to the homepage of this app.
    """

    # remove the username from the session if it is there
    out_user = flask_login.current_user.id
    flask_login.logout_user()
    session.pop('registrations', None)
    session.pop('username', None)
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
        add_user_and_password(username, password)

        return redirect(url_for('home'))
    else:
        return render_template('signup.html', form=form)


@app.route('/check-usernames/', methods=['POST'])
def check_username():
    """Check if POSTed username does already exist.

    :return: true if username already in use
    """

    users = get_users()
    username = request.data.decode('utf-8')

    if username in users:
        return Response('true')
    else:
        return Response('false')


@app.route('/profile/', methods=['GET', 'POST'])
@flask_login.login_required
def show_registrations():
    """Retrieve all registered projects of the current user and show them.

       The function retrieves the current users stored configurations and
       passes them to the corresponding template.
    """

    username = flask_login.current_user.id
    registrations = load_config(username)
    return render_template("show_entries.html", registrations=registrations,
                           username=username)


@app.route('/profile/registration/', methods=['POST'])
@flask_login.login_required
def register_remaining():
    """Register all projects at Conductor service if not done already.

       The function checks all projects in the users config file and if
       a project does not have an id already it will try register it
       at the specified Conductor Service.
    """

    logger.info(request.form)
    return Response('Cool')
    #
    # username = flask_login.current_user.id
    # userconfigs = load_config(username)
    # registrations = {}
    # change_count = 0
    #
    # if 'registrations' not in session:
    #     for service, projects in userconfigs.items():
    #         requester = registrator.MyHTTPRequester(port='5000')
    #         for projectname, entries in projects.items():
    #             url = entries['projectUrl']
    #             events = entries['events']
    #             for event in events:
    #                 new_id = requester.register(event_type=event,
    #                                             project=projectname,
    #                                             projectUrl=url,
    #                                             service_address=service)
    #                 if new_id is not None:
    #                     registrations[new_id] = {projectname: event}
    #                     logger.info('Added new id for registration.')
    #                     change_count += 1
    #     if change_count > 0:
    #         session['registrations'] = registrations
    #         logger.info('Made ' + str(change_count) + ' registration(s) for user '
    #                     + username + '.')
    #         return Response('Registrations were successful.')
    #     else:
    #         logger.info('Made no registrations for user '
    #                     + username + '.')
    #         return Response('Could not register any projects.')
    # return Response('Already registered.')


@app.route('/profile/activate/', methods=['POST'])
@flask_login.login_required
def activate_user_setup():
    """Set the active flag to True.

       The active flag indicates if a user is currently interested in
       receiving events for the project he has registered for.
    """

    flask_login.current_user.active = True
    logger.info('Activated messages for user '
                + flask_login.current_user.id + '.')
    return Response('200')


@app.route('/profile/deactivate/', methods=['POST'])
@flask_login.login_required
def deactivate_user_setup():
    """Set the active flag to False.

       The active flag indicates if a user is currently interested in
       receiving events for the project he has registered for.
    """

    flask_login.current_user.active = False
    logger.info('Deactivated messages for user '
                + flask_login.current_user.id + '.')
    return Response('200')


@app.route('/profile/edit/', methods=['GET', 'POST'])
@flask_login.login_required
def edit_registrations():
    """Retrieve all registered projects of the current user and show them.

       The function retrieves the current users stored configurations and
       passes them to the corresponding template so that the user can
       manipulate them if wished.
    """

    username = flask_login.current_user.id
    if request.method == 'GET':
        registrations = load_config(username)
        return render_template("edit_registration.html",
                               registrations=registrations,
                               username=username)
    else:
        data = {}
        for i, entries in enumerate(zip(request.form.getlist('service'),
                                        request.form.getlist('projectName'),
                                        request.form.getlist('repository'),
                                        request.form.getlist('eventType'))):

            if entries[0] not in data:
                data[entries[0]] = {entries[1]: {"projectUrl": entries[2], "events": [entries[3]]}}
            elif entries[1] not in data[entries[0]]:
                data[entries[0]][entries[1]] = {"projectUrl": entries[2], "events": [entries[3]]}
            else:
                data[entries[0]][entries[1]]["events"].append(entries[3])

        save_config(username, data)
        return redirect('/profile/')


@app.route('/change-password/', methods=['GET', 'POST'])
@flask_login.login_required
def change_password():
    """Render the form to change password of current user.

       The function retrieves the form to change one's password and
       renders it. If the current user submitted the form, the function
       hashes the password and stores it in the users file of the app.
    """

    from .forms import ChangePasswordForm

    username = flask_login.current_user.id
    form = ChangePasswordForm(request.form)
    if form.validate_on_submit():
        add_user_and_password(username, request.form['newPassword1'])
        logger.info("Successfully changed password of "
                    + username + '.')
        return redirect(url_for('home'))
    else:
        return render_template('change_password.html',
                               form=form,
                               username=username)


@app.route('/event/', methods=['POST'])
def render_event():
    """Catch POSTed data and process it.

       The function checks what kind of information was sent and
       forwards it to the lights class to process it.
    """

    logger.info('Received the following: '
                + str(request.data.decode('utf-8')))
    if flask_login.current_user.active == True:
        # blink_thread = Thread(target=Blink, kwargs={'numTimes': 10,'speed': 0.5})
        # blink_thread.start()
        pass
    return Response('Received POSTed event.')
