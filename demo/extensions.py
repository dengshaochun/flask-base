#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 10/16/19 7:29 PM
# @Author  : dengsc


from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s [%(filename)s:%(lineno)d] [%(funcName)s] - %(message)s',
        }
    },
    'handlers': {
        'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})


from flask_sqlalchemy import SQLAlchemy  # noqa
db = SQLAlchemy()

from flask_migrate import Migrate  # noqa
migrate = Migrate()
