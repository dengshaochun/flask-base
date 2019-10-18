#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 10/16/19 7:49 PM
# @Author  : dengsc


import os
import logging
from demo.utils.common import Alert
from demo.celery_app.celery_worker import ContextTask


logger = logging.getLogger(__name__)


class AlertTask(ContextTask):

    # 任务失败时执行
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        try:
            project_name = os.getenv('PROJECT_NAME')
            message = f'Project: {project_name}, Task id: {task_id}, Exception: {str(einfo)}'
            alert_users = [x.strip() for x in os.getenv('DEFAULT_ALERT_USERS', '').split(',')]
            Alert().alert_users(
                users=alert_users,
                title=f'[{project_name}] Celery Failed [{task_id}]',
                content=message,
                level='critical'
            )
        except Exception as e:
            logging.exception(einfo)
            logging.exception(e)
