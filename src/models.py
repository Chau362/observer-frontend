"""This module defines the user models which are used in the app.
"""

from flask_login import UserMixin, AnonymousUserMixin
from itsdangerous import URLSafeTimedSerializer

#Login_serializer used to encryt and decrypt the cookie token for the remember
#me option of flask-login
login_serializer = URLSafeTimedSerializer("SECRET_KEY")

class User(UserMixin):
    """Generic class for authenticated users.

       Besides the inherited methods and attributes it defines an active
       flag to indicate if a user is currently interested in receiving
       information about new events.
    """

    def __init__(self):
        self.active = False

    def serialize(self):
        return {
                'id': self.id,
                'is_authenticated': self.is_authenticated,
                'is_active': self.is_active,
                'is_anonymous': self.is_anonymous,
                'active': self.active,
            }


class Anonymous(AnonymousUserMixin):
    """Generic class for anonymous user.

       Besides the inherited methods and attributes it defines an id
       attribute which is set to Guest.
    """

    def __init__(self):
        self.id = 'Guest'

    def serialize(self):
        return {
                'id': self.id,
                'is_authenticated': self.is_authenticated,
                'is_active': self.is_active,
                'active': self.active,
            }