import os
import json
import logging
from bcrypt import hashpw, gensalt
from flask import Flask

# logging setup
logger = logging.getLogger('src')


def get_users():
    """Opens the users file containing all usernames and passwords.

    Provides the dictionary with usernames and corresponding passwords
    of all users for the current application.
    :return: dictionary containing usernames and passwords
    """

    cwd = os.path.dirname(os.path.abspath(__file__))
    with open(cwd + '/users.json') as registered_users:
        users = json.load(registered_users)
    return users


class FlaskApp(Flask):
    """This provides a customized Flask application for the client frontend.

    It essentially adds a dictionary of all users of this app and a lock
    to protect this variable.
    """

    users = get_users()
    active_users = []
    active_processes = []
    registrations = {}

    def __init__(self, *args, **kwargs):
        super(FlaskApp, self).__init__(*args, **kwargs)

    @classmethod
    def add_user_and_password(cls, username, password):
        """Adds credentials for a new user to the users file.

        :param username: name the user has chosen for his account
        :param password: with which the user can access his account
        """

        users = cls.users
        users[username] = hashpw(password.encode('utf-8'),
                                 gensalt()).decode('utf-8')
        cwd = os.path.dirname(os.path.abspath(__file__))
        with open(cwd + "/users.json", "w") as outfile:
            json.dump(users, outfile, sort_keys=True, indent=4)
        cls.users = users

    @classmethod
    def delete_user(cls, username):
        """Removes credentials from users file.

        :param username: as indicator which account credentials to remove
        """

        users = cls.users
        users.pop(username, None)
        cwd = os.path.dirname(os.path.abspath(__file__))
        with open(cwd + "/users.json", "w") as outfile:
            json.dump(users, outfile, sort_keys=True, indent=4)
        cls.users = users

    @staticmethod
    def load_config(username):
        """Load config file and return Registration objects.
        """

        path = os.path.dirname(os.path.abspath(__file__))
        file = username + ".json"
        try:
            with open(path + "/user_configs/" + file) as jsonuser:
                config = json.load(jsonuser)
            registrations = config['registrations']
            return registrations
        except FileNotFoundError:
            logger.info('Could not retrieve configurations of user '
                        + username + '.')
            return []

    @staticmethod
    def save_config(username, data):
        """Write and safe new config file.
        """

        path = os.path.dirname(os.path.abspath(__file__))
        file = username + ".json"
        try:
            with open(path + "/user_configs/" + file, "w") as jsonuser:
                json.dump(data, jsonuser, sort_keys=True, indent=4)
        except FileNotFoundError:
            logger.error('Could not save configurations for user '
                         + username + '.')

    @staticmethod
    def delete_config(username):
        """Delete a config file for specified user.
        """

        path = os.path.dirname(os.path.abspath(__file__))
        file = username + ".json"

        os.remove(path + "/user_configs/" + file)
        logger.info('Deleted configurations for ' + username + '.')
