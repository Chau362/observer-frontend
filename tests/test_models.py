"""Tests for `models.py`.
"""

import unittest, sys, os
from src.models import Registration, RegistrationSerializer, \
    Project

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/tests')

class ModelsTestCase(unittest.TestCase):
    """Class with test cases for all models in use.
    """

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_Registration_equals(self):
        """Tests the equals function of the class `Registration`.

        The test creates two objects with almost the same attributes.
        Only the ID which usually will be allocated by the conductor
        server is different. Such registrations refer to the same
        project and thus should be considered equal.
        """

        event = "GIT_PUSH"
        url = "http://github.com"
        name = "Schlumpf"
        service = "http://192.168.4.44/register"

        object_1 = Registration(event=event,
                                project_url=url,
                                project_name=name,
                                service=service,
                                registration_id=1)
        object_2 = Registration(event=event,
                                project_url=url,
                                project_name=name,
                                service=service,
                                registration_id=2)

        self.assertEqual(object_1, object_2)

    def test_Project_equals(self):
        """Tests the equals function of the class `Project`.

        The test creates two objects with the same `project_url` and the
        same `event`. Only the `credentials` attribute is different.
        Such objects refer to the same project and thus should be
        considered equal.
        """

        event = "GIT_COMMIT"
        url = "http://github.com"

        object_1 = Project(event=event,
                           project_url=url,
                           credentials={"eventType": "GIT_COMMIT",
                                        "name": "foo"})
        object_2 = Project(event=event,
                           project_url=url,
                           credentials={"projectUrl": "http://github.com",
                                        "name": "foobar"})

        self.assertEqual(object_1, object_2)
