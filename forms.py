from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, EqualTo


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(message="Please enter a Username.")])
    password = PasswordField('Password', validators=[InputRequired(message="Please enter your Password.")])


class ChangePassword(FlaskForm):
    cuurentPassword = PasswordField('currentPassword', [InputRequired(message="Please enter your current Password.")])
    newPassword1 = PasswordField('newPassword1', [InputRequired(), EqualTo('confirm', message='Passwords must match')])
    newPassword2 = PasswordField('newPassword2')
