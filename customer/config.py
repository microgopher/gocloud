import os
import tempfile


class BaseConfig(object):
    """ Base configuration from which others
        inherit from: defines available endpoints
    """
    DEBUG = False
    TESTING = False
    DATABASE_URL = 'sqlite://:memory:'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ALGORITHM = "RS256"
    JWT_PUBLIC_KEY = open(".ssh/jwt-key.pub").read()


class DevelopmentConfig(BaseConfig):
    """ Sets config for development """
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' \
        + os.path.join(BASE_DIR, 'customers_dev.sqlite')
    


class TestingConfig(BaseConfig):
    """ Sets config for testing """
    TESTING = True
    JWT_ALGORITHM = 'HS256'
    JWT_SECRET_KEY = "test123"
    DB_FD, DATABASE = tempfile.mkstemp()
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' \
        + os.path.join(DATABASE)


class ProductionConfig(BaseConfig):
    """ Sets config for production """
    TESTING = False
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' \
        + os.path.join(BASE_DIR, 'customers.sqlite')
