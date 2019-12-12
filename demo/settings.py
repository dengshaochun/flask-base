#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 10/16/19 7:31 PM
# @Author  : dengsc

import os
from dotenv import load_dotenv, find_dotenv


class Config(object):
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    load_dotenv(find_dotenv())
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    SECRET_KEY = os.getenv('SECRET_KEY', 'you will never get *&123')

    # sqlalchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True

    # paginate
    PAGE_SIZE = 10
    MAX_PAGE_SIZE = 100

    ERROR_404_HELP = False


class ProdConfig(Config):
    """Production configuration."""
    ENV = 'prod'
    DEBUG = False
    SQLALCHEMY_ECHO = False
    # DB URL variable set by heroku
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '')


class DevConfig(Config):
    """Development configuration."""
    ENV = 'dev'
    DEBUG = True
    DB_NAME = 'dev.sqlite'
    DB_PATH = os.path.join(Config.PROJECT_ROOT, DB_NAME)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(DB_PATH)


class TestConfig(Config):
    """Test configuration."""
    ENV = 'test'
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
