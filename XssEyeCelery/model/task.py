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
import datetime
from exception.hunter_web_exception import BaseHunterException
from model.hunter_model import HunterModel, HunterModelService
from model.default_value import TaskStatus
from common.mysql_util import MysqlManage


class Task(HunterModel):
    """
    正对整个任务，并非task_url
    id : 任务id
    task_status: 任务状态，hunter_status+sqlmap_status+xssfork_status 三者状态的汇总
    hunter_status: 任务状态(0:等待，1:运行中，2:运行完成)
    sqlmap_status: 任务状态(0:等待，1:运行中，2:运行完成)
    xssfork_status: 任务状态(0:等待，1:运行中，2:运行完成)
    create_user_id: 创建用户id，创建任务者  其他分配到的用户则和user表关联
    task_name: 任务名称
    create_time: 任务创建时间(平台创建任务时)
    killed_time: 结束任务时间(平台结束任务时)
    use_start_time: 使用开始时间(插件点击同步操作)
    finish_time: 结束时间(mq消费完成)
    use_send_time:   使用时间(从同步任务到结束任务)
    start_consume_time:开始消费到时间(消费到开始任务标示)
    finish_consume_time:完成消费时间(消费到结束任务标示)
    access_key: 认证身份(保留字段)
    hook_rule: redis 也存入一份，用于和openrestry使用
    receivers_email: 任务完成之后发送邮箱，支持多个
    """
    task_status = IntegerField(default=TaskStatus.WAITING)
    hunter_status = IntegerField(default=TaskStatus.WAITING)
    sqlmap_status = IntegerField(default=TaskStatus.WAITING)
    xssfork_status = IntegerField(default=TaskStatus.WAITING)
    create_user_id = IntegerField(null=True)
    task_name = TextField(null=True)
    created_time = DateTimeField(formats='%Y-%m-%d %H:%M:%S', default=datetime.datetime.now)
    killed_time = DateTimeField(null=True)
    use_start_time = DateTimeField(null=True)
    start_consume_time = DateTimeField(null=True)
    finish_consume_time = DateTimeField(null=True)
    access_key = TextField(null=True)
    hook_rule = TextField(null=True)
    receivers_email = TextField(null=True)

    class Meta:
        database = MysqlManage.get_database()


class TaskService:
    """
    对task表进行CURD操作
    """

    @staticmethod
    def get_fields_by_where(**kwargs):
        """
        To use:
        >>> tasks = TaskService.get_fields_by_where(fields=(Task.task_status), where=(Task.id == 1))
        >>> print(tasks)
        :param kwargs: 
        :return: 
        """
        return HunterModelService.get_fields_by_where(Task, **kwargs)

    @staticmethod
    def count(**kwargs):
        """
        数据数量
        To use:
        >>> TaskService.count(where=(Task.id == 1))
        :param kwargs: 
        :return: 
        """
        return HunterModelService.count(Task, **kwargs)

    @staticmethod
    def update(**kwargs):
        """
        更新操作，更新操作之后
        To use:
        >>> TaskService.update(fields=({Task.hunter_status: TaskStatus.DONE }))
        :param kwargs: 
        :return: 
        """
        return HunterModelService.update(Task, **kwargs)

    @staticmethod
    def save(**kwargs):
        """
        保存任务信息
        To use:
        >>> TaskService.save(task_status=1)
        :param url_id: 
        :param task_id: 
        :param result: 
        :return: 
        """
        return HunterModelService.save(Task, **kwargs)

    @staticmethod
    @MysqlManage.close_database
    def get_working_tasks(user_id):
        """
        根据用户id获取扫描中的任务列表
        SELECT * FROM task INNER JOIN usertask ON usertask.task_id = task.id WHERE	usertask.fullname='mingchen' AND  task.task_status <= 2
        :param user_id: 
        :return: 
        """
        from model.user_task import UserTask
        tasks = Task.select().join(UserTask, JOIN.INNER, on=(UserTask.task_id == Task.id)).where(
            UserTask.user_id == user_id, Task.task_status <= TaskStatus.WORKING).execute()
        return tasks

    @staticmethod
    @MysqlManage.close_database
    def get_tasks(user_id):
        """
        根据用户id获取任务列表，不光是任务创建者，分配给其他人的任务也能被看到
        SELECT * FROM task INNER JOIN usertask ON usertask.task_id = task.id WHERE	usertask.user_id='12'
        :param user_id: 
        :return: 
        """
        from model.user_task import UserTask
        tasks = Task.select().join(UserTask, JOIN.INNER, on=(UserTask.task_id == Task.id)).where(
            UserTask.user_id == user_id).execute()
        return tasks

    @staticmethod
    @MysqlManage.close_database
    def get_tasks_url_num_bak(task_id, task_status):
        """
        获取得到任务以及其对应的扫描url数据统计
        :param task_id: 
        :param task_status: 
        :return: 
        """
        from model.url import Url
        query = list()
        if task_id is not None and task_id != "":
            try:
                task_id = int(task_id)
            except ValueError:
                raise BaseHunterException("task_id 不是一个数字")
            query.append(Task.id == task_id)
        if task_status is not None and task_status != "":
            query.append(Task.task_status == int(task_status))

        if len(query) > 0:
            tasks = Task.select(Task.receivers_email, Task.task_name, Task.created_time, Task.id, Task.access_key,
                                Task.task_status, Task.hook_rule,
                                Url.select(fn.COUNT(Url.id)).alias('unscaned_urls_num').where(Url.task_id == Task.id,
                                                                                              Url.status != TaskStatus.DONE),
                                Url.select(fn.COUNT(Url.id)).alias('scaned_urls_num').where(Url.task_id == Task.id,
                                                                                            Url.status == TaskStatus.DONE)).where(
                *tuple(query)).execute()
        else:
            tasks = Task.select(Task.receivers_email, Task.task_name, Task.created_time, Task.id, Task.access_key,
                                Task.task_status, Task.hook_rule,
                                Url.select(fn.COUNT(Url.id)).alias('unscaned_urls_num').where(Url.task_id == Task.id,
                                                                                              Url.status != TaskStatus.DONE),
                                Url.select(fn.COUNT(Url.id)).alias('scaned_urls_num').where(Url.task_id == Task.id,
                                                                                            Url.status == TaskStatus.DONE)).execute()
        return tasks

    @staticmethod
    @MysqlManage.close_database
    def get_tasks_url_num(task_id, task_status):
        """
        获取得到任务以及其对应的扫描url数据统计
        :param task_id: 
        :param task_status: 
        :return: 
        """
        from model.url import Url
        from model.user import User
        query = list()
        if task_id is not None and task_id != "":
            try:
                task_id = int(task_id)
            except ValueError:
                raise BaseHunterException("task_id 不是一个数字")
            query.append(Task.id == task_id)
        if task_status is not None and task_status != "":
            query.append(Task.task_status == int(task_status))

        if len(query) > 0:
            tasks = Task.select(Task.receivers_email, Task.task_name, Task.created_time, Task.id, Task.access_key,
                                Task.task_status, Task.hook_rule,
                                User.select(User.user_name).alias('create_user_name').where(
                                    User.id == Task.create_user_id),
                                Url.select(fn.COUNT(Url.id)).alias('unscaned_urls_num').where(Url.task_id == Task.id,
                                                                                              Url.status != TaskStatus.DONE),
                                Url.select(fn.COUNT(Url.id)).alias('scaned_urls_num').where(Url.task_id == Task.id,
                                                                                            Url.status == TaskStatus.DONE)).where(
                *tuple(query)).execute()
        else:
            tasks = Task.select(Task.receivers_email, Task.task_name, Task.created_time, Task.id, Task.access_key,
                                Task.task_status, Task.hook_rule,
                                User.select(User.user_name).alias('create_user_name').where(
                                    User.id == Task.create_user_id),
                                Url.select(fn.COUNT(Url.id)).alias('unscaned_urls_num').where(Url.task_id == Task.id,
                                                                                              Url.status != TaskStatus.DONE),
                                Url.select(fn.COUNT(Url.id)).alias('scaned_urls_num').where(Url.task_id == Task.id,
                                                                                            Url.status == TaskStatus.DONE)).execute()
        return tasks

    @staticmethod
    @MysqlManage.close_database
    def get_task_status(task_id):
        """
        
        :param task_id: 
        :return: 
        """
        if TaskService.count(where=(Task.id == task_id)) > 0:
            target_task = TaskService.get_fields_by_where(where=(Task.id == task_id))[0]
            return target_task.hunter_status
        return None
