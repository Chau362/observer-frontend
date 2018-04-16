from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, EqualTo, Length


class LoginForm(FlaskForm):
    username = StringField('Username', 
                           validators=[InputRequired(
                               message="Please enter a Username.")])
    password = PasswordField('Password',
                             validators=[InputRequired(
                                 message="Please enter your Password.")])


class ChangePasswordForm(FlaskForm):
    currentPassword = PasswordField('currentPassword',
                                    validators=[
                                    InputRequired(
                                    message="Please enter your current Password.")])
    newPassword1 = PasswordField('newPassword1',
                                 validators=[
                                     InputRequired(
                                     message="Please enter your new Password."),
                                     Length(min=8,
                                            message="Your password must contain at least 8 characters.")])
    newPassword2 = PasswordField('newPassword2',
                                 validators=[
                                     InputRequired(message=
                                                   "Please enter your new Password again."),
                                     EqualTo('newPassword1',
                                             message=
                                             'Passwords must match')])


class RegisterForm(FlaskForm):
    username = StringField('Username',
                           validators=[InputRequired(
                               message="Please enter a Username.")])

    password1 = PasswordField('password1',
                                 validators=[
                                     InputRequired(
                                         message="Please enter your new Password."),
                                     Length(min=8,
                                            message="Your password must contain at least 8 characters.")])

    password2 = PasswordField('password2',
                                 validators=[
                                     InputRequired(message=
                                                   "Please enter your new Password again."),
                                     EqualTo('password1',
                                             message=
                                             'Passwords must match')])