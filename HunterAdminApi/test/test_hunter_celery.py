#!/ usr/bin/env
# coding=utf-8
"""
author: b5mali4
Copyright (c) 2018
>>> python3 hunter_celery.py -A hunter_celery worker -l info -c 1
"""
import os
import logging

from celery import Celery

from common import log
from common.logo import logo
from common.logo import celery_logo
from common.logo import example_data
from common.path import HUNTER_PATH
from taskschedule.task_schedule import scan

os.chdir("{}config".format(HUNTER_PATH))
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
    scan(package=package, task_id=task_id, create_user=create_user, status=status)


@celery.task
def system_notice_celery(message):
    """
    运行在多台服务器下的消费者接收来自系统的消息，常见的有新增插件，关闭插件，删除插件
    :return: 
    """
    print(message)


def init():
    """
    启动的时候初始化，主要是新建一些日志目录之类的
    :return: 
    """
    logger.propagate = False
    logger.setLevel(logging.DEBUG)
    logger.info(celery_logo)


if __name__ == "__main__":
    init()
    celery.start()
