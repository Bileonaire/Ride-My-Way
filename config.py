"""Contains various settings for each process of development
"""
from os import getenv

class Config(object):
    """Base class with all the constant config variables"""
    DEBUG = False
    TESTING = False
    SECRET_KEY = getenv("SECRET_KEY")


class TestingConfig(Config):
    """Contains additional config variables required during testing"""
    DEBUG = True
    TESTING = True


class DevelopmentConfig(Config):
    """Contains additional config variables required during development"""
    DEBUG = True


class ProductionConfig(Config):
    """Contains additional config variables required during production"""
    DEBUG = False
