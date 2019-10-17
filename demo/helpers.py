#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 10/16/19 7:30 PM
# @Author  : dengsc

import functools
from flask import request, url_for, current_app
from sqlalchemy import desc


def paginate_and_filter(current_model=None):
    """
    query filter and paginate
    :param current_model: <object> current query model
    :return: response
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            page = request.args.get('page', 1, int)
            page_size = min(
                request.args.get('page_size', current_app.config['PAGE_SIZE'], int),
                current_app.config['MAX_PAGE_SIZE']
            )

            # default query
            query = func(*args, **kwargs)

            request_args = request.args.to_dict()

            # pop page args
            request_args.pop('page', 1)
            request_args.pop('page_size', 1)

            # model filters
            if current_model:
                model_columns = [x.key for x in current_model.__table__.columns]
                model_like_columns = [f'{x}__like' for x in model_columns]
                for attr, value in request_args.items():
                    if attr in model_columns:
                        query = query.filter(getattr(current_model, attr) == value)
                    elif attr in model_like_columns:
                        attr = attr[:-6]
                        query = query.filter(getattr(current_model, attr).like(f'%%{value}%%'))
                    elif attr == 'order_by':
                        if value.startswith('-'):
                            query = query.order_by(desc(value[1:]))
                        else:
                            query = query.order_by(value)

            # model paginate
            p = query.paginate(page, page_size)

            meta = {
                'page': page,
                'page_size': page_size,
                'total': p.total,
                'pages': p.pages,
            }

            links = {}
            if p.has_next:
                links['next'] = url_for(
                    request.endpoint, page=p.next_num,
                    page_size=page_size, **kwargs, **request_args
                )
            if p.has_prev:
                links['prev'] = url_for(
                    request.endpoint, page=p.prev_num,
                    page_size=page_size, **kwargs, **request_args
                )
            links['first'] = url_for(
                request.endpoint, page=1,
                page_size=page_size, **kwargs, **request_args
            )
            links['last'] = url_for(
                request.endpoint, page=p.pages,
                page_size=page_size, **kwargs, **request_args
            )

            meta['links'] = links
            result = {
                'items': p.items,
                'meta': meta
            }

            return result, 200
        return wrapped
    return decorator
