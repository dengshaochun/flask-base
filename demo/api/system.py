#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 10/18/19 4:43 PM
# @Author  : dengsc


import logging
from demo.api import api
from flask_restful import Resource
from flask import current_app


logger = logging.getLogger(__name__)


class URLResource(Resource):

    def get(self):
        """
        list all route
        :return:
        """
        url_map = []
        for route in current_app.url_map.iter_rules():
            url_map.append(
                {
                    'route': str(route),
                    'methods': ','.join(route.methods)
                }
            )
        return {'url_map': sorted(url_map, key=lambda d: d.get('route'))}, 200


api.add_resource(
    URLResource,
    '/'
)
