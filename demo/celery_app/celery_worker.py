#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 10/16/19 7:48 PM
# @Author  : dengsc


import logging
from celery import Celery
from demo import create_app


logger = logging.getLogger(__name__)


flask_app = create_app()
celery_app = Celery()
celery_app.config_from_object('demo.celery_app.celeryconfig')
TaskBase = celery_app.Task


class ContextTask(TaskBase):
    abstract = True

    def __call__(self, *args, **kwargs):
        with flask_app.app_context():
            return TaskBase.__call__(self, *args, **kwargs)


celery_app.Task = ContextTask
