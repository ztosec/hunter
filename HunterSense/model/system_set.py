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
import time
import datetime
from peewee import *
from common import config
from .base_model import BaseModel
from .base_model import BaseModelService
from common.sqllite_util import SqliteManage


class SystemSetting(BaseModel):
    """
    To Create Table:
    >>> if __name__ == "__main__":
    >>>     SystemSetting.create_table()

    socket_port : 监听端口
    socket_switch: socket服务开关
    fake_root_domain: 表示访问任何以其结尾的域名都将会被记录
    ns1domain: 一个域名，配置A记录指向一个DNS服务器，该DNS服务器记录所有访问FAKE_ROOT_DOMAIN结尾的域名记录
    ns2domain: 一个域名，配置A记录指向一个DNS服务器，该DNS服务器记录所有访问FAKE_ROOT_DOMAIN结尾的域名记录
    server_ip: DNS服务器ip，NS1_DOMAIN和NS2_DOMAIN配置A记录指向的IP，即你的外网IP
    dns_switch: dns服务开启开关
    """
    socket_port = IntegerField(default=config.SERVER_SOCKET_PORT)
    socket_switch = BooleanField(default=False)
    fake_root_domain = TextField(default=config.FAKE_ROOT_DOMAIN)
    ns1domain = TextField(default=config.NS1_DOMAIN)
    ns2domain = TextField(default=config.NS2_DOMAIN)
    server_ip = TextField(default=config.SERVER_IP)
    dns_switch = BooleanField(default=False)

    class Meta:
        database = SqliteManage.get_database()


class SystemSettingService:
    @staticmethod
    def get_fields_by_where(**kwargs):
        """
        To use:
        >>> system_settings = SystemSettingService.get_fields_by_where(fields=(SystemSetting.socket_port), where=(SystemSetting.server_ip == '127.0.0.1'))
        >>> print(system_settings)
        :param kwargs: 
        :return: 
        """
        return BaseModelService.get_fields_by_where(SystemSetting, **kwargs)

    @staticmethod
    def remove(**kwargs):
        """
        数据库删除操作
        To use:
        >>> SystemSettingService.remove(where=(SystemSetting.server_ip == '127.0.0.1'))
        :param kwargs: 
        :return: 
        """
        return BaseModelService.remove(SystemSetting, **kwargs)

    @staticmethod
    def count(**kwargs):
        """
        数据数量
        To use:
        >>> SystemSettingService.count(where=(SystemSetting.server_ip == '127.0.0.1'))
        :param kwargs: 
        :return: 
        """
        return BaseModelService.count(SystemSetting, **kwargs)

    @staticmethod
    def update(**kwargs):
        """
        更新操作
        To use:
        >>> SystemSettingService.update(fields=({SystemSetting.socket_port: "7998" }))
        :param kwargs: 
        :return: 
        """
        return BaseModelService.update(SystemSetting, **kwargs)

    @staticmethod
    def save(**kwargs):
        """
        更新操作
        To use:
        >>> SystemSettingService.save(fake_root_domain="2333.xx.com")
        :param kwargs: 
        :return: 
        """
        return BaseModelService.save(SystemSetting, **kwargs)
