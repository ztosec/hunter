#!/ usr/bin/env
# coding=utf-8
#
# Copyright 2019 ztosec & https://sec.zto.com/
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
初始化数据库中的数据，包含插件信息
>>> python init_tables.py

"""
import sys
import subprocess
import pymysql
from common.mysql_util import MysqlManage
from model.url import Url
from model.task import Task
from model.user import User
from model.user_task import UserTask
from api.service.redis_service import RedisService
from model.plugin_info import PluginInfo
from model.vulnerability import Vulnerability
from model.user import User, UserService
from model.system_config import SystemConfig, SystemConfigService
from common.plugins_util import load_default_checkers
from model.plugin_info import PluginInfo, PluginInfoService
from model.ldap_config import LdapConfig, LdapConfigService
from model.network_proxy import NetWorkProxyConfig, NetWorkProxyConfigService


def create_indexs():
    """
    建立索引
    :return: 
    """
    db_cursor = MysqlManage.get_database().cursor()
    create_index(db_cursor=db_cursor, sql="create index index_task_id on url (task_id) ;")
    create_index(db_cursor=db_cursor, sql="create index index_task_id on vulnerability (task_id) ;")
    create_index(db_cursor=db_cursor, sql="create index index_task_id on usertask (task_id) ;")
    create_index(db_cursor=db_cursor, sql="create index index_user_id on usertask (user_id) ;")


def create_index(db_cursor, sql):
    try:
        db_cursor.execute(sql)
    except Exception as e:
        if isinstance(e, pymysql.err.InternalError) and "Duplicate key name" in str(e):
            pass


def create_tables():
    """
    初始化表结构
    :return: 
    """
    Url.create_table()
    Task.create_table()
    User.create_table()
    UserTask.create_table()
    PluginInfo.create_table()
    Vulnerability.create_table()
    SystemConfig.create_table()
    PluginInfo.create_table()
    LdapConfig.create_table()
    NetWorkProxyConfig.create_table()


def create_admin_user():
    """
    新建管理账户
    :return: 
    """
    if UserService.count(where=(User.user_name == "hunter")) <= 0:
        User.create(user_name="hunter", pass_word="hunter", full_name="hunter管理员", role=4)


def init_data():
    """
    根据运行模式填充不同的数据，主要是认证KEY不同，注意task_access_private_key和task_access_public_key必须为16位

    :param model: 
    :return: 
    """
    if SystemConfigService.count() <= 0:
        SystemConfig.create(hunter_log_token="hunter-log-token",
                            hunter_api_url="http://hunter_sense_host:8837/api/v1/hunter/",
                            hunter_log_socket_port="7799", hunter_log_dns_fake_root_domain="xxx.xx.com",
                            hunter_log_socket_host="hunter_sense_host", hunter_api_key="hunter_api",
                            task_access_private_key="private.key12345",
                            task_access_public_key="public.key123456", smtp_host="smtp.xxx.com",
                            smtp_port="465", sender_email="warn@xx",
                            sender_password="123456", hunter_log_socket_switch=True)
    if LdapConfigService.count() <= 0:
        LdapConfigService.save(ldap_host="ldap://ldap.xx.com:389", bind_dn="",
                               bind_dn_password="", base_dn="",
                               search_filter="",
                               user_name_field="", full_name_field="displayName",
                               email_field="mail", mobile_field="mobile")
    if NetWorkProxyConfigService.count() <= 0:
        NetWorkProxyConfigService.save(ca_country_name="CN", ca_province="shanghai", ca_locality_name="shanghai",
                                       ca_organization_name="ZtoSec",
                                       ca_organizational_unit_name="ZtoSec Technology Co., Ltd",
                                       ca_common_name="HunterProxy",
                                       white_host_list="127.0.0.1:3000,sec.zto.com,127.0.0.1:15672")
    init_plugin_info()
    create_admin_user()


def init_plugin_info():
    """
    初始化插件信息到数据库中
    :return: 
    """
    # 初始化redis配置信息
    RedisService.init_plugin_config()
    for checker_name, checker_instance in load_default_checkers().items():
        if PluginInfoService.count(where=(PluginInfo.plugin_name == checker_name)) == 0:
            PluginInfoService.save(author=checker_instance.info["author"], plugin_name=checker_instance.info["name"],
                                   plugin_tag=checker_instance.info["tag"],
                                   imp_version=checker_instance.info["imp_version"],
                                   description=checker_instance.info["description"],
                                   repair=checker_instance.info["repair"],
                                   type=checker_instance.info["type"]["fullname"],
                                   chinese_type=checker_instance.info["type"]["fullchinesename"],
                                   level=checker_instance.info["type"]["level"], )


if __name__ == "__main__":
    try:
        create_tables()
        init_data()
        create_indexs()
        print("success")
    except Exception as e:
        print(e)
        print("fail")
