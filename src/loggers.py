"""This module provides functions to setup logging for the Flask app.

   Depending on how the application is run the configuration of the
   logging will be set differently. For more information read the
   docs of the specific function.
"""

import logging

__author__ = "Masud Afschar"
__status__ = "Development"

# change logging file here
LOG_FILE = "info.log"
# change log level here
LOG_LEVEL = "INFO"


def setup_gunicorn_logging(app):
    """This is meant to be called if the Flask app is run by Gunicorn.

    The logger will set the handlers of the Flask app logger
    to the Gunicorn logger. The Flask app will have the same
    log level as the Gunicorn logger.

    :param app: the actual Flask app to be logged

    :return: the logger object
    """

    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    return app.logger


def setup_logging(log_level=LOG_LEVEL, log_file=LOG_FILE):
    """This is meant to be called if the Flask app is run by its own.

    It will set up a console log and a produce a log file in the current
    working directory.

    :param log_level: granularity of log messages
    :param log_file: file location to write log messages

    :return: logger object
    """
    logger = logging.getLogger('src')
    logger.setLevel(log_level)

    logger_file_handler = logging.FileHandler(log_file)
    logger_file_handler.setLevel(log_level)
    logger_file_handler.setFormatter(
        logging.Formatter("[%(asctime)s] [%(process)s] [%(levelname)s] - %(name)s: %(message)s",
                          datefmt='%Y-%m-%d %H:%M:%S %z'))

    console_log = logging.StreamHandler()
    console_log.setLevel(log_level)
    console_log.setFormatter(
        logging.Formatter("[%(asctime)s] [%(process)s] [%(levelname)s] - %(name)s: %(message)s",
                          datefmt='%Y-%m-%d %H:%M:%S %z'))
    logger.addHandler(logger_file_handler)
    logger.addHandler(console_log)

    return logger
