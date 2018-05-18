
import json
from logging import getLogger
from http.server import HTTPServer, BaseHTTPRequestHandler
from multiprocessing import Process
from src.lights.eventhandler import handle_event

logger = getLogger('src.lights')


class EventHandler(BaseHTTPRequestHandler):

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

        This request type shall not be allowed.
        """
        pass

    def do_POST(self):
        """Respond to a POST request.
        """
        # get the posted data
        self._set_headers()

        content_length = int(self.headers['Content-Length'])
        # read data and convert from bytes to string
        received_data = self.rfile.read(content_length).decode('utf-8')

        try:
            # deserialize data into python object
            event = json.loads(received_data)
        except:
            return

        print('Received event.')
        handle_event(event)
        # event_process = Process(target=handle_event, kwargs={'event': event})
        # event_process.start()


if __name__ == '__main__':
    port = 9090
    server_address = ('', port)
    httpd = HTTPServer(server_address, EventHandler)

    print('Started server process listening on port ' + str(port))
    httpd.serve_forever()
