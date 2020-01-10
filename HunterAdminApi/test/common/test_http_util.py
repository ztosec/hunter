#!/ usr/bin/env
# coding=utf-8
"""
author: b5mali4
Copyright (c) 2018
"""
import unittest
from common.http_util import get_host_port, get_parent_route, remove_http, get_top_domain


class HttpUtilTestCase(unittest.TestCase):
    def testRemoveHttp(self):
        """
        测试
        :return: 
        """
        print(get_parent_route(url='https://www.domain2333.com:80/xxxxxxx'))
        print(remove_http(url='domain.com:8090'))
        print(remove_http(url='https://domain.cn/////xssssss.jsp'))
        print(remove_http(url='domain'))
        print(get_host_port(url='https://ww.domain2333.com:8090/'))
        print(get_host_port(url='https://ww.domain2333.com/xxxx'))
        print(get_host_port(url='https://ww.domain2333.com:8090/xxxx'))
        print(get_host_port(url='https://ww.domain2333.com/'))
        print(get_host_port(url='https://domain:8090'))
        print(get_host_port(url='https://domain/////xssssss.jsp'))
        print(get_host_port(url='127.0.0.1', default_port=8090))
        print(get_host_port(url='127.0.0.1:8909'))
        print(get_top_domain(url='https://www.w333.domain2333.com:81/xxxxx'))


if __name__ == "__main__":
    unittest.main()
