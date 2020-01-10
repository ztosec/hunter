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
import redis
import threading

from common.config_util import get_system_config


class RedisManage(object):
    """
    redis 管理器
    """
    _instance_lock = threading.Lock()

    __redis_client = None

    @classmethod
    def get_redis_client(cls):
        """
        获得redis client,使用redis连接池
        :return: 
        """
        redis_client = redis.Redis(connection_pool=RedisManage.get_redis_pool())
        return redis_client

    @staticmethod
    def initialized():
        return hasattr(RedisManage, "__redis_pool") and RedisManage.__redis_pool is not None

    @classmethod
    def get_redis_pool(cls):
        """
        获取redis连接池
        :return: 
        """
        redis_config = get_system_config()["redis"]
        redis_host = redis_config["host"]
        redis_port = redis_config["port"]
        redis_password = redis_config["password"]
        max_connections = redis_config["max_connections"]
        if not RedisManage.initialized():
            with RedisManage._instance_lock:
                if not RedisManage.initialized():
                    RedisManage.__redis_pool = redis.ConnectionPool(host=redis_host, port=redis_port,
                                                                    password=redis_password,
                                                                    decode_responses=True,
                                                                    max_connections=max_connections)
        return RedisManage.__redis_pool
