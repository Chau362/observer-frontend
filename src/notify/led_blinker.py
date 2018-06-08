# import RPi.GPIO as GPIO
# import time
# import logging
#
# logger = logging.getLogger('src.notify')
#
#
# def Blink(num_times,speed):
#     GPIO.setmode(GPIO.BOARD)
#     GPIO.setup(7, GPIO.OUT)
#     GPIO.setup(11, GPIO.OUT)
#
#     for i in range(0,num_times):
#         GPIO.output(7,True)
#         time.sleep(speed)
#         GPIO.output(7,False)
#         time.sleep(speed)
#         GPIO.output(11, True)
#         time.sleep(speed)
#         GPIO.output(11, False)
#         time.sleep(speed)
#
#     GPIO.cleanup()
