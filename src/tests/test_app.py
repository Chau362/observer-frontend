from src.__init__ import app, session, json
import unittest
import tempfile


class ObserverFrontendTestCase(unittest.TestCase):
    """This class implements all tests for the flask app which runs the frontend.
    """

    @classmethod
    def setUpClass(cls):
        # make temporary users file
        # cls.users = tempfile.mkstemp()
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        # disable error catching during request handling
        app.testing = True
        app.config['WTF_CSRF_ENABLED'] = False
        #  test client provides a simple interface to the application
        self.app = app.test_client()

    def tearDown(self):
        pass

    def login(self, username, password):
        return self.app.post('/login/', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
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
        rv = self.app.get('/change-password/')
        self.assertEqual(rv.status_code, 302)

    def test_invalid_login(self):
        self.login('testUser', 'xxx')
        rv = self.app.get('/profile/')

    def test_unauthorized_access(self):
        rv = self.app.post('/profile/', data={})
        self.assertEqual(rv.status_code, 302)

    def test_register_projects(self):
        from flask_login import current_user
        with self.app:
            self.login('testUser', 'xxx')
            self.assertTrue(current_user.id == 'testUser')
            rv = self.app.post('/profile/registration/', data=current_user.id)
            self.assertEqual(rv.status_code, 200)

    def test_unauthenticated_profile_view(self):
        from flask_login import current_user
        with self.app:
            self.login('testUser', 'xxx')
            self.assertTrue(current_user.id == 'testUser')
            rv = self.app.post('/profile/')
            self.assertEqual(rv.status_code, 200)

    def test_successful_password_change(self):
        with self.app:
            self.login('foobar', 'yyyy')
            rv = self.app.get('/change-password/')
            self.assertEqual(rv.status_code, 200)
            response = self.app.post('/change-password/', data=dict(
                currentPassword='yyyy', newPassword1='yyyy',
                newPassword2='yyyy'))
            self.assertEqual(response.status_code, 302)

    def test_register_new_user(self):
        with self.app:
            response = self.app.post('/register/', data=dict(
                username='MensMan', password1='shitty',
                password2='shitty', service='https://docs.pytest.org/en/latest/tmpdir.html'))
            self.assertEqual(response.status_code, 302)

    def test_activation_deactivation_of_events(self):
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
        with self.app:
            from flask_login import current_user
            self.login('foobar', 'yyyy')
            self.assertTrue(current_user.id == 'foobar')
            response = self.app.get('/profile/')
            self.assertEqual(response.status_code, 200)
            response = self.app.get('/profile/edit/')
            self.assertEqual(response.status_code, 200)

    def test_receive_event(self):
        with self.app:
            from flask_login import current_user
            self.login('foobar', 'yyyy')
            self.assertTrue(current_user.id == 'foobar')
            response = self.app.post('/event/')
            self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
