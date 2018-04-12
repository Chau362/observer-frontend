from flask_login.mixins import UserMixin, AnonymousUserMixin
import json
import itertools

# mock database of users
users = [
    {'id': '1', 'username': 'admin', 'password': 'xxx', 'is_admin': True},
    {'id': '2', 'username': 'desmond', 'password': 'yyy', 'is_admin': False}
]

def find_user_by_id(user_id):
    for _user in users:
        if _user['id'] == user_id:
            return _user
    return None

class User(UserMixin, object):
    new_id = itertools.count(0)

    def __init__(self):
        super().__init__()
        self.id = next(self.new_id)


# https://code.luasoftware.com/tutorials/flask/how-to-configure-flask-login/

class LoginUser(UserMixin):

    def __init__(self, id):
        self.id = id

    @property
    def username(self):
        user = self.get_user()
        return user['username']

    @property
    def is_admin(self):
        user = self.get_user()
        return user['is_admin']

    def get_user(self):
        return find_user_by_id(self.id)


class AnonymousUser(AnonymousUserMixin):

    def __init__(self):
        self.username = "Guest"

    @property
    def username(self):
        return "Guest"

    @property
    def is_admin(self):
        return None

    def get_user(self):
        return None