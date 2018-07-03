"""This module contains the handler class for events from Gitlab and Github.

The `GitEventHandler` class implements all functions for handling events
received from Gitlab or Github.
"""

from eventhandler import EventHandler


class GitEventHandler(EventHandler):
    """Class to handle events received from Github and Gitlab.
    """

    def __init__(self):
        self.event_type = "GIT_COMMIT"
        # self-made Github icon for the unicorn hat
        self.icon = [[(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
                      (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)],
                     [(0, 0, 0), (255, 0, 0), (0, 0, 0), (0, 0, 0),
                      (0, 0, 0), (0, 0, 0), (255, 0, 0), (0, 0, 0)],
                     [(0, 0, 0), (0, 0, 0), (255, 0, 0), (255, 0, 0),
                      (255, 0, 0), (255, 0, 0), (0, 0, 0), (0, 0, 0)],
                     [(0, 0, 0), (0, 0, 0), (255, 0, 0), (0, 0, 0),
                      (0, 0, 0), (255, 0, 0), (0, 0, 0), (0, 0, 0)],
                     [(255, 0, 0), (0, 0, 0), (255, 0, 0), (255, 0, 0),
                      (255, 0, 0), (255, 0, 0), (0, 0, 0), (0, 0, 0)],
                     [(255, 0, 0), (255, 0, 0), (0, 0, 0), (255, 0, 0),
                      (255, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)],
                     [(0, 0, 0), (255, 0, 0), (255, 0, 0), (255, 0, 0),
                      (255, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)],
                     [(0, 0, 0), (0, 0, 0), (0, 0, 0), (255, 0, 0),
                      (255, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)]]

    def show_icon(self):
        """Shows Github icon on unicorn hat.

        :return: None
        """

        try:
            import unicornhat, signal
        except ImportError:
            return

        unicornhat.set_pixels(self.icon)
        unicornhat.show()
        signal.pause()