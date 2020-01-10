#!/ usr/bin/env
# coding=utf-8
#
# Copyright 2019 ztosec & https://sec.zto.com/
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
            
"""
import json
import threading
import configparser
from common.log import get_default_logger
from common.path import HUNTER_CONFIG_PATH
from common.plugin_config.base_plugin_config import BasePluginConfig

logger = get_default_logger()


class RedisPluginConfig(BasePluginConfig):
    """
    插件配置，从redis加载插件相关配置
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
        :param args: 
        :param kwargs: 
        :return: 
        """
        if not RedisPluginConfig.initialized():
            with RedisPluginConfig._instance_lock:
                if not RedisPluginConfig.initialized():
                    RedisPluginConfig._single_instance = BasePluginConfig.__new__(cls)
        return RedisPluginConfig._single_instance

    @staticmethod
    def initialized():
        return hasattr(RedisPluginConfig, "_single_instance")

    def get_plugin_config(self, refresh=True):
        """
        从redis中获取插件配置信息，如果出异常会自动降级
        :param refresh: 
        :return: 
        """
        from common.redis_util import RedisManage
        from api.service.redis_service import RedisService
        if refresh or not self.plugin_config:
            try:
                plugin_configs = RedisManage.get_redis_client().hgetall(RedisService.HUNTER_PLUGIN_SWITCH)
                for plugin_name, plugin_config_info in plugin_configs.items():
                    self.plugin_config[plugin_name] = json.loads(plugin_config_info)
                if not plugin_configs:
                    logger.warn("RedisPluginConfig get_plugin_config empty, hunter will try derated_service")
                    return self.get_derated_plugin_config()
            except Exception as e:
                logger.exception("RedisPluginConfig get_plugin_config error, hunter will try derated_service")
                return self.get_derated_plugin_config()

        return self.plugin_config

    def modify_plugin_config(self, checker_name, key, value):
        """
        收到开启禁用开关，本身不会再去修改redis中的配置信息，只会同步修改到本地文件
        :param checker_name: 
        :param key: 
        :param value: 
        :return: 
        """
        if self.next_plugin_config and isinstance(self.next_plugin_config, BasePluginConfig):
            self.next_plugin_config.modify_plugin_config(checker_name, key, value)
