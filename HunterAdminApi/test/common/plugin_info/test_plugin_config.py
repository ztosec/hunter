#!/ usr/bin/env
# coding=utf-8
"""
author: b5mali4
Copyright (c) 2018
"""

import unittest
from common.plugin_config.localfile_plugin_config import LocalFilePluginConfig
from common.plugin_config.redis_plugin_config import RedisPluginConfig


class PluginConfigTestCase(unittest.TestCase):
    def testGetPluginConfigFromLocalFile(self):
        """
        测试从本地配置文件中加载配置
        :return: 
        """
        plugin_config = LocalFilePluginConfig()
        print(plugin_config)

        plugin_config = LocalFilePluginConfig()
        print(plugin_config)

        result = plugin_config.get_plugin_config()
        print(result)

    def testGetPluginConfigFromRedis(self):
        """
        测试从redis中加载配置，方便测试初始化redis
        :return: 
        """
        from api.service.redis_service import RedisService

        RedisService.init_plugin_config()

        plugin_config = RedisPluginConfig()
        print(plugin_config)
        result = plugin_config.get_plugin_config()
        print(result)

    def testCase1DegradedService(self):
        """
        测试降级方案，redis获取配置出现异常，将自动切换加载本地配置文件
        :return: 
        """
        local_plugin_config = LocalFilePluginConfig()
        redis_plugin_config = RedisPluginConfig(local_plugin_config)

        result = redis_plugin_config.get_plugin_config()
        print(result)

    def testCase2DegradedService(self):
        """
        可降级的
        :return: 
        """
        from common.plugin_config.base_plugin_config import DegradablePluginConfig

        degradable_plugin_config = DegradablePluginConfig.instance()
        result = degradable_plugin_config.get_plugin_config()
        print(result)
        result1 = degradable_plugin_config.get_plugin_config()
        print(result1)


if __name__ == "__main__":
    unittest.main()
