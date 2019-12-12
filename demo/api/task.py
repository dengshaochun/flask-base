#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 10/16/19 8:14 PM
# @Author  : dengsc


import logging
from demo.api import api
from celery import Celery
from celery.result import AsyncResult
from flask_restful import Resource, reqparse

import demo.errors as errors


logger = logging.getLogger(__name__)


execute_task_parser = reqparse.RequestParser()
execute_task_parser.add_argument('task_name', type=str, required=True)
execute_task_parser.add_argument('task_args', type=list, location='json')
execute_task_parser.add_argument('task_kwargs', type=dict, location='json')


class TaskResource(Resource):

    def get(self, task_name):
        from demo.celery_app.tasks import celery_app
        task_obj = celery_app.tasks.get(task_name)
        return {'name': task_name, 'desc': task_obj.__doc__}, 200


class TaskCollectionResource(Resource):

    def get(self):
        from demo.celery_app.tasks import celery_app
        tasks = [x for x in celery_app.tasks.keys()]
        return {'tasks': tasks}, 200

    def post(self):
        """
        submit a task
        """
        args = execute_task_parser.parse_args()
        from demo.celery_app.tasks import celery_app
        current_task = celery_app.tasks.get(args.get('task_name'))
        task_args = args.get('task_args') if args.get('task_args') else ()
        task_kwargs = args.get('task_kwargs') if args.get('task_kwargs') else {}
        result = current_task.delay(*task_args, **task_kwargs)
        return {'task_id': result.id}, 200


class TaskResultResource(Resource):
    """
    get celery task status
    """

    def get(self, task_id):
        from demo.celery_app.celeryconfig import CELERY_RESULT_BACKEND
        app = Celery(backend=CELERY_RESULT_BACKEND)
        result = AsyncResult(id=task_id, app=app)
        if result:
            failed = not result.successful() if result.date_done else None
            response_data = {
                'task_id': result.task_id,
                'status': result.status,
                'failed': failed,
                'date_done': result.date_done,
                'result': str(result.result)
            }
            return response_data, 200
        else:
            return errors.not_found(message=f'Task {task_id} not found.')


api.add_resource(
    TaskResource,
    '/tasks/funcs/<task_name>/'
)
api.add_resource(
    TaskCollectionResource,
    '/tasks/funcs/'
)
api.add_resource(
    TaskResultResource,
    '/tasks/<task_id>/'
)
