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
"""
import json
import threading
import configparser
from abc import ABCMeta, abstractmethod

from common.path import HUNTER_PASS_DIC_PATH
from common.path import HUNTER_CONFIG_PATH
from common.log import get_default_logger

config = dict()
plugin = dict()
weak_password_list = list()
logger = get_default_logger()


def get_system_config(refresh=False):
    """
    获取配置文件的一些信息
    :return: 
    """
    global config
    if refresh or not config:
        config_parser = configparser.ConfigParser()
        config_parser.read(HUNTER_CONFIG_PATH)
        for key in config_parser.options('config'):
            value = config_parser.get('config', key)
            config[key] = json.loads(value)
    return config


def get_weak_password_list(refresh=False):
    """
    返回弱密码字典
    :return: 
    """
    global weak_password_list
    if refresh or not weak_password_list:
        with open(HUNTER_PASS_DIC_PATH, 'r') as dics:
            weak_password_list = [line.replace("\n", "") for line in dics.readlines()]
    return weak_password_list
