
import os
import json
import unittest
from src.myflask import FlaskApp
from src.config import basedir


class FlaskAppTestCase(unittest.TestCase):

    app = None
    cwd = os.path.dirname(os.path.abspath(__file__))
    username = "foo"
    password = "foobar"
    registrations = [{
            "_active": True,
            "event": "GIT_COMMIT",
            "id": "1",
            "project_name": "scab-oberserver",
            "project_url": "https://iteragit.iteratec.de/observer-hive/scab-oberserver-hive.git",
            "service": "http://192.168.4.46:8080/register"
        }]

    @classmethod
    def setUpClass(cls):
        cls.app = FlaskApp(__name__)
        # set configurations of this app
        cls.app.config.from_object("src.config.TestingConfig")

    @classmethod
    def tearDownClass(cls):
        cls.app.delete_user(cls.username)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_add_new_user(self):
        self.app.add_user_and_password(self.username, self.password)
        dir = os.path.split(self.cwd)[0]
        with open(dir + "/src/users.json", "r") as userfile:
            users = json.load(userfile)
        user_exists = True if self.username in users else False
        self.assertTrue(user_exists)

    def test_save_config(self):
        self.app.save_config(self.username, self.registrations)
        dir = os.path.split(self.cwd)[0]
        self.assertTrue(os.path.isfile(dir + "/src/user_configs/" + self.username + ".json"))

    def test_load_config(self):
        registrations = self.app.load_config(self.username)
        self.assertEqual(type(registrations), list)

    def test_rename_user(self):
        new_name = "fatman"
        new_password = "cheappassword"
        self.app.rename_user(self.username, new_name, new_password)
        dir = os.path.split(self.cwd)[0]
        with open(dir + "/src/users.json", "r") as userfile:
            users = json.load(userfile)
        user_exists = True if new_name in users else False
        self.assertTrue(user_exists)

    def test_delete_user(self):
        self.app.delete_user(self.username)
        dir = os.path.split(self.cwd)[0]
        with open(dir + "/src/users.json", "r") as userfile:
            users = json.load(userfile)
        user_exists = True if self.username in users else False
        self.assertFalse(user_exists)

    def test_delete_config(self):
        self.app.delete_config(self.username)


if __name__ == '__main__':
    unittest.main()
