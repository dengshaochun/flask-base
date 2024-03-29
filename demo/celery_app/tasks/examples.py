#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 10/16/19 7:50 PM
# @Author  : dengsc


import logging

from demo.celery_app.celery_worker import celery_app
from demo.celery_app.custom_task import AlertTask

logger = logging.getLogger(__name__)


@celery_app.task(base=AlertTask)
def hello():
    """
    test hello
    :return: <str> hello
    """
    return 'hello'


@celery_app.task(base=AlertTask)
def test_exception():
    """
    test task failed
    :return: None
    """
    raise Exception('test exception')


@celery_app.task(base=AlertTask)
def add(a, b):
    """
    return a + b
    :param a: <int> a
    :param b: <b> b
    :return: <int> a + b
    """
    return a + b
