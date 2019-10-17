#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 10/16/19 7:47 PM
# @Author  : dengsc


from celery.schedules import crontab


CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
BROKER_URL = 'redis://localhost:6379/0'
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERYD_CONCURRENCY = 20  # 并发worker数
CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24 * 7  # celery任务执行结果的超时时间
CELERYD_MAX_TASKS_PER_CHILD = 20  # 每个worker执行了多少任务就会死掉
CELERY_TIMEZONE = 'Asia/Shanghai'

CELERY_IMPORTS = [
    'demo.celery_app.tasks.examples',
]

CELERYBEAT_SCHEDULE = {
    'test_task': {
        'task': 'demo.celery_app.tasks.examples.hello',
        'schedule': crontab(minute='*/2')
    }
}
