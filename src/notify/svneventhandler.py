"""This module contains the handler class for events from SVN.

The `SVNEventHandler` class implements all functions for handling events
received from SVN.
"""

from eventhandler import EventHandler
from logging import getLogger
from random import randint
from time import sleep

logger = getLogger('notifier.giteventhandler')


class SVNEventHandler(EventHandler):
    """Class to handle events from SVN.
    """

    def __init__(self):
        self.event_type = "SVN_COMMIT"
        # self-made SVN icon for the unicorn hat
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
        """Shows SVN icon on unicorn hat.

        :return: None
        """

        try:
            import unicornhat, signal
        except ImportError:
            logger.info('Could not import modules to show messages on Unicorn.')
            return

        unicornhat.set_pixels(self.icon)
        unicornhat.show()
        signal.pause()

    def show_on_led(self):
        """Shows events sent from Github on WS2801 LED strip.

        :return: None
        """

        try:
            import Adafruit_WS2801
            import Adafruit_GPIO.SPI as SPI
        except ImportError:
            logger.info('Could not import modules to show messages on LED.')
            return

        PIXEL_COUNT = 160

        PIXEL_CLOCK = 11
        PIXEL_DOUT = 19
        pixels = Adafruit_WS2801.WS2801Pixels(PIXEL_COUNT, clk=PIXEL_CLOCK, do=PIXEL_DOUT)

        pixels.clear()
        pixels.show()

        # Set the first third of the pixels red.
        rand = randint(1, 255)
        for i in range(PIXEL_COUNT//3):
            pixels.set_pixel_rgb(i, 255, rand, 0)  # Set the RGB color (0-255) of pixel i.

        # Set the next third of pixels green.
        rand = randint(1, 255)
        for i in range(PIXEL_COUNT//3, PIXEL_COUNT//3*2):
            pixels.set_pixel_rgb(i, rand, 255, 0)

        # Set the last third of pixels blue.
        rand = randint(1, 255)
        for i in range(PIXEL_COUNT//3*2, PIXEL_COUNT):
            pixels.set_pixel_rgb(i, rand, 0, 255)

        pixels.show()
        sleep(3)
        pixels.clear()
