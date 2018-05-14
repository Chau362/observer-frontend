"""This module defines the user models which are used in the app.
"""

import logging
from flask_login import UserMixin, AnonymousUserMixin


logger = logging.getLogger('src.models')


class Registration:
    """Generic class for a registration.
    """

    def __init__(self, service, project_name, project_url, event, active=False):
        """
        :type service: string
        :type project_name: string
        :type project_url: string
        :type event: string
        :type active: bool
        """

        self.service = service
        self.project_name = project_name
        self.project_url = project_url
        self.event = event
        self._active = active

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, value):
        if not type(value) == bool:
            raise TypeError("Attribute must be boolean.")
        self._active = value

    def __eq__(self, other):
        """Check the equality of two registrations.

        :param other: object to compare to
        :return: true if all attributes are the same
        """
        if isinstance(other, Registration):

            if not self.service == other.service:
                return False
            if not self.project_name == other.project_name:
                return False
            if not self.project_url == other.project_url:
                return False
            if not self.event == other.event:
                return False

            return True

        return False

    def __ne__(self, other):
        """Check the inequality of two registrations.

        :param other: object to compare to
        :return: true if any attribute is not the same
        """
        equal = self.__eq__(other)
        return not equal

    @property
    def __hash__(self):
        return hash((self.service, self.project_name,
                     self.project_url, self.event))

    def __repr__(self):
        return repr((self.service, self.project_name,
                     self.project_url, self.event))


class RegistrationSerializer:

    @staticmethod
    def serialize_registration(registration):
        return Registration(registration['service'],
                            registration['project_name'],
                            registration['project_url'],
                            registration['event'],
                            registration['_active'])

    @staticmethod
    def deserialize_registration(registration):
        return registration.__dict__


class User(UserMixin):
    """Generic class for authenticated users.

    Besides the inherited methods and attributes it defines an active
    flag to indicate if a user is currently interested in receiving
    information about new events.
    """

    def __init__(self):
        self._registrations = []

    @property
    def registrations(self):
        return self._registrations

    @registrations.setter
    def registrations(self, list_of_registrations):
        self._registrations = list(map(RegistrationSerializer.serialize_registration,
                                       list_of_registrations))


class Anonymous(AnonymousUserMixin):
    """Generic class for anonymous user.

    Besides the inherited methods and attributes it defines an id
    attribute which is set to Guest.
    """

    def __init__(self):
        self.id = 'Guest'
        self.registrations = []

    def serialize(self):
        return {
                'id': self.id,
                'is_authenticated': self.is_authenticated,
                'is_active': self.is_active,
        }



