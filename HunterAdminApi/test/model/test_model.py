#!/ usr/bin/env
# coding=utf-8
"""
author: b5mali4
Copyright (c) 2018
"""
import unittest
from common import log
from exception.request_classification_exception import HeaderParseError


class PluginInfoModelTestCase(unittest.TestCase):
    def testCreateTable(self):
        """
        测试创建表单
        :return: 
        """
        from model.plugin_info import PluginInfo
        PluginInfo.create_table()


class SystemConfigModelTestCase(unittest.TestCase):
    """
    系统设置表
    """

    def testCreateTable(self):
        """
        测试创建表单
        :return: 
        """
        from model.system_config import SystemConfig
        SystemConfig.create_table()


class TaskModelTestCase(unittest.TestCase):
    """
    任务表
    """

    def testCreateTable(self):
        """
        测试创建表单
        :return: 
        """
        from model.task import Task
        Task.create_table()

    def testGetCurrentTasks(self):
        """
        获取最新任务
        :return: 
        """
        import logging
        logger = logging.getLogger('peewee')
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.DEBUG)
        from model.task import TaskService
        task = TaskService.get_current_tasks(1)[0]
        print(task)


class UrlModelTestCase(unittest.TestCase):
    """
    Url表
    """

    def testCreateTable(self):
        """
        测试创建表单
        :return: 
        """
        from model.url import Url
        Url.create_table()


class UserModelTestCase(unittest.TestCase):
    """
    User表
    """

    def testCreateTable(self):
        """
        测试创建表单
        :return: 
        """
        from model.url import Url
        Url.create_table()

    def testGetAllUser(self):
        """
        列出所有用户
        :return: 
        """
        from model.user import UserService,User
        import logging
        logger = logging.getLogger('peewee')
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.DEBUG)
        user=UserService.get_fields_by_where()
        logger.info("1121")

        User.select().execute()
        logger.info(user)


if __name__ == "__main__":
    unittest.main()
