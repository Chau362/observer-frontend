"""This module provides the actual function to show events.
"""

import os
import yaml
from time import sleep
from logging import getLogger
from settings import events, active_users, revolving, \
    toggle_revolving
from src.models import Project
from giteventhandler import GitEventHandler
from svneventhandler import SVNEventHandler

logger = getLogger('notifier.revolver')
cwd = os.path.dirname(os.path.abspath(__file__))

with open(cwd + "/" + "config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)


def handle_event(event, pihat=cfg['pihat'], project_name=None):
    """Handle event as specified by eventhandler object.

    The function instantiates an object according to the webservice the
    event is related to and renders the event.

    :param event: with all information about what happened
    :param dict pihat: indicates which hat to be used
    :param str project_name: name the user has chosen for this project
    :return: None
    """

    handler = GitEventHandler() if event.event == 'GIT_COMMIT' else SVNEventHandler()

    # find out which hat is connected
    if pihat['unicorn']:
        handler.show_icon()
    elif pihat['ledstrip']:
        handler.show_on_led()
    elif pihat['breadboard']:
        pass
    else:
        handler.do_something()

    return True


def show_messages():
    """Runs an infinite loop which shows all events.

    The function gets the dictionary of active users from the customized
    Flask app and iterates through it. For each user the intersection of
    followed projects and events to show is made and only these events
    will be shown.

    :return: None
    """

    while True:

        if not revolving:
            toggle_revolving()

        for user, project_list in active_users.items():
            logger.info(user)
            project_list = set(map(lambda project:
                                    Project(project['project_url'],
                                            project['event'], project),
                                    project_list))
            for event in events.intersection(project_list):
                handle_event(event)
        sleep(5)
