"""This module implements supporting features for tests.
"""

import json
import socket
import itertools
from requests import post
from http.server import BaseHTTPRequestHandler
import os, sys
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/tests')

def get_free_port():
    """Looks for a port at which a socket can still bind.

    :return: port number which is not currently in use
    """

    s = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
    s.bind(('localhost', 0))
    address, port = s.getsockname()
    s.close()
    return port


class MockConductorServer(BaseHTTPRequestHandler):
    """Customized request handler to mock a conductor server.

    The main feature is that is generates an ID for each successful
    POST request and sends this as a response to the request. Furthermore
    it sends an exemplary event to the specified callback address to fully
    simulate a conductor server.
    """

    new_id = itertools.count()

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        """Respond to a GET request."""
        self._set_headers()

    def do_POST(self):
        """Respond to a POST request."""
        self._set_headers()

        content_length = int(self.headers['Content-Length'])
        # read data and convert from bytes to string
        received_data = self.rfile.read(content_length).decode('utf-8')

        try:
            # deserialize data into python object
            data = json.loads(received_data)
        except:
            return

        self.wfile.write(json.dumps(next(self.new_id)).encode())

        try:
            post(data["callback"], json={"projectUrl":"", "eventType":""})
        except (ConnectionError, ConnectionAbortedError,
                ConnectionRefusedError, KeyError):
            return

    def do_HEAD(self):
        """Respond to a HEAD request."""
        self._set_headers()