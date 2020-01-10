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
import threading
from peewee import *
from common.mysql_util import MysqlManage
from model.hunter_model import HunterModel, HunterModelService


class NetWorkProxyConfig(HunterModel):
    """
    代理证书相关设置
    """
    # 代理证书相关设置
    ca_country_name = TextField(null=True)
    ca_province = TextField(null=True)
    ca_locality_name = TextField(null=True)
    ca_organization_name = TextField(null=True)
    ca_organizational_unit_name = TextField(null=True)
    ca_common_name = TextField(null=True)
    # 认证白名单
    white_host_list = TextField(null=True)

    # 是否启动LDAP认证，是否启用基础账号密码认证
    ldap_auth_switch = BooleanField(default=False)
    account_auth_switch = BooleanField(default=True)

    # 代理开关
    switch = BooleanField(default=True)

    class Meta:
        database = MysqlManage.get_database()


class NetWorkProxyConfigService:
    """
    代理证书相关设置
    """
    __cacert_config_single = None
    _instance_lock = threading.Lock()

    @staticmethod
    def get_fields_by_where(**kwargs):
        """
        To use:
        >>> proxy_config = NetWorkProxyConfigService.get_fields_by_where(fields=(NetWorkProxyConfig.ca_country_name), where=(NetWorkProxyConfig.id == 1))
        >>> print(ca_config)
        :param kwargs: 
        :return: 
        """
        return HunterModelService.get_fields_by_where(NetWorkProxyConfig, **kwargs)

    @staticmethod
    def count(**kwargs):
        """
        数据数量
        To use:
        >>> NetWorkProxyConfigService.count(where=(NetWorkProxyConfig.id == 1))
        :param kwargs: 
        :return: 
        """
        return HunterModelService.count(NetWorkProxyConfig, **kwargs)

    @staticmethod
    def update(**kwargs):
        """
        更新操作，更新操作之后，需要对单列进行赋值
        To use:
        >>> NetWorkProxyConfigService.update(fields=({NetWorkProxyConfig.ca_common_name: "HunterProxy" }))
        :param kwargs: 
        :return: 
        """
        result = HunterModelService.update(NetWorkProxyConfig, **kwargs)
        NetWorkProxyConfigService.get_single_instance(True)
        return result

    @staticmethod
    def save(**kwargs):
        """
        保存操作，不做第二次
        To use:
        >>> CaCertConfigService.save(ca_country_name="ldap://127.0.0.1")
        :param kwargs: 
        :return: 
        """
        return HunterModelService.save(NetWorkProxyConfig, **kwargs)

    @staticmethod
    def get_single_instance(refresh=False):
        """
        获取单列
        :param refresh: 
        :return: 
        """
        with NetWorkProxyConfigService._instance_lock:
            if refresh or NetWorkProxyConfigService.__cacert_config_single is None:
                NetWorkProxyConfigService.__cacert_config_single = NetWorkProxyConfigService.get_fields_by_where()[0]
            return NetWorkProxyConfigService.__cacert_config_single

    @staticmethod
    def is_white_hosts(host):
        """
        是否为白名单列表中的HOST
        :param host: 
        :return: 
        """
        proxy_config_single = NetWorkProxyConfigService.get_single_instance()
        if proxy_config_single.white_host_list and host in proxy_config_single.white_host_list.split(","):
            return True
        return False
