#!/ usr/bin/env
# coding=utf-8
"""
author: b5mali4
Copyright (c) 2018
"""
import unittest
from common.json_utils import loads, has_dict_value_blank


class JsonUtilTestCase(unittest.TestCase):
    def testCase1(self):
        data = '{"address": "", "avatar": "1223.png", "cert_level": 3, "city": "上海市", "country": "中国", "dept_code": "123"}'
        print(type(loads(data)))
        print(loads(data))
        # str = '{"name": null, "age": 12}'
        # print(load(str, "w"))
        dic = {"name": "hello", "user": ''}
        print(has_dict_value_blank(dic, ['name', "user"]))


if __name__ == "__main__":
    unittest.main()
