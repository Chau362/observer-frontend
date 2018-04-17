"""This module defines the user models which are used in the app.
"""

from flask_login import UserMixin, AnonymousUserMixin


class User(UserMixin):
    """Generic class for authenticated users.

       Besides the inherited methods and attributes it defines an active
       flag to indicate if a user is currently interested in receiving
       information about new events.
    """

    def __init__(self):
        self.active = False


class Anonymous(AnonymousUserMixin):
    """Generic class for anonymous user.

       Besides the inherited methods and attributes it defines an id
       attribute which is set to Guest.
    """

    def __init__(self):
        self.id = 'Guest'