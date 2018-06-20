"""This module defines the user models which are used in the app.
"""

import logging
from flask_login import UserMixin, AnonymousUserMixin

logger = logging.getLogger('src.models')


class Project:
    """Generic class for registered projects.

    :ivar str project_url: url of the project at the webservice
    :ivar str event: type of event to be followed
    :ivar dict credentials: other information about the project
    """

    def __init__(self, project_url, event, credentials):
        """
        :param str project_url:
        :param str event:
        :param dict credentials:
        """

        self.project_url = project_url
        self.event = event
        self.credentials = credentials

    def __eq__(self, other):
        """Check the equality of two registrations.

        :param other: object to compare to
        :return: true if all attributes are the same
        """

        if isinstance(other, Project):

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

    def __hash__(self):
        return hash((self.project_url, self.event))

    def __repr__(self):
        return repr((self.project_url, self.event))

    def __str__(self):
        return self.event


class Registration:
    """Generic class for a registration.

    :ivar int registration_id: allocated by the conductor server
    :ivar str service: address of the conductor service
    :ivar str project_name: name chosen by the user for this project
    :ivar str project_url: url of the project
    :ivar str event: type of event to be followed
    :ivar bool active: indicator if user wants to be notified about this
    """

    def __init__(self, registration_id, service, project_name,
                 project_url, event, active=False):
        """
        :type service: string
        :type project_name: string
        :type project_url: string
        :type event: string
        :type active: bool
        """

        self.id = registration_id
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

    def __hash__(self):
        return hash((self.service, self.project_name,
                     self.project_url, self.event))

    def __repr__(self):
        return repr((self.id, self.service, self.project_name,
                     self.project_url, self.event, self.active))


class RegistrationSerializer:
    """This provides supporting functions for the Class `Registration`

    The `serialize_registration()` converts a dictionary with all information
    of a single registration into a `Registration` object. The
    `deserialize_registration()` does the opposite.
    """

    @staticmethod
    def serialize_registration(registration):
        """Turns a python `dict` into a Registration object.

        :param dict registration: containing parameters of the registration
        :return: Registration object
        """

        return Registration(registration['id'], registration['service'],
                            registration['project_name'],
                            registration['project_url'],
                            registration['event'],
                            registration['_active'])

    @staticmethod
    def deserialize_registration(registration):
        """Turns a Registration object into a python `dict`.

        :param registration: special object
        :return: dictionary containing parameters of the registration
        """

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
    attribute which is set to `Guest`.
    """

    def __init__(self):
        self.id = 'Guest'
        self.registrations = []
