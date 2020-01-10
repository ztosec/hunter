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
from peewee import *

from model.default_value import DEFAULT_TASK_ID
from model.hunter_model import HunterModel, HunterModelService
from common.mysql_util import MysqlManage


class UserTask(HunterModel):
    """
    要支持多种功能坚权限，可以根据user表中的任意一个字段坚权，或者主管上级能查看到下级的任务和漏洞详情
    任务映射表，多个用户可以针对对同一个任务进行测试
    迁移语句如下:    
    INSERT INTO usertask('task_id', 'user_id') SELECT t1.id, t2.id FROM task t1 INNER JOIN user t2 ON t1.user_name = t2.user_name
    task_id 任务id
    user_id 用户id
    """
    task_id = IntegerField(null=True)
    user_id = IntegerField(null=True)

    class Meta:
        database = MysqlManage.get_database()


class UserTaskService:
    """
    对task表进行CURD操作
    """

    @staticmethod
    def get_fields_by_where(**kwargs):
        """
        To use:
        >>> user_tasks = UserTaskService.get_fields_by_where(fields=(UserTask.task_id), where=(UserTask.id == 1))
        >>> print(user_tasks)
        :param kwargs: 
        :return: 
        """
        return HunterModelService.get_fields_by_where(UserTask, **kwargs)

    @staticmethod
    def count(**kwargs):
        """
        数据数量
        To use:
        >>> UserTaskService.count(where=(UserTask.id == 1))
        :param kwargs: 
        :return: 
        """
        return HunterModelService.count(UserTask, **kwargs)

    @staticmethod
    def update(**kwargs):
        """
        更新操作，更新操作之后
        To use:
        >>> UserTaskService.update(fields=({UserTask.task_id: 1 }))
        :param kwargs: 
        :return: 
        """
        return HunterModelService.update(UserTask, **kwargs)

    @staticmethod
    def save(**kwargs):
        """
        保存任务信息，用户任务id关联表，一个任务可以分配给多个用户
        To use:
        >>> UserTaskService.save(task_id=1, user_id=3)
        :return: 
        """
        return HunterModelService.save(UserTask, **kwargs)

    @staticmethod
    def remove(**kwargs):
        """
        删除操作
        To use:
         >>> UserTaskService.remove(where=(UserTask.task_id == 1))
        :return: 
        """
        return HunterModelService.remove(UserTask, **kwargs)
