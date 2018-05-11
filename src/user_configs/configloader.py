"""This module loads configurations for a specific user.
"""

import os
import json
import logging

# logging setup
logger = logging.getLogger('src')


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
