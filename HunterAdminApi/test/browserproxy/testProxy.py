#!/ usr/bin/env
# coding=utf-8
"""
author: b5mali4
Copyright (c) 2018
"""
import unittest
from networkproxycool.proxy import ProxyServer
from networkproxycool.proxy import ProxyHandler


class ProxyTestCase(unittest.TestCase):
    def testProxy(self):
        """
        测试代理启动
        :return: 
        """
        try:
            proxy = ProxyServer(ProxyHandler)
            proxy.start()
        except KeyboardInterrupt:
            proxy.stop()


if __name__ == "__main__":
    unittest.main()
