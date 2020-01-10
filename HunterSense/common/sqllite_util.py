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
Copyright (c) 2018
"""
import threading
from common import config
from log import logger
from peewee import *
from playhouse.pool import PooledSqliteDatabase


class SqliteManage(object):
    __database = None
    _instance_lock = threading.Lock()
    sql_manage_logger = logger.get_default_logger()

    @classmethod
    def get_database(cls, refresh=False):
        if SqliteManage.__database is None or refresh:
            SqliteManage.__database = PooledSqliteDatabase(config.DB_PATH, max_connections=config.MAX_CONNECTIONS,
                                                           stale_timeout=config.STALE_TIMEOUT,
                                                           check_same_thread=False)
        return SqliteManage.__database

    @classmethod
    def close_database(cls, func):
        """
        关闭连接 see http://www.codersec.net/2018/07/peewee%E8%B8%A9%E5%9D%91%E6%97%A5%E8%AE%B0/
        :param cls: 
        :param func: 
        :return: 
        """

        def wapper(*args, **kwargs):
            try:
                SqliteManage.get_database().connect()
            except Exception as e:
                pass
            finally:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    SqliteManage.sql_manage_logger.exception("close_database error")
                    raise e
                finally:
                    SqliteManage.get_database().close()

        return wapper
