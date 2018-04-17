from observer_frontend import request_maker
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
import socket
import requests
import unittest


class MockServerRequestHandler(BaseHTTPRequestHandler):
    """Customized request handler to test request maker.
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


class RequestMakerTestCase(unittest.TestCase):
    """This class implements all tests to check the request maker.
    """

    @classmethod
    def setUpClass(cls):
        # Configure mock server.
        cls.mock_server_port = get_free_port()
        cls.mock_server = HTTPServer(('localhost', cls.mock_server_port), MockServerRequestHandler)

        # Start running mock server in a separate thread.
        # Daemon threads automatically shut down when the main process exits.
        cls.mock_server_thread = Thread(target=cls.mock_server.serve_forever)
        cls.mock_server_thread.setDaemon(True)
        cls.mock_server_thread.start()

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_running_test_server(self):
        url = 'http://localhost:{port}/users'.format(port=self.mock_server_port)
        response = requests.head(url)
        self.assertEqual(response.status_code, 200)

    def test_register(self):
        url = 'http://localhost:{port}/users'.format(port=self.mock_server_port)
        requester = request_maker.MyHTTPRequester('mock')
        response = requester.register('GIT_COMMIT', 'scam',
                                      'http://scam.com', url)
        self.assertEqual(response, '')

    def test_unregister(self):
        url = 'http://localhost:{port}/users'.format(port=self.mock_server_port)
        requester = request_maker.MyHTTPRequester('mock')
        response = requester.unregister(url, '0')
        self.assertEqual(response, None)

    def test_check_registrations(self):
        url = 'http://localhost:{port}/users'.format(port=self.mock_server_port)
        requester = request_maker.MyHTTPRequester('mock')
        response = requester.check_registrations([], url)
        self.assertEqual(response, None)


if __name__ == '__main__':
    unittest.main()
