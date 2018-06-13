"""This module tests the notifier application.
"""

import os
import socket
import unittest
import requests
from time import sleep
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
from src.models import Project
from src.notify.handler import EventHandler
from src.notify.settings import revolving
from src.notify.revolver import show_messages
from src.notify.eventhandler import handle_event
from src.notify.loggers import setup_logging


class MockConductorServer(BaseHTTPRequestHandler):
    """Customized request handler to mock a conductor server.
    """

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html'.encode("utf-8"))
        self.end_headers()

    def do_GET(self):
        """Respond to a GET request."""
        self._set_headers()

    def do_POST(self):
        """Respond to a POST request."""
        # get the posted data
        self._set_headers()

    def do_HEAD(self):
        """Respond to a HEAD request."""
        self._set_headers()


def get_free_port():
    s = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
    s.bind(('localhost', 0))
    address, port = s.getsockname()
    s.close()
    return port


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
        cls.handler = HTTPServer(('localhost', cls.handler_port), EventHandler)

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

    @unittest.skip
    def test_running_test_server(self):
        url = 'http://localhost:{port}/users'.format(port=self.mock_server_port)
        response = requests.head(url)
        self.assertEqual(response.status_code, 200)

    @unittest.skip
    def test_register(self):
        url = 'http://localhost:{port}/users'.format(port=self.mock_server_port)
        requester = request_maker.MyHTTPRequester('mock')
        response = requester.register('GIT_COMMIT', 'scam',
                                      'http://scam.com', url)
        self.assertEqual(response, '')

    @unittest.skip
    def test_unregister(self):
        url = 'http://localhost:{port}/users'.format(port=self.mock_server_port)
        requester = request_maker.MyHTTPRequester('mock')
        response = requester.unregister(url, '0')
        self.assertEqual(response, None)

    @unittest.skip
    def test_check_registrations(self):
        url = 'http://localhost:{port}/users'.format(port=self.mock_server_port)
        requester = request_maker.MyHTTPRequester('mock')
        response = requester.check_registrations([], url)
        self.assertEqual(response, None)

    def test_request_handler(self):
        url = 'http://localhost:{port}'.format(port=self.handler_port)
        response = requests.head(url)
        self.assertEqual(response.status_code, 200)
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        response = requests.post(url)
        self.assertEqual(response.status_code, 200)

    def test_revolver(self):
        self.assertTrue(revolving)

    def test_handler_function(self):
        event = Project('http://mock', 'GIT_COMMIT', None)
        result = handle_event(event)
        self.assertTrue(result)
        result = handle_event(event, show=True)
        self.assertTrue(result)
        event = Project('http://mock', 'SVN_COMMIT', None)
        result = handle_event(event)
        self.assertTrue(result)

    def test_logging(self):
        logger = setup_logging()
        logger.info('Succeeded in writing log information.')

    def test_revolver(self):
        self.assertFalse(revolving)
        revolver_thread = Thread(target=show_messages)
        revolver_thread.setDaemon(True)
        revolver_thread.start()
        sleep(3)
        self.assertTrue(revolving)


if __name__ == '__main__':
    unittest.main()
