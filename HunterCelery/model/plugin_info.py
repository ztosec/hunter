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
import json
from peewee import *
import datetime

from plugins.base.vuln_enum import PluginSwith, VulnLevel
from model.hunter_model import HunterModel, HunterModelService
from common.mysql_util import MysqlManage


class PluginInfo(HunterModel):
    """
    author: 作者
    plugin_name: 插件名字
    imp_version: 影响版本
    description: 描述信息
    repair: 修复建议
    type: 类型
    chinese_type: 中文类型
    level: 等级
    useable:是否使用插件，默认不禁用
    
    """
    author = TextField(null=True)
    plugin_name = TextField(null=True)
    plugin_tag = TextField(null=True)
    imp_version = TextField(null=True)
    description = TextField(null=True)
    repair = TextField(null=True)
    type = TextField(null=True)
    chinese_type = TextField(null=True)
    level = TextField(null=True)
    useable = IntegerField(default=PluginSwith.ON)

    class Meta:
        database = MysqlManage.get_database()


class PluginInfoService:
    """
    对PluginInfo表进行CURD操作
    """

    @staticmethod
    def get_fields_by_where(**kwargs):
        """
        To use:
        >>> plugin_infos = PluginInfoService.get_fields_by_where(fields=(PluginInfo.plugin_name), where=(PluginInfo.level == VulnLevel.LOW))
        >>> print(plugin_infos)
        :param kwargs: 
        :return: 
        """
        return HunterModelService.get_fields_by_where(PluginInfo, **kwargs)

    @staticmethod
    def count(**kwargs):
        """
        数据数量
        To use:
        >>> PluginInfoService.count(where=(PluginInfo.level == VulnLevel.HIGHT))
        :param kwargs: 
        :return: 
        """
        return HunterModelService.count(PluginInfo, **kwargs)

    @staticmethod
    def update(**kwargs):
        """
        更新操作，更新操作之后
        To use:
        >>> PluginInfoService.update(fields=({PluginInfo.useable: PluginSwith.OFF }))
        :param kwargs: 
        :return: 
        """
        return HunterModelService.update(PluginInfo, **kwargs)

    @staticmethod
    def save(**kwargs):
        """
        保存操作，不做第二次
        To use:
        >>> PluginInfoService.save(plugin_name="cve1222")
        :param kwargs: 
        :return: 
        """
        return HunterModelService.save(PluginInfo, **kwargs)
