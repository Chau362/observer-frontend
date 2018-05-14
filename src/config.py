import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """Template class for Flask configuration.
    """
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = "SECRET_KEY"
    WTF_CSRF_SECRET_KEY = "SUPER_SECRET_KEY"


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    WTF_CSRF_ENABLED = False
    CSRF_ENABLED = False
    TESTING = True
