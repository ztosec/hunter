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

from model.task import Task
from model.default_value import Role
from model.hunter_model import HunterModel, HunterModelService
from common.mysql_util import MysqlManage


class User(HunterModel):
    """
    用户表，    用于用户管理，可以从ldap或者其他认证方式同步数据过来
    open_id 表示sso中的openid，只有sso单点登录才有
    user_name 表示用户名，记住一定要唯一不重复
    pass_word 密码，只有在默认认证方式才需要
    full_name 表示完整的用户名，中文名
    email    用户邮箱，用户默认邮箱，任务结束之后发送的邮箱以task表中的receivers_email为主
    dept_name 部门名称
    role 表示用户权限，是否为管理员，详情可见Role
    recent_operation_time 最近一次操作时间，包含关闭开启任务等等
    user_info 详细的用户信息，可以自己补充
    mobile_phone 手机号码
    """
    open_id = TextField(null=True)
    user_name = TextField(null=True)
    pass_word = TextField(null=True)
    full_name = TextField(null=True)
    email = TextField(null=True)
    dept_name = TextField(null=True)
    role = IntegerField(default=Role.USER)
    recent_operation_time = DateTimeField(null=True)
    user_info = TextField(null=True)
    mobile_phone = TextField(null=True)

    class Meta:
        database = MysqlManage.get_database()


class UserService:
    """
    对Url表进行CURD操作
    """

    @staticmethod
    def get_fields_by_where(**kwargs):
        """
        To use:
        >>> users = UserService.get_fields_by_where(fields=(User.full_name), where=(User.mobile_phone == "122222"))
        >>> print(users)
        :param kwargs: 
        :return: 
        """
        return HunterModelService.get_fields_by_where(User, **kwargs)

    @staticmethod
    def count(**kwargs):
        """
        数据数量
        To use:
        >>> UserService.count(where=(User.full_name == "xxxx"))
        :param kwargs: 
        :return: 
        """
        return HunterModelService.count(User, **kwargs)

    @staticmethod
    def update(**kwargs):
        """
        更新操作，更新操作之后
        To use:
        >>> UserService.update(fields=({User.recent_operation_time: datetime }))
        :param kwargs: 
        :return: 
        """
        return HunterModelService.update(User, **kwargs)

    @staticmethod
    def save(**kwargs):
        """
        保存操作，不做第二次
        To use:
        >>> UserService.save(user_name="admin")
        :param kwargs: 
        :return: 
        """
        return HunterModelService.save(User, **kwargs)

    @staticmethod
    @MysqlManage.close_database
    def get_users(task_id):
        """
        根据任务id获取到对于的用户详情，多个用户
        SELECT * FROM user INNER JOIN usertask ON usertask.user_id = user.id where usertask.task_id = 2333
        To use:
         >>> UserService.get_users(task_id=1)
        :param task_id: 
        :return: 
        """
        from model.user_task import UserTask
        users = User.select().join(UserTask, JOIN.INNER, on=(UserTask.user_id == User.id)).where(
            UserTask.task_id == task_id).execute()
        return users

    @staticmethod
    @MysqlManage.close_database
    def get_create_user(task_id):
        """
        根据任务ID获取到创建任务者
        SELECT * FROM user WHERE id = (SELECT create_user_id FROM task WHERE task.id = task_id)
        :return: 
        """
        users = User.select().where(User.id == (Task.select(Task.create_user_id).where(Task.id == task_id))).execute()
        if len(users) == 1:
            return users[0]
        return None
