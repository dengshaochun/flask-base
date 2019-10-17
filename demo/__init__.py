#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 10/16/19 7:29 PM
# @Author  : dengsc


import os
from flask import Flask
from demo.settings import ProdConfig, DevConfig
from demo.extensions import (
    db,
    migrate
)
from demo.api import api_blueprint

if os.getenv('FLASK_ENV') == 'prod':
    DefaultConfig = ProdConfig
else:
    DefaultConfig = DevConfig


def create_app(config_object=DefaultConfig):
    """
    An application factory, as explained here:
        http://flask.pocoo.org/docs/patterns/appfactories/
    :param config_object:
    :return: config_object: The configuration object to use.
    """
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    return app


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)


def register_blueprints(app):
    app.register_blueprint(api_blueprint)
