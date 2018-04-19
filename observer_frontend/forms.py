"""This module contains all forms used by the Observer-Hive frontend.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, EqualTo, Length


class LoginForm(FlaskForm):
    """This class defines the login form.

       The form provides two entry fields for the user's
       credentials: username and password.
    """

    username = StringField('Username',
                           validators=[InputRequired(
                               message="Please enter a Username.")])
    password = PasswordField('Password',
                             validators=[InputRequired(
                                 message="Please enter your Password.")])


class ChangePasswordForm(FlaskForm):
    """This class defines the form to change an existing users password.

       The form provides one entry fields for the current password and two
       entry fields for new password, the second one being used for verification.
    """

    currentPassword = PasswordField('currentPassword',
                                    validators=[
                                        InputRequired(
                                            message="Please enter your current Password.")])
    newPassword1 = PasswordField('newPassword1',
                                 validators=[
                                     InputRequired(
                                         message="Please enter your new Password."),
                                     Length(min=4,
                                            message="Your password must contain at least 8 characters.")])
    newPassword2 = PasswordField('newPassword2',
                                 validators=[
                                     InputRequired(message=
                                                   "Please enter your new Password again."),
                                     EqualTo('newPassword1',
                                             message=
                                             'Passwords must match')])


class RegisterForm(FlaskForm):
    """This class defines part the registration form.

       The form provides entry fields for the chosen username and
       two entry fields for a password, the second one being used for verification.
    """

    username = StringField('Username',
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
