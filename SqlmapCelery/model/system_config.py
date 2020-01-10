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
import logging
import threading
from peewee import *
import warnings
import json
from model.default_value import DEFAULT_TASK_ID
from common.mysql_util import MysqlManage
from model.hunter_model import HunterModel, HunterModelService


class SystemConfig(HunterModel):
    """
    系统设置表，只能有一条记录
    hunter_log_token                HunterLog 平台API
    hunter_api_url                  HunterLog 平台API url，一般是 http://xxxx:8888/api/v1/hunter/  {uuid}
    hunter_log_socket_port          HunterLog Socket服务端口，默认是 7799
    hunter_log_socket_host          HunterLog Socket服务ip
    hunter_log_socket_switch        是否使用HunterLog Socket模块作为poc插件针对无回显操作
    hunter_log_dns_fake_root_domain HunterLog Dns模块 域名
    hunter_log_dns_switch           是否使用HunterLog Socket模块作为poc插件针对无回显操作
    hunter_api_key hunterServer     对外API
    notice_message                  系统通知消息
    
    task_access_private_key         用于生成task表access_key字段值的私钥
    task_access_public_key          用于生成task表access_key字段值的公钥
    
    smtp_host                       smtp主机
    smtp_port                       smtp端口
    sender_email                    通知邮箱名
    sender_password                 通知邮箱名对应密码
    email_content_template          通知邮件模版
    """
    hunter_log_token = TextField(null=True)  # 可以不使用，不使用token无法查看Log记录到的内容，只能看是否存在记录，推荐使用
    hunter_api_url = TextField(null=True)
    hunter_log_socket_port = TextField(null=True)
    hunter_log_socket_host = TextField(null=True)
    hunter_log_socket_switch = BooleanField(default=False)
    hunter_log_dns_fake_root_domain = TextField(null=True)
    hunter_log_dns_switch = BooleanField(default=False)
    hunter_api_key = TextField(null=True)
    notice_message = TextField(null=True)
    # task表access_key
    task_access_private_key = TextField(null=True)
    task_access_public_key = TextField(null=True)

    # 邮件相关，任务结束之后发送邮件通知
    smtp_host = TextField(null=True)
    smtp_port = IntegerField(null=True)
    sender_email = TextField(null=True)
    sender_password = TextField(null=True)
    email_content_template = TextField(null=True)

    class Meta:
        database = MysqlManage.get_database()


class SystemConfigService:
    __system_config_single = None
    _instance_lock = threading.Lock()

    @staticmethod
    def get_fields_by_where(**kwargs):
        """
        To use:
        >>> system_config = SystemConfigService.get_fields_by_where(fields=(SystemConfig.socket_port), where=(SystemConfig.id == 1))
        >>> print(system_config)
        :param kwargs: 
        :return: 
        """
        return HunterModelService.get_fields_by_where(SystemConfig, **kwargs)

    @staticmethod
    def count(**kwargs):
        """
        数据数量
        To use:
        >>> SystemConfigService.count(where=(SystemConfig.id == 1))
        :param kwargs: 
        :return: 
        """
        return HunterModelService.count(SystemConfig, **kwargs)

    @staticmethod
    def update(**kwargs):
        """
        更新操作，更新操作之后，需要对单列进行赋值
        To use:
        >>> SystemConfigService.update(fields=({SystemConfig.hunter_log_token: "777" }))
        :param kwargs: 
        :return: 
        """
        result = HunterModelService.update(SystemConfig, **kwargs)
        SystemConfigService.get_single_instance(True)
        return result

    @staticmethod
    def get_single_instance(refresh=False):
        """
        获取单列
        :param refresh: 
        :return: 
        """
        with SystemConfigService._instance_lock:
            if refresh or SystemConfigService.__system_config_single is None:
                SystemConfigService.__system_config_single = SystemConfigService.get_fields_by_where()[0]
            return SystemConfigService.__system_config_single

    @staticmethod
    def make_access_key(task_id, username, create_time):
        """
        将 其他三个参数组合成 {"task_id":"1", "username":"lilie", "create_time":"2018-12992"} 后用ase加密
        :param private_key: 
        :param task_id: 
        :param username: 
        :param create_time: 
        :return: 
        """
        private_key = SystemConfigService.get_single_instance().task_access_private_key
        clear_data = {"task_id": task_id, "username": username, "create_time": create_time}
        return prpcrypt.get_single_instance(private_key, False).encrypt(json.dumps(clear_data))
