#!/ usr/bin/env
# coding=utf-8
"""
author: b5mali4
Copyright (c) 2018
To use:
redis服务，保存任务基本信息
"""
import unittest
import time
from api.service.redis_service import RedisService


class RedisServiceTestCase(unittest.TestCase):
    def testInitPluginInfo(self):
        RedisService.init_plugin_info()

    def testDeprecated(self):
        from deprecated import deprecated

        @deprecated(version='2.0', reason="This class is no longer supported")
        class Demo():
            def __init__(self):
                pass

        demo = Demo()
