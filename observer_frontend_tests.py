import os
import observer_frontend
import unittest
import tempfile

class ObserverFrontendTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, observer_frontend.app.config['DATABASE'] = tempfile.mkstemp()
        observer_frontend.app.testing = True
        self.app = observer_frontend.app.test_client()
        with observer_frontend.app.app_context():
            observer_frontend.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(observer_frontend.app.config['DATABASE'])

if __name__ == '__main__':
    unittest.main()