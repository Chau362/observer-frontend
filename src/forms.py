"""This module contains all forms used by the Observer-Hive frontend.
"""

import os
import json
import logging
from bcrypt import checkpw
from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, EqualTo, Length

logger = logging.getLogger('src')


def get_users():
    """Retrieve all users and their passwords.

    :return: dictionary with all users and passwords
    """

    cwd = os.path.dirname(os.path.abspath(__file__))
    with open(cwd + '/users.json') as registered_users:
        users = json.load(registered_users)
    return users


class LoginForm(FlaskForm):
    """This class defines the login form.

     The form provides two entry fields for the user's
     credentials: username and password.
    """

    username = StringField('username',
                           validators=[InputRequired(
                               message="Please enter a Username.")])
    password = PasswordField('password',
                             validators=[InputRequired(
                                 message="Please enter your Password.")])

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)

    def validate(self):
        """Custom validator for the login form.

        Checks if username is known to the app and compares the
        entered password to the  stored one.

        :return: True if all checks have been passed
        """

        rv = FlaskForm.validate(self)
        if not rv:
            return False

        users = get_users()

        username = self.username.data
        if username not in users:
            self.username.errors.append('Unknown username')
            logger.info(username + ' unknown.')
            return False

        if not checkpw(self.password.data.encode('utf-8'),
                       users[username].encode('utf-8')):
            self.password.errors.append('Invalid password')
            logger.info('Denied access to '
                        + username
                        + ' due to wrong password.')
            return False

        return True


class ChangeCredentialsForm(FlaskForm):
    """This class defines the form to change an existing users password.

     The form provides one entry fields for the current password and two
     entry fields for new password, the second one being used for verification.
    """

    username = StringField('username',
                           validators=[InputRequired(
                               message="Please enter a Username.")])

    currentPassword = PasswordField('currentPassword',
                                    validators=[
                                        InputRequired(
                                            message="Please enter your current Password.")])
    newPassword1 = PasswordField('newPassword1',
                                 validators=[
                                     InputRequired(
                                         message="Please enter your new Password."),
                                     Length(min=4,
                                            message="Your password must contain at least 4 characters.")])
    newPassword2 = PasswordField('newPassword2',
                                 validators=[
                                     InputRequired(message=
                                                   "Please enter your new Password again."),
                                     EqualTo('newPassword1',
                                             message=
                                             'Passwords must match')])

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)

    def validate(self):
        """Custom validator to change credentials.

        Checks if user provided the correct password currently in use and
        changes it if user has entered a new password which has been
        verified by entering it a second time.

        :return: True if all checks have been passed.
        """

        rv = FlaskForm.validate(self)
        if not rv:
            return False

        users = get_users()

        if not checkpw(self.currentPassword.data.encode('utf-8'),
                       users[current_user.id].encode('utf-8')):
            self.currentPassword.errors.append('Invalid password')
            logger.info('Attempt to change password of '
                        + current_user.id
                        + ' failed due to wrong current password.')
            return False

        return True


class RegisterForm(FlaskForm):
    """This class defines part the registration form.

    The form provides entry fields for the chosen username and
    two entry fields for a password, the second one being used for verification.
    """

    username = StringField('username',
                           validators=[InputRequired(
                               message="Please enter a Username.")])

    password1 = PasswordField('password1',
                              validators=[
                                  InputRequired(
                                      message="Please enter your new Password."),
                                  Length(min=4,
                                         message="Your password must contain at least 4 characters.")])

    password2 = PasswordField('password2',
                              validators=[
                                  InputRequired(message=
                                                "Please enter your new Password again."),
                                  EqualTo('password1',
                                          message=
                                          'Passwords must match')])

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)

    def validate(self):
        """Custom validator for new user registrations.

        Checks if password is at least 4 characters long and verifies the
        correct entry by comparing it to the second input of password.

        :return: True if all checks have been passed.
        """

        rv = FlaskForm.validate(self)
        if not rv:
            return False
        return True
