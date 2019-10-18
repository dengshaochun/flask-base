#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 10/16/19 7:45 PM
# @Author  : dengsc


import os
import logging
import datetime
import requests
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
from pytz import timezone

logger = logging.getLogger(__name__)


class RequestApi:

    def __init__(self, host, port, username=None, password=None, use_tls=False, version=1, headers=None):
        self._version = version
        self._host = host
        self._port = port
        self.protocol = use_tls and 'https' or 'http'
        self.api_url = '{0}://{1}:{2}/api/v{3}'.format(self.protocol, self._host, self._port, self._version)
        if username and password:
            self.auth = (username, password)
        else:
            self.auth = None
        self.headers = headers if headers else {'Content-Type': 'application/json'}

    def _send_requests(self, action, resource_url, data):
        _post_args = {
            'url': '{0}/{1}'.format(self.api_url, resource_url),
            'json': data,
            'headers': self.headers
        }
        if self.auth:
            _post_args['auth'] = self.auth

        if action == 'post':
            response = requests.post(**_post_args)
        elif action == 'delete':
            _post_args.pop('json', None)
            response = requests.delete(**_post_args)
        elif action == 'put':
            response = requests.put(**_post_args)
        elif action == 'patch':
            response = requests.patch(**_post_args)
        else:
            _post_args.pop('json', None)
            response = requests.get(**_post_args, params=data)
        logger.debug('Response: {0} {1}'.format(response.url, response.status_code))
        return response

    def create(self, resource_url, data):
        return self._send_requests('post', resource_url, data)

    def delete(self, resource_url):
        return self._send_requests('delete', resource_url, None)

    def update(self, resource_url, data):
        return self._send_requests('put', resource_url, data)

    def retrieve(self, resource_url, params=None):
        return self._send_requests('get', resource_url, params)


class Alert:

    def __init__(self):
        self.group_url = os.getenv('ALERT_GROUP_URL', None)
        self.users_url = os.getenv('ALERT_USERS_URL', None)
        self.cst_tz = timezone(os.getenv('TIMEZONE', 'Asia/Shanghai'))
        self.level = {
            'info': 1,
            'major': 4,
            'critical': 3,
            'recover': 1
        }

        if not self.group_url or not self.users_url:
            raise Exception('Alert url must be set.')

    def get_timed_message(self, message):
        return f'{message} ,Created at: {datetime.datetime.now().astimezone(self.cst_tz)}'

    def alert_group(self, code, content, labels):
        data = {
            'code': code,
            'desc': self.get_timed_message(content),
            'labels': labels
        }
        r = requests.post(url=self.group_url, json=data)
        return r.json()

    def alert_users(self, users, title, content, level):

        if level not in self.level:
            raise Exception(f'Alert level must in {self.level.keys()}, current input {level}!')

        channels = [x.strip() for x in os.getenv('DEFAULT_ALERT_CHANNELS', '').split(',')]
        data = {
            'receivers': users,
            'channels': channels,
            'title': title,
            'content': self.get_timed_message(content),
            'config': {
                'wechat': {
                    'app_id': self.level.get(level)
                }
            }
        }

        logger.debug(data)
        r = requests.post(url=self.users_url, json=data)
        logger.debug(r.content)
        return r.json()


class PrpCrypt(object):

    def __init__(self, key=os.getenv('AES_SECRET_KEY')):
        self.length = 16
        self.coding = 'utf-8'
        self.key = self.modify_length(key).encode(self.coding)
        self.mode = AES.MODE_CBC

    def modify_length(self, value):
        count = len(value)
        if count < self.length:
            add = (self.length - count)
            value = value + ('\0' * add)
        elif count > self.length:
            add = (self.length - (count % self.length))
            value = value + ('\0' * add)

        return value

    def encrypt(self, text):
        text = self.modify_length(text).encode(self.coding)
        aes = AES.new(self.key, self.mode, b'0000000000000000')
        return bytes.decode(b2a_hex(aes.encrypt(text)))

    def decrypt(self, text):
        aes = AES.new(self.key, self.mode, b'0000000000000000')
        plain_text = aes.decrypt(a2b_hex(bytes(text, encoding=self.coding)))
        # 解密后，去掉补足的空格用strip() 去掉
        return bytes.decode(plain_text).rstrip('\0')
