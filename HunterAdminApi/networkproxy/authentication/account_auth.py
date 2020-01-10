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
>>> sq = Square(3)
>>> sq.area
9
Simple Postgres pool example code:

    # Use the special postgresql extensions.
    from playhouse.pool import PooledPostgresqlExtDatabase

    db = PooledPostgresqlExtDatabase(
        'my_app',
        max_connections=32,
        stale_timeout=300,  # 5 minutes.
        user='postgres')

    class BaseModel(Model):
        class Meta:
            database = db
"""
import json
import requests
from common.http_util import HttpMethod
from common.http_util import ContentType
from common.http_util import StatusCode
from common import log

logger = log.get_default_logger()


class NetWorkProxyAccountAuth:
    """
    网络代理LDAP认证模式
    """

    @staticmethod
    def auth_login_logic(username, password):
        """
        访问同主机8888端口
        :return: 
        """
        try:
            req = requests.post(url="http://127.0.0.1:8888/api/v1/account/login/",
                                json={"user_name": username, "pass_word": password})
            response_data = req.json()
            if response_data and "status" in response_data and response_data["status"] == StatusCode.HTTP_OK:
                return True
            return False
        except Exception as e:
            if isinstance(e, requests.exceptions.ConnectionError):
                logger.warn("代理需要使用HunterServer服务鉴权，请开始HunterServer Api")
            else:
                logger.exception("NetWorkProxyAccountAuth=>auth_login_logic raise error")