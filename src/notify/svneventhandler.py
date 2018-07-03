"""This module contains the handler class for events from SVN.

The `SVNEventHandler` class implements all functions for handling events
received from SVN.
"""

from eventhandler import EventHandler


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
            return

        unicornhat.set_pixels(self.icon)
        unicornhat.show()
        signal.pause()


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
