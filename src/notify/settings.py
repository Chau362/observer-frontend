"""This module defines cross module variables which are used to handle events.
"""

events = set()
""":ivar set events: set of events which have been received"""

active_users = {}
""":ivar dict active_users: dict of users who want to be notified"""

revolving = False
""":ivar bool revolving: indicator if events are shown"""


def toggle_revolving():
    global revolving
    revolving = True
