#!/ usr/bin/env
# coding=utf-8
"""
author: b5mali4
Copyright (c) 2018
"""
import json
import unittest
import requests


class HunterUserApiTestCase(unittest.TestCase):
    def addUser2dbAndRedis(self):
        """
        同步一个账号到数据库和redis
        :return: 
        """
        from api.service.redis_service import RedisService
        from model.default_value import Role
        from model.user import User, UserService

        user_name = "b5mali4"
        full_name = "小明"
        email = "b5mali4@xx.com"
        dept_name = "信息安全部"
        role = Role.USER
        mobile_phone = "131xxxx9871"
        if UserService.count(where=(User.user_name == user_name)) <= 0:
            UserService.save(user_name=user_name, full_name=full_name, email=email, dept_name=dept_name,
                             role=role, mobile_phone=mobile_phone)
        else:
            UserService.update(fields=(
                {User.user_name: user_name, User.full_name: full_name, User.email: email, User.dept_name: dept_name,
                 User.role: role, User.mobile_phone: mobile_phone}))

        user = UserService.get_fields_by_where(where=(User.user_name == user_name))[0]

        user_info = {"user_name": "b5mali4", "full_name": "小明", "email": "b5mali4@xx.com",
                     "dept_name": "信息安全部", "role": Role.USER, "mobile_phone": "131xxxx9871", "id": user.id}

        RedisService.update_user(user_name="b5mali4", user_info=user_info)

    def testCreateTaskWithOutAuth(self):
        """
        不带认证的创建任务
        测试创建任务，主要观察针对不同请求数据的响应，rabbitmq，观察数据库和Redis是否填充完成
        
        redis同步一次用户信息
        
        'hook_rule', 'read_agreement', 'task_name'
        :return: 
        """
        self.addUser2dbAndRedis()
        headers = {"Content-Type": "application/json"}
        hook_rule = "11111"
        read_agreement = True
        task_name = "122"
        post_data = {'hook_rule': hook_rule, 'read_agreement': read_agreement, 'task_name': task_name}
        req = requests.request(url='http://10.211.55.2:8888/api/v1/user/task/', method="post",
                               data=json.dumps(post_data), headers=headers)
        print(req.json())

    def testCreateTaskWithAuth(self):
        """
        带认证的创建任务
        测试创建任务，主要观察针对不同请求数据的响应，观察数据库和Redis是否填充完成

        'hook_rule', 'read_agreement', 'task_name'
        :return: 
        """
        headers = {}
        hook_rule = "12121"
        read_agreement = True
        task_name = "122"
        post_data = {'hook_rule': hook_rule, 'read_agreement': read_agreement, 'task_name': task_name}
        req = requests.request(url='http://10.211.55.2:8888/api/v1/user/task/', method="post",
                               data=json.dumps(post_data), headers=headers)
        print(req.json())

    def testStopTaskWithOutAuth(self):
        """
        停止任务
        测试停止任务，主要观察redis和rabbitmq和数据库
        :return: 
        """
        post_data = {'task_id': 3}
        headers = {"Content-Type": "application/json"}
        req = requests.request(url='http://10.211.55.2:8888/api/v1/user/task/', method="delete",
                               data=json.dumps(post_data), headers=headers)
        print(req.json())

    def testStopTaskWithAuth(self):
        """
        停止任务
        测试停止任务，主要观察redis和rabbitmq和数据库
        :return: 
        """
        post_data = {'task_id': 3}
        headers = {"Content-Type": "application/json"}
        req = requests.request(url='http://10.211.55.2:8888/api/v1/user/task/', method="delete",
                               data=json.dumps(post_data), headers=headers)
        print(req.json())

    def testUpdateTaskWithAuth(self):
        """
        停止任务
        测试停止任务，主要观察redis和rabbitmq和数据库
        :return: 
        """
        post_data = {
            "hook_rule": "121721212",
            "task_id": 2,
            # "user_ids": [""]
        }
        headers = {"Content-Type": "application/json"}
        req = requests.request(url='http://10.211.55.2:8888/api/v1/user/task/', method="put",
                               data=json.dumps(post_data), headers=headers)
        print(req.json())

    def testCurrentTask(self):
        """
        显示当前任务
        :return: 
        """
        headers = {
            "Cookie": "m=2258:YWRtaW46MnZ4SVNBbWFTb1BzQUFCWElIU2hz; session=eyJ1c2VyX25hbWUiOiJtaW5nY2hlbiJ9.EEZK5w.HKTR9TT8rlvQAUq1-Ld_jYWX3Zw"}
        req = requests.request(url='http://10.211.55.2:8888/api/v1/user/current_task/', method="get", headers=headers)
        print(req.json())


if __name__ == "__main__":
    unittest.main()
