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
To use:
"""
import sys
import logging
from model.user import User
from model.request_log import RequestLog
from model.system_set import SystemSetting
from model.request_log_dup import RequestLogDup
from model.user import UserService


def initialize_database(username, password, token):
    """
    初始化数据库结构，主要初始化用户表和系统设置
    :param username: 
    :param password: 
    :param token:
    :return: 
    """
    logger = logging.getLogger('peewee')
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.DEBUG)
    User.create_table()
    User.create(username=username, password=password, token=token)
    RequestLog.create_table()
    RequestLogDup.create_table()
    SystemSetting.create_table()
    SystemSetting.create()


def check_initialization_success():
    """
    检测初始化是否成功
    :return: 
    """
    user = UserService.get_fields_by_where()[0]
    print("username:{},passwor:{},token:{}".format(user.username, user.password, user.token))
    """
    if user[0] > 0:
        print("initialization success")
    else:
        print("initialization fail")
    """


if __name__ == "__main__":
    username = sys.argv[1]
    password = sys.argv[2]
    token = sys.argv[3]
    # print("初始化账号:{},密码:{},token:{}".format(username, password, token))
    initialize_database(username, password, token)
    check_initialization_success()
