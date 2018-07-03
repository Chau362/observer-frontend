"""This module starts the process which handles events from the conductor.

It starts a thread which will iterate through all received events and
handles them. Furthermore it imports the customized HTTPRequestHandler
for events and runs a simple server.
"""

from http.server import HTTPServer
from threading import Thread
from loggers import setup_logging
from handler import RequestHandler
from revolver import show_messages

logger = setup_logging()

if __name__ == '__main__':

    # start thread which shows all events in a loop
    notifier = Thread(target=show_messages)
    notifier.start()
    logger.info('Started notifier thread.')

    # setup server for receiving events
    port = 9090
    server_address = ('', port)
    httpd = HTTPServer(server_address, RequestHandler)

    # run the server
    logger.info('Started server process listening on port ' + str(port))
    httpd.serve_forever()
