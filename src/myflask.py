import os
import json
import logging
from bcrypt import hashpw, gensalt
from flask import Flask

# logging setup
logger = logging.getLogger('src')


def get_users(cwd, file_name):
    """Get users and their passwords.

    :param str cwd: current working directory
    :param str file_name: name of the file containing the credentials
    :return: dictionary of users and passwords
    """

    with open(cwd + '/' + file_name + '.json') as registered_users:
        users = json.load(registered_users)
    return users


class FlaskApp(Flask):
    """This class provides a customized Flask application for the client frontend.

    :ivar str cwd: current working directory
    :ivar dict users: all users currently registered
    :ivar dict active_users: users which want to be notified
    """

    cwd = os.path.dirname(os.path.abspath(__file__))
    users = get_users(cwd, 'users')
    active_users = {}

    def __init__(self, *args, **kwargs):
        super(FlaskApp, self).__init__(*args, **kwargs)

    @classmethod
    def add_user_and_password(cls, username, password):
        """Adds credentials for a new user to the users file.

        :param str username: name the user has chosen for his account
        :param str password: with which the user can access his account
        """

        users = cls.users
        users[username] = hashpw(password.encode('utf-8'),
                                 gensalt()).decode('utf-8')
        try:
            with open(cls.cwd + "/users.json", "w") as outfile:
                json.dump(users, outfile, sort_keys=True, indent=4)
        except:
            logger.info('Unable to write new user file.')
        cls.users = users

    @classmethod
    def delete_user(cls, username):
        """Removes credentials from users file.

        :param str username: indicates which account credentials to remove
        """

        users = cls.users
        users.pop(username, None)
        try:
            with open(cls.cwd + "/users.json", "w") as outfile:
                json.dump(users, outfile, sort_keys=True, indent=4)
            try:
                file = username + ".json"
                os.remove(cls.cwd + "/user_configs/" + file)
            except FileNotFoundError:
                logger.info('User ' + username + ' had no registered projects.')
        except FileNotFoundError:
            logger.info('Unable to write new user file.')
        cls.users = users

    @classmethod
    def rename_user(cls, current_name, new_name, new_password):
        """Changes user credentials as indicated.

        :param str current_name: current name used by the user
        :param str new_name: new name to save
        :param str new_password: new password to save
        """
        users = cls.users
        users.pop(current_name, None)

        users[new_name] = hashpw(new_password.encode('utf-8'),
                                 gensalt()).decode('utf-8')
        try:
            with open(cls.cwd + "/users.json", "w") as outfile:
                json.dump(users, outfile, sort_keys=True, indent=4)
        except:
            logger.info('Unable to write new user file.')

        cls.users = users

        old_file = current_name + ".json"
        new_file = new_name + ".json"
        try:
            os.rename(cls.cwd + "/user_configs/" + old_file, cls.cwd + "/user_configs/" + new_file)
            logger.info("Renamed file containing configs of user "
                        + current_name + ".")
        except FileNotFoundError:
            logger.info('User ' + current_name + ' had no registered projects.')

    @classmethod
    def load_config(cls, username):
        """Loads the config file and returns the list of registrations.

        :param str username: indicating for which user
        :return: list of dictionaries representing registrations
        """

        file = username + ".json"
        try:
            with open(cls.cwd + "/user_configs/" + file) as jsonuser:
                config = json.load(jsonuser)
            registrations = config['registrations']
            return registrations
        except FileNotFoundError:
            logger.info('Could not retrieve configurations of user '
                        + username + '.')
            return []

    @classmethod
    def save_config(cls, username, data):
        """Write and safe new config file.

        :param str username: specifying the user
        :param list data: list containing all registrations to save
        :return: None
        """

        file = username + ".json"
        data.sort(key=lambda registration: registration['id'])
        data.sort(key=lambda registration: registration['project_name'])
        data.sort(key=lambda registration: registration['service'])
        try:
            with open(cls.cwd + "/user_configs/" + file, "w") as jsonuser:
                json.dump({"registrations": data}, jsonuser, sort_keys=True, indent=4)
        except FileNotFoundError:
            logger.error('Could not save configurations for user '
                         + username + '.')

    @classmethod
    def delete_config(cls, username):
        """Delete a config file for specified user.

        :param str username: specifying the user
        :return: None
        """

        file = username + ".json"
        try:
            os.remove(cls.cwd + "/user_configs/" + file)
        except FileNotFoundError:
            logger.info('Found no configurations for ' + username + '.')
        logger.info('Deleted configurations for ' + username + '.')
