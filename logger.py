
import logging

from logging import FileHandler
from logging import Formatter

LOG_FORMAT = (
    "%(asctime)s - [%(levelname)s] - %(name)s: %(message)s")
LOG_LEVEL = logging.INFO
LOG_FILE = "info.log"

# Logging setup
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(asctime)s - [%(levelname)s] - %(name)s: %(message)s'
        },
        'debug': {
            'format': '%(asctime)s - [%(levelname)s] - %(name)s: %(message)s in %(pathname)s %(lineno)d'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'info_file_handler': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'info.log',
            'formatter': 'simple',
            'encoding': 'utf8'
        },
        'error_file_handler': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'info.log',
            'formatter': 'simple',
            'encoding': 'utf8'
        }
    },
    'loggers': {
        'root': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'observer_frontend': {
            'handlers': ['console', 'info_file_handler'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}


# user logger
request_logger = logging.getLogger("request_maker")
request_logger.setLevel(LOG_LEVEL)
request_logger_file_handler = FileHandler(LOG_FILE)
request_logger_file_handler.setLevel(LOG_LEVEL)
request_logger_file_handler.setFormatter(Formatter(LOG_FORMAT))
request_logger.addHandler(request_logger_file_handler)