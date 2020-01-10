#!/ usr/bin/env
# coding=utf-8
#
# Copyright 2019 ztosec & https://www.zto.com/
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
"""
author: b5mali4
"""
import json
import time
from datetime import datetime
from model.user import UserService, User

TOKENS = list()


def get_current_time():
    """
    获取当前时间
    :return: 
    """
    return time.time()


def encode_b64(number, filter=True):
    """
    :param number: 
    :param filter:  保留原文带000还是去除0000
    :return: 
    """
    number = int(number)
    table = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-_'
    result = []
    temp = number
    if 0 == temp:
        result.append('0')
    else:
        while 0 < temp:
            result.append(table[int(temp % 64)])
            temp /= 64

    b64 = ''.join([x for x in reversed(result)])
    if filter:
        for i in range(0, len(result)):
            if b64[i] != '0':
                break
        b64 = b64[i:]
    return b64


def get_tokens(refresh=False):
    """
    从数据库中获取token，单例模式
    :param refresh: 
    :return: 
    """
    global TOKENS
    if not TOKENS or refresh:
        TOKENS = list()
        users = UserService.get_fields_by_where(fields=(User.token))
        for user in users:
            TOKENS.append(user.token)
    return TOKENS
