#!/ usr/bin/env
# coding=utf-8
"""
author: b5mali4
Copyright (c) 2018
测试sso认证模块
"""
import unittest


class SsoTestCase(unittest.TestCase):
    def testApiAccess(self):
        """
        测试api权限，如果没有授权会跳到认证页面
        :return: 
        """
        import json
        import requests
        post_data = {'task_id': 3}
        headers = {"Content-Type": "application/json"}
        req = requests.request(url='http://10.211.55.2:8888/api/v1/user/task/', method="delete",
                               data=json.dumps(post_data), headers=headers)
        print(req.json())


if __name__ == "__main__":
    unittest.main()
