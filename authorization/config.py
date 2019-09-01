import os
import tempfile


class BaseConfig(object):
    """ Base configuration from which others
        inherit from: defines available endpoints
    """
    DEBUG = False
    TESTING = False
    DATABASE_URL = 'sqlite://:memory:'
    SECRET_KEY = 'secret'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'jwt-secret-string'
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']


class DevelopmentConfig(BaseConfig):
    """ Sets config for development """
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' \
        + os.path.join(BASE_DIR, 'authorization_dev.sqlite')
    


class TestingConfig(BaseConfig):
    """ Sets config for testing """
    TESTING = True
    DB_FD, DATABASE = tempfile.mkstemp()
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' \
        + os.path.join(DATABASE)


class ProductionConfig(BaseConfig):
    """ Sets config for production """
    TESTING = False
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' \
        + os.path.join(BASE_DIR, 'authorization.sqlite')
