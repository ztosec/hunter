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
>>> bash start_consume.sh hunter 
"""
import logging
import os
from celery import Celery
from taskschedule.task_schedule import modify_checker
from taskschedule.task_schedule import scan
from common import log
from common.broadcast_value import BroadCastAction, BroadCastType
from common.plugins_util import modify_default_checkers, load_default_checkers
from common.logo import celery_logo
from common.logo import logo
from common.path import HUNTER_PATH
from model.default_value import TaskStatus
from model.task import Task, TaskService

os.chdir("{}/config".format(HUNTER_PATH))
celery = Celery()
celery.config_from_object('celery_config')
# logger = log.getLogger("celery")
logger = log.get_default_logger()


@celery.task
def scan_celery(package, task_id, create_user, status):
    """
    celey 调度模式扫描
    注意，scan_celery函数只有在celey开启的时候才会
    :param package: 
    :param task_id: 
    :param create_user: 
    :param status: 
    :return: 
    """
    logger.setLevel(logging.INFO)
    logger.info(logo)
    if status == TaskStatus.WORKING:
        # 更新任务状态和hunter状态
        current_task_status = TaskService.get_task_status(task_id=task_id)
        if current_task_status and current_task_status < TaskStatus.WORKING:
            TaskService.update(fields=({Task.task_status: TaskStatus.WORKING}), where=(Task.id == task_id))
        TaskService.update(fields=({Task.sqlmap_status: TaskStatus.WORKING}), where=(Task.id == task_id))
        logger.warn("there is a task [task_id:{}, create_user:{}] has start".format(task_id, create_user))
    elif status == TaskStatus.KILLED:
        try:
            TaskService.update(fields=({Task.sqlmap_status: TaskStatus.DONE}), where=(Task.id == task_id))
            current_task = TaskService.get_fields_by_where(where=(Task.id == task_id))[0]
            if current_task.hunter_status == TaskStatus.DONE and current_task.sqlmap_status == TaskStatus.DONE \
                    and current_task.xssfork_status == TaskStatus.DONE:
                TaskService.update(fields=({Task.task_status: TaskStatus.DONE}), where=(Task.id == task_id))
                task_notice_celery.delay(
                    message={"type": BroadCastType.TASK, "action": BroadCastAction.COMPLETE_TASK_NOTIFICATION,
                             "data": {"task_id": task_id}})

        except Exception:
            logger.exception("scan_celery error")
        logger.warn("there is a task [task_id:{}, create_user:{}] has killed".format(task_id, create_user))
    else:
        scan(package=package, task_id=task_id, create_user=create_user, status=status)


@celery.task
def system_notice_celery(broadcast):
    """
    系统通知
    :return: 
    """
    broadcast_type = broadcast["type"]
    action = broadcast["action"]
    if broadcast_type == BroadCastType.PLUGIN:
        if action == BroadCastAction.MODIFY_PLUGIN:
            modify_checker(broadcast)


@celery.task
def task_notice_celery(message):
    """
    任务状态通知，任务扫描开始，扫描结束通知，接入钉钉，邮件或者其他平台
    :return: 
    """
    action = message["action"]
    if action == BroadCastAction.COMPLETE_TASK_NOTIFICATION:
        task_id = message["data"]["task_id"]
        logger.warn("Cheers! there is a task task_id:{} has been checked out".format(task_id))


def init():
    """
    启动的时候初始化，主要是新建一些日志目录之类的
    :return: 
    """
    logger.propagate = False
    logger.setLevel(logging.DEBUG)
    # logger.setLevel(logging.WARN)
    logger.info(celery_logo)
    load_default_checkers(True)
    modify_default_checkers()


if __name__ == "__main__":
    init()
    celery.start()
