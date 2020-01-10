#!/ usr/bin/env
# coding=utf-8
"""
author: b5mali4
Copyright (c) 2018
"""
import unittest
import time
from peewee import *


class HunterAdminWebApiTestCase(unittest.TestCase):
    def testListTasksSpendTime(self):
        """
        测试 http://10.211.55.2:8888/api/v1/admin/task/ api耗时
        :return: 
        """
        import time
        import peewee
        from model.task import TaskService, Task
        from model.url import UrlService, Url
        from model.default_value import TaskStatus
        from api.service.redis_service import RedisService
        """
        测试 ListTask 耗时，便于对数据索引作出优化
        :return: 
        """
        task_id = None
        status = None
        # 构造条件查询元组
        query = list()
        if task_id is not None and task_id != "":
            query.append(Task.id == int(task_id))
        if status is not None and status != "":
            query.append(Task.task_status == int(status))

        # EXPLAIN	SELECT	*,(SELECT COUNT(*)	FROM	url	WHERE	url.task_id	=	task.id AND	url.`status`	!=2) AS	'unscaned_url_num',(SELECT COUNT(*)	FROM	url	WHERE	url.task_id	=	task.id AND	url.`status`	=2) AS	'scaned_urls_num'	FROM	task
        if len(query) > 0:
            tasks = Task.select(Task.receivers_email, Task.task_name, Task.created_time, Task.id, Task.access_key,
                                Task.task_status,
                                Url.select(fn.COUNT(Url.id)).alias('unscaned_urls_num').where(Url.task_id == Task.id,
                                                                                              Url.status != TaskStatus.DONE),
                                Url.select(fn.COUNT(Url.id)).alias('scaned_urls_num').where(Url.task_id == Task.id,
                                                                                            Url.status == TaskStatus.DONE)).where(
                *tuple(query)).execute()
        else:
            import logging
            logger = logging.getLogger('peewee')
            logger.addHandler(logging.StreamHandler())
            logger.setLevel(logging.DEBUG)

            tasks = Task.select(Task.receivers_email, Task.task_name, Task.created_time, Task.id, Task.access_key,
                                Task.task_status,
                                Url.select(fn.COUNT(Url.id)).alias('unscaned_urls_num').where(Url.task_id == Task.id,
                                                                                              Url.status != TaskStatus.DONE),
                                Url.select(fn.COUNT(Url.id)).alias('scaned_urls_num').where(Url.task_id == Task.id,
                                                                                            Url.status == TaskStatus.DONE)).execute()
        task_info_list = list()
        for task in tasks:
            hook_rule = RedisService.get_task(task.id)["hook_rule"]
            unscaned_urls_num = task.unscaned_urls_num
            scaned_urls_num = task.scaned_urls_num
            total_url_num = unscaned_urls_num + scaned_urls_num

            if task.task_status in [TaskStatus.KILLED, TaskStatus.DONE]:
                percent = 100
            else:
                percent = 0 if total_url_num == 0 else (scaned_urls_num / total_url_num) * 100

            task_info_list.append({'receiver_emails': task.receivers_email, 'task_name': task.task_name,
                                   'create_time': task.created_time.strftime("%Y-%m-%d %H:%M"), 'percent': percent,
                                   'unscaned_url_num': unscaned_urls_num, 'scaned_url_num': scaned_urls_num,
                                   'total_url_num': total_url_num, 'hook_rule': hook_rule, 'task_id': task.id,
                                   'task_access_key': task.access_key, 'task_status': task.task_status})
        task_info_list.reverse()

        print(task_info_list)

    def testSql(self):
        from model.task import TaskService, Task
        from model.url import UrlService, Url
        from model.user_task import UserTask, UserTaskService
        from model.vulnerability import Vulnerability, VulnerabilityService
        from model.default_value import TaskStatus
        from api.service.redis_service import RedisService

        import logging
        logger = logging.getLogger('peewee')
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.DEBUG)

        # Task.select(Task.created_time, Url.select(fn.COUNT(Url.id)).alias('count').where(Url.task_id == Task.id)).execute()

        #VulnerabilityService.get_tasks_urls_vulns_num_by_days(user_id=None, day_range=100)

        #Url.select(fn.COUNT(Url.id).alias('urls_total_num')).join(UserTask, JOIN.INNER,on=(UserTask.task_id == Url.task_id)).where(UserTask.user_id == 1).execute()

        Vulnerability.select(fn.COUNT(Vulnerability.id).alias('vulns_total_num')).join(UserTask, JOIN.INNER, on=(UserTask.task_id == Vulnerability.task_id)).where(UserTask.user_id == 1).execute()


if __name__ == "__main__":
    unittest.main()
