"""This module tests the application running the client frontend.
"""

import os
import unittest
from tempfile import NamedTemporaryFile
from src.__init__ import app


class ObserverFrontendTestCase(unittest.TestCase):
    """This class implements all tests for the flask app which runs the frontend.
    """

    test_user = "foobar"
    users = None

    @classmethod
    def setUpClass(cls):
        """Configures the app to be in testing mode."""
        # disable error catching during request handling
        app.config.from_object("src.config.TestingConfig")
        #  test client provides a simple interface to the application
        cls.app = app.test_client()
        # make temporary users file
        NamedTemporaryFile(prefix="foobar",
                           suffix=".json",
                           dir=app.cwd + "/user_configs/")

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        self.logout()

    def login(self, username, password):
        """Helper function for automated login."""
        return self.app.post('/login/', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        """Helper function for automated logout."""
        return self.app.get('/logout/', follow_redirects=True)

    def test_homepage(self):
        """Access homepage.

        Sends a HTTP GET request to homepage an checks if
        request status code is 200.
        """
        rv = self.app.get('/')
        self.assertTrue(rv.status_code, 200)

    def test_user_can_login(self):
        """Checks if user can log in.

        Calls the helper function to log in and then checks the
        ID (which is the username) of the current user and that
        the current user is not anonymous.
        """
        from flask_login import current_user
        with self.app:
            self.login('testUser', 'xxx')
            self.assertTrue(current_user.id == 'testUser')
            self.assertFalse(current_user.is_anonymous)

    def test_login_logout(self):
        """Check behaviour of log ins.

        The test will login with correct credentials,
        log the user out and then try to log in with
        incorrect password.
        """
        from flask_login import current_user
        with self.app:
            self.login('testUser', 'xxx')
            self.assertTrue(current_user.id == 'testUser')
            self.logout()
            self.assertTrue(current_user.is_anonymous)
            self.login('testUser', 'yyy')
            self.assertTrue(current_user.is_anonymous)

    def test_access_denied(self):
        """Checks protected pages showing user data.

        Only authenticated users can access the tested endpoints.
        The test checks if an unauthenticated user can access them.
        """
        rv = self.app.get('/profile/')
        self.assertEqual(rv.status_code, 302)
        rv = self.app.get('/profile/edit/')
        self.assertEqual(rv.status_code, 302)
        rv = self.app.get('/change-credentials/')
        self.assertEqual(rv.status_code, 302)

    def test_invalid_login(self):
        """Checks what happens if user uses invalid password.

        In case of an invalid login attempt the user should be
        redirected to the login page as the `LoginForm` validates
        to false.
        """
        self.login('testUser', 'hello')
        rv = self.app.get('/profile/')
        self.assertEqual(rv.status_code, 302)

    def test_unauthorized_access(self):
        """Checks what happens if unauthorized user calls protected endpoint.

        An unauthorized user is expected to be redirected to the login page.
        """
        rv = self.app.post('/profile/', data={})
        self.assertEqual(rv.status_code, 302)

    @unittest.skip
    def test_register_projects(self):
        from flask_login import current_user
        with self.app:
            self.login('testUser', 'xxx')
            self.assertTrue(current_user.id == 'testUser')
            rv = self.app.post('/profile/registration/', data=current_user.id)
            self.assertEqual(rv.status_code, 200)

    def test_authenticated_profile_view(self):
        """Checks if login process works as expected.

        After a successful login the authenticated user should be
        able to access the `profile` endpoint.
        """
        from flask_login import current_user
        with self.app:
            self.login('testUser', 'xxx')
            self.assertTrue(current_user.id == 'testUser')
            rv = self.app.post('/profile/')
            self.assertEqual(rv.status_code, 200)

    def test_successful_password_change(self):
        """Checks if an authenticated user can change his password.

        After a successful login the user mus be able to access the
        `change-credentials` endpoint and submit his new password.
        On success the user will be redirected to his `profile` page.
        """
        with self.app:
            self.login('foobar', 'yyyy')
            rv = self.app.get('/change-credentials/')
            self.assertEqual(rv.status_code, 200)
            response = self.app.post('/change-credentials/', data=dict(
                username='foobar', currentPassword='yyyy',
                newPassword1='yyyy', newPassword2='yyyy'))
            self.assertEqual(response.status_code, 302)

    def test_register_new_user(self):
        """Checks the registration process.

        After a user has submitted his data for registration, he
        should be redirected to his `profile` page.
        """
        with self.app:
            response = self.app.post('/register/', data=dict(
                username='MensMan', password1='shitty',
                password2='shitty', service='https://docs.pytest.org/en/latest/tmpdir.html'))
            self.assertEqual(response.status_code, 302)

    def test_activation_deactivation_of_events(self):
        """Checks if an authenticated user can change his status.

        After successful login the `/profile/activate/` and
        `/profile/deactivate/` endpoint should be able to accept
        requests and respond with a 200 status code.
        """
        with self.app:
            from flask_login import current_user
            self.login('foobar', 'yyyy')
            self.assertTrue(current_user.id == 'foobar')
            response = self.app.get('/profile/')
            self.assertEqual(response.status_code, 200)
            rv = self.app.post('/profile/activate/')
            self.assertEqual(rv.status_code, 200)
            rf = self.app.post('/profile/deactivate/')
            self.assertEqual(rf.status_code, 200)

    def test_edit_registrations(self):
        """Checks if `/profile/edit/` endpoint can be reached.

        After a successful login the user should be able to see
        reach this endpoint.
        """
        with self.app:
            from flask_login import current_user
            self.login('foobar', 'yyyy')
            self.assertTrue(current_user.id == 'foobar')
            response = self.app.get('/profile/')
            self.assertEqual(response.status_code, 200)
            response = self.app.get('/profile/edit/')
            self.assertEqual(response.status_code, 200)

    @unittest.skip
    def test_receive_event(self):
        """Checks the `event` endpoint.

        An HTTP POST request with an empty body is sent to
        the `event` endpoint. The request should be handled
        appropriately.
        """
        with self.app:
            from flask_login import current_user
            self.login('foobar', 'yyyy')
            self.assertTrue(current_user.id == 'foobar')
            response = self.app.post('/event/')
            self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
