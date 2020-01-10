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
from model.hunter_model import HunterModel, HunterModelService
from common.mysql_util import MysqlManage
from model.default_value import TaskStatus


class Url(HunterModel):
    """
    status: 任务状态(0:等待，1:运行中，2:运行完成)
    origin_data: 数据包完整内容(json格式/mysql5.7支持)，请求源数据
    plugin: 所选中的插件
    start_time: 开始时间，一般是时间
    end_time: 结束时间
    task_id: 对应任务id，可以根据此方便的映射到人员等信息
    task_name:任务名(保留)
    task_id: 任务id
    parser_type: 流量来源，主要是代理，chrome浏览器或者其他方式
    """
    status = IntegerField(default=TaskStatus.NONE)
    origin_data = TextField(null=True)
    plugin = TextField(null=True)
    start_time = DateTimeField(formats='%Y-%m-%d %H:%M:%S', default=datetime.datetime.now)
    end_time = TextField(null=True)
    task_id = IntegerField(null=True)
    classification_url = TextField(null=True)
    classification_data = TextField(null=True)
    parser_type = TextField(null=True)

    class Meta:
        database = MysqlManage.get_database()


class UrlService:
    """
    对Url表进行CURD操作
    """

    @staticmethod
    def get_fields_by_where(**kwargs):
        """
        To use:
        >>> urls = UrlService.get_fields_by_where(fields=(Url.origin_data), where=(Url.task_id == 1))
        >>> print(urls)
        :param kwargs: 
        :return: 
        """
        return HunterModelService.get_fields_by_where(Url, **kwargs)

    @staticmethod
    def count(**kwargs):
        """
        数据数量
        To use:
        >>> UrlService.count(where=(Url.id == 1))
        :param kwargs: 
        :return: 
        """
        return HunterModelService.count(Url, **kwargs)

    @staticmethod
    def update(**kwargs):
        """
        更新操作，更新操作之后
        To use:
        >>> UrlService.update(fields=({Url.plugin: "xxe" }))
        :param kwargs: 
        :return: 
        """
        return HunterModelService.update(Url, **kwargs)

    @staticmethod
    def save(**kwargs):
        """
        保存操作，已经close掉connect
        :param self: 
        :return: 
        """
        return HunterModelService.save(Url, **kwargs)
