
import os
import simpleaudio as audio


class EventHandler:

    def __init__(self, event_type):
        self.event_type = event_type

    @staticmethod
    def play_music(**kwargs):
        path = os.path.dirname(os.path.abspath(__file__))
        file = "morse.wav"

        wave_obj = audio.WaveObject.from_wave_file(path + "/" + file)
        play_obj = wave_obj.play()
        play_obj.wait_done()


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
    handler = EventHandler(event)
    handler.play_music()
