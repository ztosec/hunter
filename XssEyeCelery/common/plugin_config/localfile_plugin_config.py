#!/ usr/bin/env
# coding=utf-8
#
# Copyright 2019 ztosec & https://www.zto.com/
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
"""
author: b5mali4
To use:
>>> plugin_config = LocalFilePluginConfig().get_plugin_config()    
>>> print(plugin_config)
"""

import json
import threading
import configparser
from common.log import get_default_logger
from common.path import HUNTER_CONFIG_PATH
from common.plugin_config.base_plugin_config import BasePluginConfig

logger = get_default_logger()


class LocalFilePluginConfig(BasePluginConfig):
    """
    插件配置，从本地加载插件相关配置
    """
    _instance_lock = threading.Lock()

    def __init__(self, next_plugin_config=None):
        """
        降级方案，下一级插件配置
        """
        self.next_plugin_config = next_plugin_config
        self.plugin_config = dict()

    def __new__(cls, *args, **kwargs):
        """
        获取单例，双重检查机制
        :param args: 
        :param kwargs: 
        :return: 
        """
        if not LocalFilePluginConfig.initialized():
            with LocalFilePluginConfig._instance_lock:
                if not LocalFilePluginConfig.initialized():
                    LocalFilePluginConfig._single_instance = BasePluginConfig.__new__(cls)
        return LocalFilePluginConfig._single_instance

    @staticmethod
    def initialized():
        return hasattr(LocalFilePluginConfig, "_single_instance") and LocalFilePluginConfig._single_instance is not None

    def get_plugin_config(self, refresh=False):
        """
        从本地文件加载配置，提供降级方案
        :param refresh: 
        :return: 
        """
        if refresh or not self.plugin_config:
            config_parser = configparser.ConfigParser()
            config_parser.read(HUNTER_CONFIG_PATH)
            try:
                for key in config_parser.options('plugin'):
                    value = config_parser.get('plugin', key)
                    self.plugin_config[key] = json.loads(value)
            except Exception as e:
                if isinstance(e, configparser.NoSectionError):
                    self.init_plugin_config()
                    return self.get_plugin_config()
                else:
                    return self.derated_service()
        return self.plugin_config

    def init_plugin_config(self):
        """
        初始化本地文件配置，初始化配置中插件信息，即所有开关默认打开
        所有插件不移除，将目录中插件信息更新到配置文件中
        :return: 
        """
        from common.plugins_util import load_checkers, get_module

        logger.info("initialize plugin config")
        checker_dict = load_checkers(get_module(), True)

        config_parser = configparser.ConfigParser()
        config_parser.read(HUNTER_CONFIG_PATH)
        if "plugin" not in config_parser.sections():
            config_parser.add_section("plugin")

        for checker_name, checker_instance in checker_dict.items():
            config_parser.remove_option('plugin', checker_name)
            config_parser.set("plugin", checker_name, json.dumps(
                {"tag": checker_instance.info["tag"], "useable": checker_instance.useable, "removed": False}))
        with open(HUNTER_CONFIG_PATH, "w+") as file:
            config_parser.write(file)

    def modify_plugin_config(self, checker_name, key, value):
        """
        修改配置中插件信息，修改开关操作 
        :return: 
        """
        config_parser = configparser.ConfigParser()
        config_parser.read(HUNTER_CONFIG_PATH)
        if "plugin" not in config_parser.sections():
            self.init_plugin_config()
            config_parser.read(HUNTER_CONFIG_PATH)
        if checker_name in config_parser.options("plugin"):
            # config_parser.remove_option('plugin', checker_name)
            plugin_info = json.loads(config_parser.get('plugin', checker_name))
            if key in plugin_info:
                plugin_info[key] = value
                config_parser.set("plugin", checker_name, json.dumps(plugin_info))

        with open(HUNTER_CONFIG_PATH, "w+") as file:
            config_parser.write(file)
