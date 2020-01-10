#!/ usr/bin/env
# coding=utf-8
"""
author: b5mali4
Copyright (c) 2018
"""
import unittest
from common.plugins_util import get_module, get_plugin, print_module, print_plugin, load_pyfiles, load_checkers


class PluginUtilTestCase(unittest.TestCase):
    """
    插件工具测试
    """

    def testGetModle(self):
        # print(get_module())
        print_module()

    def testGetPlugin(self):
        """
        根据模块显示插件
        :return: 
        """
        modules = get_module()
        print(modules)
        plugins = get_plugin(modle=modules[0])
        print(plugins)
        print_plugin(modules[0])

    def testloadPyfiles(self):
        """
        加载py文件
        :return: 
        """
        from common.path import PLUGIN_PATH
        plugin_path = "{}/{}".format(PLUGIN_PATH, "fastjson")
        py_files = load_pyfiles(plugin_path)
        print(py_files)

    def testLoadCheckers(self):
        """
        加载插件实体
        :return: 
        """
        check_dict = load_checkers("titans")
        for (key, value) in check_dict.items():
            print(key)
            print(value)

        check_dict2 = load_checkers("titans")
        for (key, value) in check_dict.items():
            print(key)
            print(value)

if __name__ == "__main__":
    unittest.main()
