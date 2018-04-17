from observer_frontend.observer_frontend import app
import unittest
import tempfile


class ObserverFrontendTestCase(unittest.TestCase):
    """This class implements all tests for the flask app which runs the frontend.
    """

    def setUp(self):
        # make temporary users file
        self.users = tempfile.mkstemp()
        # disable error catching during request handling
        app.testing = True
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

            Sends a HTTP GET request to homepage an checks for keyword
            in retrieved template.
        """
        rv = self.app.get('/')
        assert b'Welcome' in rv.data

    def test_valid_login(self):
        """Checks login process.
        """
        rv = self.login('testUser', 'xxx')
        assert b'testUser' in rv.data

    def test_access_denied(self):
        rv = self.app.get('/change-password/')
        self.assertEquals(rv.status_code, 302)

    def test_invalid_login(self):
        self.login('testUser', 'xxx')
        rv = self.app.get('/profile/')

    @unittest.skip("can't login")
    def test_unauthorized_activation(self):
        rv = self.app.post('/profile/register/', data={})
        self.assertEqual(rv.status_code, 302)

    @unittest.skip("can't login")
    def test_register_projects(self):
        with self.app as c:
            self.login('testUser', 'xxx')
            rv = c.post('/profile/register/', data={})
            self.assertEquals(rv.status_code, 200)


if __name__ == '__main__':
    unittest.main()
