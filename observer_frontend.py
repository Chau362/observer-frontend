
from flask import Flask, redirect, render_template, request, url_for, flash, Response
import flask_login
import http_request_maker as registrator
from forms import LoginForm
from bcrypt import hashpw, gensalt, checkpw
import logging
import json
import os
from threading import Thread
#from led_blinker import Blink

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

with open("users.json") as user_data:
    users = json.load(user_data)

class User(flask_login.UserMixin):
    pass


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
    logger.info('Someone did visit homepage.')
    if not flask_login.current_user.is_authenticated:
        return render_template('home.html')
    else:
        return render_template('logged_in.html', username= flask_login.current_user.id)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    with open("users.json") as registered_users:
        users = json.load(registered_users)
    if request.method == 'POST' and form.validate_on_submit():
        usrname = request.form['username']
        password = request.form['password']
        if usrname in users:
            if checkpw(password.encode('utf-8'),
                      users[usrname].encode('utf-8')):
                user = User()
                user.id = usrname
                flask_login.login_user(user)
                return redirect(request.args.get("next") or url_for("home"))
            else:
                return redirect('/login/')
        else:
            return redirect('/login/')
    else:
        return render_template('login.html', form=form)


@app.route('/logout/', methods=['GET', 'POST'])
@flask_login.login_required
def logout():
    # remove the username from the session if it is there
    flask_login.logout_user()
    flash('You have been logged out.')
    return redirect(url_for('home'))


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        return redirect(url_for('home'))
    else:
        return render_template('signup.html')


@app.route('/profile/', methods=['GET', 'POST'])
@flask_login.login_required
def show_registrations():
    with open("config.json") as configs:
        registrations = json.load(configs)
    projects = []
    if flask_login.current_user.id in registrations:
        projects.append(registrations[flask_login.current_user.id])
    return render_template("show_entries.html", projects=projects)


@app.route('/profile/activate/', methods=['POST'])
def activate_user():
    with open("config.json") as configs:
        registrations = json.load(configs)
    projects = registrations[flask_login.current_user.id]
    for service_address in projects:
        requester = registrator.MyHTTPRequester(service_address=service_address)
        for project_name, entries in projects[service_address].items():
            for url, event in entries.items():
                requester.register(event, project_name)
    return Response('Hello hello!')


@app.route('/profile/receive/', methods=['POST'])
def receive_status():
    print(request.data)
    return Response('Received initial status.')


@app.route('/profile/edit/', methods=['GET', 'POST'])
@flask_login.login_required
def edit_registrations():
    with open("config.json") as configs:
        registrations = json.load(configs)
    projects = []
    if flask_login.current_user.id in registrations:
        projects.append(registrations[flask_login.current_user.id])
    return render_template("edit_registration.html", projects=projects)


@app.route('/change-password/', methods=['GET', 'POST'])
@flask_login.login_required
def change_password():
    with open("users.json") as registered_users:
        users = json.load(registered_users)
    current_password = users[flask_login.current_user.id]
    if request.method == "POST":
        if checkpw(request.form['currentPassword'].encode('utf-8'),
                  current_password.encode('utf-8')):
            if request.form['newPassword1'] == request.form['newPassword2']:
                users[flask_login.current_user.id] = hashpw(request.form['newPassword1'].encode('utf-8'), gensalt()).decode('utf-8')
                with open("/user_configs/users.json", "w") as outfile:
                    json.dump(users, outfile)
                flash("You successfully changed your Password!")
                return redirect(url_for('home'))
        flash("Unable to change Password. Please try again.")
        return render_template(url_for('change_password'))
    else:
        return render_template('change_password.html')


# @login_manager.unauthorized_handler
# def unauthorized_handler():
#     return 'Unauthorized'

# @template_rendered.connect()
# def when_template_rendered(sender, template, context, **extra):
#     print('Template %s is rendered with %s' % (template.name, context))


@app.route('/event/', methods=['POST'])
def render_event():
    # blink_thread = Thread(target=Blink, kwargs={'numTimes': 3,'speed': 1})
    # blink_thread.start()
    return Response('Received POSTed event.')


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='0.0.0.0', port=5000)
