"""This module provides the actual function to show events.
"""

import os
import json
import requests
from time import sleep
from logging import getLogger
from src.notify.eventhandler import handle_event
from src.notify.settings import events
from src.models import Project

logger = getLogger('src.notify.revolver')
cwd = os.path.dirname(os.path.abspath(__file__))


def show_messages():
    """Runs an infinite loop which shows all events.

    The function gets the dictionary of active users from the customized
    Flask app and iterates through it. For each user the intersection of
    followed projects and events to show is made and only these events
    will be shown.
    :return: None
    """

    while True:
        active_users = requests.get('http://observer/active-users/')
        for user, project_list in json.loads(active_users.text).items():
            print(user)
            project_list = list(map(lambda project:
                                    Project(project['project_url'],
                                            project['event'], project),
                                    project_list))
            for event in events.intersection(project_list):
                handle_event(event)
        sleep(5)
