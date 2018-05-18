"""This module provides configurations for the Flask app.

Classes and inheritance are used for configuration. The variables are
passed through an `from_object()` call.
"""

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """Template class for Flask configuration.

    These settings are the default values when in Production mode.
    """

    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = "SECRET_KEY"
    WTF_CSRF_SECRET_KEY = "SUPER_SECRET_KEY"


class ProductionConfig(Config):
    """Class providing all variables when in Production mode.
    """

    DEBUG = False


class StagingConfig(Config):
    """Class providing all variables when in Staging mode.
    """

    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    """Class providing all variables when in Development mode.
    """

    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    """Class providing all variables when in Testing mode.
    """

    WTF_CSRF_ENABLED = False
    CSRF_ENABLED = False
    TESTING = True
