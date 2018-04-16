from flask_login.mixins import UserMixin, AnonymousUserMixin
import itertools


users = {}


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