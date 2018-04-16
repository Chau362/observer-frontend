#!/usr/bin/env python3
# # -*- coding: utf-8 -*-

""" This module runs the frontend of iteratec's Observerhive.

    Blabblabla
"""

from flask import Flask, redirect, render_template, request, url_for, Response
import flask_login
from . import request_maker as registrator
from observer_frontend.forms import LoginForm, ChangePasswordForm, RegisterForm
from bcrypt import hashpw, gensalt, checkpw
import logging
import json
import os
from observer_frontend.user_configs.configloader import load_config, save_config
from threading import Thread
# from lights.led_blinker import Blink

app = Flask(__name__)

app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key"
))

# logging setup
logger = logging.getLogger(__name__)
logger.setLevel('INFO')
logger_file_handler = logging.FileHandler('info.log')
logger_file_handler.setLevel('INFO')
logger_file_handler.setFormatter(
    logging.Formatter("%(asctime)s - [%(levelname)s] - %(name)s: %(message)s",
                      datefmt='%Y-%m-%d %H:%M:%S'))
console_log = logging.StreamHandler()
console_log.setLevel('INFO')
console_log.setFormatter(
    logging.Formatter("%(asctime)s - [%(levelname)s] - %(name)s: %(message)s",
                      datefmt='%Y-%m-%d %H:%M:%S'))
logger.addHandler(logger_file_handler)
logger.addHandler(console_log)


# configure login manager
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

with open("observer_frontend/users.json") as user_data:
    users = json.load(user_data)

class User(flask_login.UserMixin):

    def __init__(self):
        self.active = False



@login_manager.user_loader
def user_loader(username):
    if username not in users:
        return

    user = User()
    user.id = username
    return user


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    if username not in users:
        return

    user = User()
    user.id = username

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form['password'] == users[username]

    return user

@app.route('/')
def home():
    if not flask_login.current_user.is_authenticated:
        return render_template('home.html')
    else:
        return render_template('logged_in.html', username= flask_login.current_user.id)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    with open("observer_frontend/users.json") as registered_users:
        users = json.load(registered_users)
    if form.validate_on_submit():
        usrname = request.form['username']
        password = request.form['password']
        if usrname in users:
            if checkpw(password.encode('utf-8'),
                      users[usrname].encode('utf-8')):
                user = User()
                user.id = usrname
                flask_login.login_user(user)
                logger.info(usrname + ' successfully logged in.')
                return redirect(request.args.get("next") or url_for("home"))
            else:
                logger.info('Denied access to ' + usrname + ' due to wrong password.')
                return redirect('/login/')
        else:
            logger.info(usrname + ' unknown.')
            return redirect('/login/')
    else:
        return render_template('login.html', form=form)


@app.route('/logout/', methods=['GET', 'POST'])
@flask_login.login_required
def logout():
    # remove the username from the session if it is there
    out_user = flask_login.current_user.id
    flask_login.logout_user()
    logger.info(out_user + ' has been logged out.')
    return redirect(url_for('home'))


@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST':
        data = {}
        projects = {}
        for project_name, repository, event in zip(request.form.getlist('projectName'),
                                               request.form.getlist('repository'),
                                               request.form.getlist('eventType')):
            projects[project_name] = {repository: {event: "None"}}
            print(request.form.getlist('projectName'), request.form.getlist('repository'), request.form.getlist('eventType'))
        data[request.form['service']] = projects
        try:
            save_config(request.form.get('username'), data)
        except:
            logger.error('Shit happened while saving user configs.')

        return redirect(url_for('home'))
    else:
        return render_template('signup.html', form=form)


@app.route('/profile/', methods=['GET', 'POST'])
@flask_login.login_required
def show_registrations():
    projects = load_config(flask_login.current_user.id)
    return render_template("show_entries.html", projects=projects)


@app.route('/profile/register/', methods=['POST'])
def register_remaining():
    projects = load_config(flask_login.current_user.id)
    change_count = 0
    for service_address in projects:
        requester = registrator.MyHTTPRequester(port='5000')
        for project_name, entries in projects[service_address].items():
            for url, events in entries.items():
                for event, id in events.items():
                    if id == "None":
                        new_id = requester.register(event_type=event,
                                                    project=project_name,
                                                    projectUrl=url,
                                                    service_address=service_address)
                        if new_id is not None:
                            projects[service_address][project_name][url][event] = new_id
                            logger.info('Added new id for registration.')
                            change_count += 1
                    else:
                        pass
    if change_count > 0:
        save_config(flask_login.current_user.id, projects)
        logger.info('Made ' + str(change_count) + 'changes for user ' + flask_login.current_user.id + '.')
    else:
        logger.info('Made no changes for user ' + flask_login.current_user.id + '.')
    return Response('200')


@app.route('/profile/activate/', methods=['POST'])
def activate_user_setup():
    flask_login.current_user.active = True
    logger.info('Activated messages for user ' + flask_login.current_user.id + '.')
    return Response('200')


@app.route('/profile/deactivate/', methods=['POST'])
def deactivate_user_setup():
    flask_login.current_user.active = False
    logger.info('Deactivated messages for user ' + flask_login.current_user.id + '.')
    return Response('200')


@app.route('/profile/edit/', methods=['GET', 'POST'])
@flask_login.login_required
def edit_registrations():
    projects = load_config(flask_login.current_user.id)
    return render_template("edit_registration.html", projects=projects)


@app.route('/change-password/', methods=['GET', 'POST'])
@flask_login.login_required
def change_password():
    with open("observer_frontend/users.json") as registered_users:
        users = json.load(registered_users)
    current_password = users[flask_login.current_user.id]
    form = ChangePasswordForm(request.form)
    if form.validate_on_submit():
        if checkpw(request.form['currentPassword'].encode('utf-8'),
                  current_password.encode('utf-8')):
            if request.form['newPassword1'] == request.form['newPassword2']:
                users[flask_login.current_user.id] = hashpw(request.form['newPassword1'].encode('utf-8'), gensalt()).decode('utf-8')
                with open("users.json", "w") as outfile:
                    json.dump(users, outfile)
                logger.info("Successfully changed password of " + flask_login.current_user.id + '.')
                return redirect(url_for('home'))
        logger.info("Unable to change password of " + flask_login.current_user.id + '.')
        return redirect(url_for('change_password'))
    else:
        return render_template('change_password.html', form=form)


@app.route('/event/', methods=['POST'])
def render_event():
    logger.info('Received the following: ' + str(request.data.decode('utf-8')))
    if flask_login.current_user.active == True:
    # blink_thread = Thread(target=Blink, kwargs={'numTimes': 10,'speed': 0.5})
    # blink_thread.start()
        pass
    return Response('Received POSTed event.')


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='0.0.0.0', port=5000)
