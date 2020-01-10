#!/ usr/bin/env
# coding=utf-8
"""
author: b5mali4
Copyright (c) 2018
"""

import unittest


class ConfigUtilTestCase(unittest.TestCase):
    def testGetWeakPassword(self):
        """
        测试
        :return: 
        """
        from common.config_util import get_system_config
        from common.config_util import get_weak_password_list
        # print(get_config())
        print(get_weak_password_list())

    def testReadConfig(self):
        """
        测试读配置文件
        :return: 
        """
        import os
        import configparser
        from common.path import HUNTER_CONFIG_PATH
        config_parser = configparser.ConfigParser()
        config_parser.read(HUNTER_CONFIG_PATH)
        print(config_parser.sections())
        print(config_parser.options('config'))
        print(config_parser.items('config'))

    def testWriteConfig(self):
        """
        测试写配置文件
        :return: 
        """
        import os
        import configparser
        from common.path import HUNTER_CONFIG_PATH
        config_parser = configparser.ConfigParser()
        config_parser.add_section("plugin")
        config_parser.set("plugin", "fastjson", '1222')
        with open(HUNTER_CONFIG_PATH, "a+") as file:
            config_parser.write(file)

    def testModifyConfig(self):
        """
        测试修改配置文件
        :return: 
        """
        import os
        import configparser
        from common.path import HUNTER_CONFIG_PATH
        config_parser = configparser.ConfigParser()
        config_parser.read(HUNTER_CONFIG_PATH)
        config_parser.remove_option('plugin', 'fastjson')
        config_parser.set("plugin", "fastjson", '3333')
        print(config_parser.options('plugin'))
        with open(HUNTER_CONFIG_PATH, "w+") as file:
            config_parser.write(file)

    def testInitPluginConfig(self):
        """
        测试初始化插件信息
        :return: 
        """
        from common.config_util import init_plugin_config

        init_plugin_config()

    def testGetPluginConfig(self):
        from common.config_util import get_plugin_config

        result = get_plugin_config()
        print(result)


if __name__ == "__main__":
    unittest.main()
