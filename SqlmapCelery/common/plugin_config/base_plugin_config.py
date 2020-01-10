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
>>> sq = Square(3)
>>> sq.area
"""
import threading
from abc import ABCMeta, abstractmethod


class BasePluginConfig(object):
    __metaclass__ = ABCMeta
    """
    插件配置，为HunterCelery使用
    """

    def __init__(self):
        """
        plugin_config格式如下 {'fastjson1': {'tag': 'fastjson', 'useable': 1, 'removed': False}}
        """
        self.plugin_config = dict()
        self.next_plugin_config = None

    @abstractmethod
    def get_plugin_config(self, refresh=False):
        pass

    def get_derated_plugin_config(self):
        """
        降级服务
        :return: 
        """
        if self.next_plugin_config and isinstance(self.next_plugin_config, BasePluginConfig):
            return self.next_plugin_config.get_plugin_config()

    @abstractmethod
    def modify_plugin_config(self, checker_name, key, value):
        pass


class DegradablePluginConfig:
    _instance_lock = threading.Lock()

    @staticmethod
    def instance():
        """
        可降级配置，默认从redis中同步插件配置信息
        :return: 
        """
        from common.plugin_config.localfile_plugin_config import LocalFilePluginConfig
        from common.plugin_config.redis_plugin_config import RedisPluginConfig

        if not DegradablePluginConfig.initialized():
            with DegradablePluginConfig._instance_lock:
                if not DegradablePluginConfig.initialized():
                    local_file_plugin_config = LocalFilePluginConfig()
                    DegradablePluginConfig._single_instance = RedisPluginConfig(local_file_plugin_config)
        return DegradablePluginConfig._single_instance

    @staticmethod
    def initialized():
        return hasattr(DegradablePluginConfig,
                       "_single_instance") and DegradablePluginConfig._single_instance is not None
