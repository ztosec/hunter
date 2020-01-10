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
MySQL连接池管理
"""
import json
import logging
import traceback
import threading
from peewee import *
from common.log import get_default_logger
from playhouse.pool import PooledMySQLDatabase
from common.config_util import get_system_config


class MysqlManage(object):
    _instance_lock = threading.Lock()

    __database = None

    mysql_logger = get_default_logger()

    @classmethod
    def get_database(cls, refresh=False):
        """
        单例多线程模式获取db对象
        :param refresh: 
        :return: 
        """
        with MysqlManage._instance_lock:
            mysql_config = get_system_config()['mysql']
            if refresh or MysqlManage.__database is None:  # or MysqlManage.__database.is_closed():
                # 老方法
                """MysqlManage.__database = MySQLDatabase(database=mysql_config["database"], host=mysql_config['host'],
                                                       port=int(mysql_config['port']),
                                                       user=mysql_config['user'],
                                                       passwd=mysql_config['password'])
                """
                MysqlManage.__database = PooledMySQLDatabase(database=mysql_config["database"],
                                                             host=mysql_config['host'],
                                                             port=int(mysql_config['port']), user=mysql_config['user'],
                                                             passwd=mysql_config['password'],
                                                             max_connections=mysql_config["max_connections"],
                                                             stale_timeout=mysql_config["stale_timeout"])
            return MysqlManage.__database

    @classmethod
    def close_database(cls, func):
        """关闭连接
        :param cls: 
        :param func: 
        :return: 
        """

        # logger = logging.getLogger('peewee')
        # logger.addHandler(logging.StreamHandler())
        # logger.setLevel(logging.DEBUG)

        def wapper(*args, **kwargs):
            try:
                MysqlManage.get_database().connect()

            except Exception as e:
                pass
            finally:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    MysqlManage.mysql_logger.exception("close_database error")
                    raise e
                finally:
                    MysqlManage.get_database().close()

        return wapper
