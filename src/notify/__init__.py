"""This module starts the process which handles events from the conductor.

It starts a thread which will iterate through all received events and
handles them. Furthermore it imports the customized HTTPRequestHandler
for events and runs a simple server.
"""

from logging import getLogger
from http.server import HTTPServer
from threading import Thread
from src.notify.handler import EventHandler
from src.notify.eventhandler import handle_event
from src.notify.revolver import show_messages
from src.notify.settings import events

logger = getLogger('src.notify')

if __name__ == '__main__':
    notifier = Thread(target=show_messages)

    notifier.start()
    logger.info('Started notifier thread.')

    port = 9090
    server_address = ('', port)
    httpd = HTTPServer(server_address, EventHandler)

    logger.info('Started server process listening on port ' + str(port))
    httpd.serve_forever()
