"""This module provides the configurations to setup logging for the notifier.
"""

import logging

__author__ = "Masud Afschar"
__status__ = "Development"

# change logging file here
LOG_FILE = "info.log"
# change log level here
LOG_LEVEL = "INFO"


def setup_logging(log_level=LOG_LEVEL, log_file=LOG_FILE):
    """Defines all configurations for logging of the notifier.

    It sets up a console log and a produce a log file in the current
    working directory.

    :param log_level: granularity of log messages
    :param log_file: file location to write log messages
    :return: logger object
    """
    logger = logging.getLogger('notifier')
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
