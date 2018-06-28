"""Contains various settings for each process of development
"""
from os import getenv
# import os
# basedir = os.path.abspath(os.path.dirname(__file__))
# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'testing.db')
class Config(object):
    """Base class with all the constant config variables"""
    DEBUG = False
    TESTING = False
    SECRET_KEY = getenv('SECRET_KEY')

class TestingConfig(Config):
    """Contains additional config variables required during testing"""
    DEBUG = True
    TESTING = True
    db = getenv('test_db')

class ProductionConfig(Config):
    """Contains additional config variables required during production"""
    DEBUG = True
    TESTING = True
    db = getenv('production_db')