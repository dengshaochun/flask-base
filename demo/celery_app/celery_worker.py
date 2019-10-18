#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 10/16/19 7:48 PM
# @Author  : dengsc


import logging
from celery import Celery
from demo import create_app


logger = logging.getLogger(__name__)

celery_app = Celery()
celery_app.config_from_object('demo.celery_app.celeryconfig')
flask_app = create_app()
flask_app.app_context().push()
