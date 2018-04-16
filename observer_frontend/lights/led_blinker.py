import RPi.GPIO as GPIO ## Import GPIO library
import time ## Import 'time' library. Allows us to use 'sleep'
import logging

# logging setup
logger = logging.getLogger(__name__)
logger.setLevel('INFO')
logger_file_handler = logging.FileHandler('info.log')
logger_file_handler.setLevel('INFO')
logger_file_handler.setFormatter(
    logging.Formatter("%(asctime)s - [%(levelname)s] - %(name)s: %(message)s",
                      datefmt='%Y-%m-%d %H:%M:%S'))
console_log = logging.StreamHandler()
console_log.setLevel('INFO')
console_log.setFormatter(
    logging.Formatter("%(asctime)s - [%(levelname)s] - %(name)s: %(message)s",
                      datefmt='%Y-%m-%d %H:%M:%S'))
logger.addHandler(logger_file_handler)
logger.addHandler(console_log)


def Blink(numTimes,speed):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(7, GPIO.OUT)
    GPIO.setup(11, GPIO.OUT)

    for i in range(0,numTimes):
        GPIO.output(7,True)
        time.sleep(speed)
        GPIO.output(7,False)
        time.sleep(speed)
        GPIO.output(11, True)
        time.sleep(speed)
        GPIO.output(11, False)
        time.sleep(speed)

    GPIO.cleanup()

