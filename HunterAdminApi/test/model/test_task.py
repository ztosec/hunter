#!/ usr/bin/env
# coding=utf-8
"""
author: b5mali4
Copyright (c) 2018
"""
import unittest
from peewee import *
from common import log
from exception.request_classification_exception import HeaderParseError


class TaskModelTestCase(unittest.TestCase):
    def testGetTasksUrlNum(self):
        """
        测试执行SQL
        :return: 
        """
        from model.task import TaskService
        import logging
        logger = logging.getLogger('peewee')
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.DEBUG)

        TaskService.get_tasks_url_num(task_id=1, task_status=3)

    def testGetTasksUrlVulnNum(self):
        from model.task import TaskService
        from model.hunter_model import OrmModelJsonSerializer
        import logging
        logger = logging.getLogger('peewee')
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.DEBUG)

        tasks = TaskService.get_tasks_url_vuln_num(user_id=1)

        response_data = [{"task_name": task.task_name, "created_time": task.created_time.strftime("%Y-%m-%d %H:%M"), "task_id": task.id,
                          "urls_num": task.urls_num, "vulns_num": task.vulns_num} for task in tasks]
        for response in response_data:
            print(response)


if __name__ == "__main__":
    unittest.main()
