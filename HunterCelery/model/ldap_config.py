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


class LdapConfig(HunterModel):
    """
    LDAP 配置，同于定时同步账号到本地数据库，只能有一条记录
    """
    ldap_host = TextField(null=True)
    bind_dn = TextField(null=True)
    bind_dn_password = TextField(null=True)
    base_dn = TextField(null=True)
    search_filter = TextField(null=True)
    user_name_field = TextField(null=True)
    full_name_field = TextField(null=True)
    email_field = TextField(null=True)
    dept_name_field = TextField(null=True)
    mobile_field = TextField(null=True)
    ldap_switch = BooleanField(default=False)

    class Meta:
        database = MysqlManage.get_database()


class LdapConfigService:
    """
    ldap认证配置服务
    """
    __ldap_config_single = None
    _instance_lock = threading.Lock()

    @staticmethod
    def get_fields_by_where(**kwargs):
        """
        To use:
        >>> ldap_config = LdapConfigService.get_fields_by_where(fields=(LdapConfig.ldap_host), where=(LdapConfig.id == 1))
        >>> print(ldap_config)
        :param kwargs: 
        :return: 
        """
        return HunterModelService.get_fields_by_where(LdapConfig, **kwargs)

    @staticmethod
    def count(**kwargs):
        """
        数据数量
        To use:
        >>> LdapConfigService.count(where=(LdapConfig.id == 1))
        :param kwargs: 
        :return: 
        """
        return HunterModelService.count(LdapConfig, **kwargs)

    @staticmethod
    def update(**kwargs):
        """
        更新操作，更新操作之后，需要对单列进行赋值
        To use:
        >>> LdapConfigService.update(fields=({LdapConfig.ldap_host: "777" }))
        :param kwargs: 
        :return: 
        """
        result = HunterModelService.update(LdapConfig, **kwargs)
        LdapConfigService.get_single_instance(True)
        return result

    @staticmethod
    def save(**kwargs):
        """
        保存操作，不做第二次
        To use:
        >>> LdapConfigService.save(ldap_host="ldap://127.0.0.1")
        :param kwargs: 
        :return: 
        """
        return HunterModelService.save(LdapConfig, **kwargs)

    @staticmethod
    def get_single_instance(refresh=False):
        """
        获取单列
        :param refresh: 
        :return: 
        """
        with LdapConfigService._instance_lock:
            if refresh or LdapConfigService.__ldap_config_single is None:
                LdapConfigService.__ldap_config_single = LdapConfigService.get_fields_by_where()[0]
            return LdapConfigService.__ldap_config_single
