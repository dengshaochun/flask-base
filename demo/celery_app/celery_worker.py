#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 10/16/19 7:48 PM
# @Author  : dengsc


from celery import Celery
from demo import create_app


def create_celery(app):
    _celery = Celery()
    _celery.config_from_object('demo.celery_app.celeryconfig')

    TaskBase = _celery.Task  # noqa

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    _celery.Task = ContextTask
    return _celery


flask_app = create_app()
celery_app = create_celery(flask_app)
