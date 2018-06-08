"""This module defines classes to handle events.

For every webservice which can be observed there is one class which provides
custom functions to notify the user about events.
"""

import os
import simpleaudio as audio
import logging

logger = logging.getLogger('src.notify.eventhandler')


class EventHandler:
    """Base class providing a minimal set of functions to handle events.
    """

    @staticmethod
    def play_music(**kwargs):
        """Plays an alert.
        """

        path = os.path.dirname(os.path.abspath(__file__))
        file = "morse.wav"

        wave_obj = audio.WaveObject.from_wave_file(path + "/" + file)
        play_obj = wave_obj.play()
        play_obj.wait_done()

    @staticmethod
    def do_something():
        """Writes a logging message that event was received.

        :return: None
        """

        logger.info("I handled an event.")

    @staticmethod
    def show_on_unicorn(projectname, event):
        """Shows given parameters on a unicorn hat for RaspberryPi.

        :param projectname: which user has chosen for this project
        :param event: that happened
        :return: None
        """

        try:
            import unicornhat as unicorn
            from pyfiglet import figlet_format
        except ImportError:
            logger.error('Could not import modules to start Unicorn Hat.')
            return

        unicorn.set_layout(unicorn.AUTO)
        unicorn.rotation(0)
        unicorn.brightness(0.5)
        width, height = unicorn.get_shape()

        TXT = projectname + ': ' + event

        figletText = figlet_format(TXT + ' ', "banner", width=1000)  # banner font generates text with heigth 7
        textMatrix = figletText.split("\n")[:width]  # width should be 8 on both HAT and pHAT!
        textWidth = len(textMatrix[0])  # the total length of the result from figlet

        i = -1

        i = 0 if i >= 100 * textWidth else i + 1  # avoid overflow
        for h in range(height):
            for w in range(width):
                hPos = (i + h) % textWidth
                chr = textMatrix[w][hPos]
                if chr == ' ':
                    unicorn.set_pixel(width - w - 1, h, 0, 0, 0)
                else:
                    unicorn.set_pixel(width - w - 1, h, 255, 0, 0)
        unicorn.show()


class GitEventHandler(EventHandler):
    """Class to handle events on Github.
    """

    def __init__(self):
        # super.__init__()
        self.event_type = "GIT_COMMIT"


class SVNEventHandler(EventHandler):
    """Class to handle events on SVN.
    """

    def __init__(self):
        # super.__init__()
        self.event_type = "SVN_COMMIT"


# class UnicornHandler(EventHandler):
#     try:
#         from pyfiglet import figlet_format
#     except ImportError:
#         exit()
#
#     import unicornhat as unicorn
#
#     def __init__(self, event_type):
#         super().__init__(event_type)
#
#     def show_event_as_text(self):
#         unicorn.set_layout(unicorn.AUTO)
#         unicorn.rotation(0)
#         unicorn.brightness(0.5)
#         width, height = unicorn.get_shape()
#
#         TXT = self.event_type
#
#         figletText = figlet_format(TXT + ' ', "banner", width=1000)  # banner font generates text with heigth 7
#         textMatrix = figletText.split("\n")[:width]  # width should be 8 on both HAT and pHAT!
#         textWidth = len(textMatrix[0])  # the total length of the result from figlet
#
#         i = -1
#         while True:
#             i = 0 if i >= 100 * textWidth else i + 1  # avoid overflow
#             for h in range(height):
#                 for w in range(width):
#                     hPos = (i + h) % textWidth
#                     chr = textMatrix[w][hPos]
#                     if chr == ' ':
#                         unicorn.set_pixel(width - w - 1, h, 0, 0, 0)
#                     else:
#                         unicorn.set_pixel(width - w - 1, h, 255, 0, 0)
#             unicorn.show()
#             sleep(0.2)


def handle_event(event):
    handler = GitEventHandler() if event == 'GIT_COMMIT' else SVNEventHandler()
    handler.do_something()
