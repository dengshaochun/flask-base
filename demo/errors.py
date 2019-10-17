#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 10/17/19 9:46 AM
# @Author  : dengsc


from flask import jsonify


def _response(status_code, error, message):
    response = jsonify({'error': error, 'detail': message})
    response.status_code = status_code
    return response


def forbidden(message=None):
    return _response(403, 'Forbidden', message)


def unauthorized(message=None):
    return _response(401, 'Unauthorized', message)


def bad_request(message=None):
    return _response(400, 'Bad Request', message)


def not_found(message=None):
    return _response(404, 'Not Found', message)


def not_allowed(message=None):
    return _response(405, 'Method Not Allowed', message)
