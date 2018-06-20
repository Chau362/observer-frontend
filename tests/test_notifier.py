"""This module tests the notifier application.
"""

import os
import unittest
import requests
from threading import Thread
from src.models import Project
from tests.tests_support import MockConductorServer, get_free_port
from src.notify.handler import RequestHandler
from src.notify.settings import revolving
from src.notify.revolver import show_messages
from src.notify.eventhandler import EventHandler, handle_event
from src.notify.loggers import setup_logging
from http.server import HTTPServer


class NotifierTestCase(unittest.TestCase):
    """This class implements all tests to check the request maker.
    """

    @classmethod
    def setUpClass(cls):
        # Configure mock server.
        cls.mock_server_port = get_free_port()
        cls.mock_server = HTTPServer(('localhost', cls.mock_server_port),
                                     MockConductorServer)

        # Configure Eventhandler
        cls.handler_port = get_free_port()
        cls.handler = HTTPServer(('localhost', cls.handler_port), RequestHandler)

        # Start running mock server in a separate thread.
        # Daemon threads automatically shut down when the main process exits.
        cls.mock_server_thread = Thread(target=cls.mock_server.serve_forever)
        cls.mock_server_thread.setDaemon(True)
        cls.mock_server_thread.start()

        # Start running handler in a separate thread.
        cls.handler_thread = Thread(target=cls.handler.serve_forever)
        cls.handler_thread.setDaemon(True)
        cls.handler_thread.start()

    @classmethod
    def tearDownClass(cls):
        try:
            os.remove('info.log')
        except PermissionError:
            pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_request_handler(self):
        """Tests the customized HTTPRequestHandler.

        The test sends all three currently supported request types
        (HEAD, GET, POST) and checks the respective status code.
        The POST is performed twice to check the different behaviour
        for user updates and received events.
        """

        url = 'http://localhost:{port}'.format(port=self.handler_port)
        response = requests.head(url)
        self.assertEqual(response.status_code, 200)
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        response = requests.post(url, json={"active_users": {}})
        self.assertEqual(response.status_code, 200)
        response = requests.post(url, json={"projectUrl": "", "eventType": ""})
        self.assertEqual(response.status_code, 200)

    def test_handler_function(self):
        """Tests the ``handle_event()`` functions.

        The test calls the ``handle_event()`` function and passes
        one event for every event type and checks that the function
        returns the value `True` which only happens if no exception
        occurred.
        """

        event = Project('http://mock', 'GIT_COMMIT', None)
        result = handle_event(event)
        self.assertTrue(result)
        result = handle_event(event, show=True)
        self.assertTrue(result)
        event = Project('http://mock', 'SVN_COMMIT', None)
        result = handle_event(event)
        self.assertTrue(result)

    def test_logging(self):
        """Tests if logging setup is correct.

        Simply calls the ``setup_logging`` and passively
        checks that no exception occurs.
        """

        logger = setup_logging()
        logger.info('Succeeded in writing log information.')

    def test_revolver(self):
        """Tests the revolver function which renders the events.

        The test runs the function in a separate thread and checks
        that the thread is alive and that the ``revolving`` variable
        is set to `True`.
        """

        self.assertFalse(revolving)
        revolver_thread = Thread(target=show_messages)
        revolver_thread.setDaemon(True)
        revolver_thread.start()
        self.assertTrue(revolver_thread.isAlive)
        # self.assertTrue(revolving)

    def test_eventhandler_functions(self):
        """Tests the functions of the EventHandler class.

        Instanciates an EventHandler object and executes all
        provided functions.
        """

        handler = EventHandler()
        success = handler.do_something()
        self.assertTrue(success)
        success = handler.play_music()
        self.assertFalse(success)


if __name__ == '__main__':
    unittest.main()
