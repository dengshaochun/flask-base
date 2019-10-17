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


add_task_parser = reqparse.RequestParser()
add_task_parser.add_argument('a', type=int)
add_task_parser.add_argument('b', type=int)


class AddTaskResource(Resource):

    def post(self):
        """
        submit add task
        :return: <str> task id
        """
        args = add_task_parser.parse_args()
        from demo.celery_app.tasks.examples import add
        result = add.delay(a=args.get('a'), b=args.get('b'))
        return {'task_id': result.id}, 200


class HelloTaskResource(Resource):

    def get(self):
        """
        submit a hello task
        :return: <str> task id
        """
        from demo.celery_app.tasks.examples import hello
        result = hello.delay()
        return {'task_id': result.id}, 200


class TaskDetailResource(Resource):
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
    AddTaskResource,
    '/tasks/func/add/'
)
api.add_resource(
    HelloTaskResource,
    '/tasks/func/hello/'
)
api.add_resource(
    TaskDetailResource,
    '/tasks/<task_id>/'
)
