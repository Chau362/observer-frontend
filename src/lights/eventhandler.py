
import os
import simpleaudio as audio


def play(**kwargs):
    path = os.path.dirname(os.path.abspath(__file__))
    file = "morse.wav"

    wave_obj = audio.WaveObject.from_wave_file(path + "/" + file)
    play_obj = wave_obj.play()
    play_obj.wait_done()
