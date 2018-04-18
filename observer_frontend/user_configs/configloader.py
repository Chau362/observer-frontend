"""This module loads configurations for a specific user.
"""

import os
import json
import logging

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


def load_config(username):
    """Load config file and return it.
    """

    path = os.path.dirname(os.path.abspath(__file__))
    file = username + ".json"
    try:
        with open(path + "/" + file) as jsonuser:
            config = json.load(jsonuser)
        return config
    except FileNotFoundError:
        logger.info('Could not retrieve configurations of user '
                    + username + '.')
        return None


def save_config(username, data):
    """Write and safe new config file.
    """

    path = os.path.dirname(os.path.abspath(__file__))
    file = username + ".json"
    try:
        with open(path + "/" + file, "w") as jsonuser:
            json.dump(data, jsonuser, sort_keys=True, indent=4)
    except FileNotFoundError:
        logger.error('Could not save configurations for user '
                    + username + '.')


def delete_configs(username):
    """Delete a config file for specified user.
    """

    path = os.path.dirname(os.path.abspath(__file__))
    file = username + ".json"

    os.remove(path + "/" + file)
    logger.info('Deleted configurations for ' + username + '.')
