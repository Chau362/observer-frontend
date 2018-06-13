"""This module defines a customized HTTPRequestHandler to receive events.
"""

import json
from logging import getLogger
from http.server import BaseHTTPRequestHandler
from src.models import Project
from src.notify.settings import events, active_users

logger = getLogger('notifier.handler')


class EventHandler(BaseHTTPRequestHandler):
    """Customized BaseHTTPRequestHandler.
    """

    def _set_headers(self):
        """Set header according to response.
        """
        self.send_response(200)
        self.send_header('Content-type', 'text/html'.encode("utf-8"))
        self.end_headers()

    def do_HEAD(self):
        """Respond to a HEAD request.
        """
        self._set_headers()

    def do_GET(self):
        """Respond to a GET request.

        This request type is currently not supported.
        """
        self._set_headers()

    def do_POST(self):
        """Respond to a POST request and add the event to a set.
        """

        # get the posted data
        self._set_headers()

        content_length = int(self.headers['Content-Length'])
        # read data and convert from bytes to string
        received_data = self.rfile.read(content_length).decode('utf-8')

        try:
            # deserialize data into python object
            data = json.loads(received_data)
        except:
            return

        if "active_users" in data:
            for user in active_users:
                if user not in data["active_users"]:
                    active_users.pop(user, None)
            active_users.update(data["active_users"])

            self.wfile.write(b"<html><head><title>client-messenger</title></head>")
            self.wfile.write(b"<body><p>Updated dict of active users.</p>")
            self.wfile.write(b"</body></html>")
        else:
            project = Project(data['projectUrl'], data['eventType'], data)
            events.add(project)

            self.wfile.write(b"<html><head><title>client-messenger</title></head>")
            self.wfile.write(b"<body><p>Received your event and added it to set.</p>")
            self.wfile.write(b"</body></html>")
