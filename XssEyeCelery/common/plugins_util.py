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
插件工具类，2.0版本从本地config.ini文件加载配置，2.1版本从redis中加载插件配置，降级时才使用config.ini配置文件
"""
import imp
import os
import logging
import traceback
from sys import version_info
from common import log
from common.path import PLUGIN_PATH
from exception.request_classification_exception import PluginNotFoundError

if version_info < (3, 0):
    from exceptions import OSError as FileNotFoundError
else:
    pass

# 全局插件实体字典，key为插件名称，value为插件实体

CHECKER_INSTANCE_DICT = dict()
logger = log.get_default_logger()


def get_module():
    """
    显示所有模块
    :return: 
    """
    whole_modules = os.listdir(PLUGIN_PATH)
    invalid_modules = ["__init__.py", "__pycache__", "base", "tmp", ".DS_Store", "__init__.pyc"]
    remove_invalid_modules(invalid_modules, whole_modules)
    return whole_modules


def remove_invalid_modules(invalid_modules, whole_modules):
    assert isinstance(invalid_modules, list)
    for invalid_module in invalid_modules:
        remove_invalid_module(invalid_module, whole_modules)


def remove_invalid_module(invalid_module, whole_modules):
    assert isinstance(whole_modules, list)
    assert isinstance(invalid_module, str)
    if invalid_module in whole_modules:
        whole_modules.remove(invalid_module)


def get_plugin(module):
    """
    根据模块显示具体插件
    :return: 
    """
    try:
        result = os.listdir(PLUGIN_PATH + module)
        remove_invalid_modules(["__init__.py", "__pycache__"], result)
        result = [plugin.replace(".py", "") for plugin in result]
    except FileNotFoundError:
        raise PluginNotFoundError(module)
    return result


def print_module():
    """
    显示模块
    :return: 
    """
    modles = get_module()
    logger.info("总共有{}个模块".format(len(modles)))
    for index, item in enumerate(modles):
        logger.debug('[%s]%s' % (index, item))


def print_plugin(module):
    """
    根据模块显示插件
    :param modle: 
    :return: 
    """
    try:
        plugins = get_plugin(module)
        logger.info("{}模块总共有{}个插件".format(module, len(plugins)))
        for index, item in enumerate(plugins):
            logger.info('[%s]%s' % (index, item))
    except PluginNotFoundError as e:
        logger.error(e)


def load_pyfiles(path):
    """
    根据路径加载出py文件
    :param path: 
    :return: 
    """
    files = []
    try:
        files = ["%s/%s" % (path, file) for file in os.listdir(path) if file.endswith('.py') and file != '__init__.py']
    except (OSError, FileNotFoundError):
        logger.exception("load_pyfiles error")
        raise PluginNotFoundError(path)
    return files


def load_checkers(module_names, reload=False):
    """
    根据模块名字加载poc
    to Use:
    >>> from common.plugins_util import load_checkers
    >>> plugins = load_checkers(["fastjson", "jackson"])
    >>> print(plugins)
    
    :param module_names: 
    :param refresh: 
    :return: 
    """
    global CHECKER_INSTANCE_DICT

    if not CHECKER_INSTANCE_DICT or reload:
        logger.info("reload local plugins")
        try:
            for module_name in module_names:
                modle_path = "{}/{}".format(PLUGIN_PATH, module_name.strip())
                plugin_files = load_pyfiles(modle_path)
                for plugin_file in plugin_files:
                    load_source(CHECKER_INSTANCE_DICT, plugin_file)

        except PluginNotFoundError:
            logger.exception("load_checkers error")
            logger.warn('模块{}不存在'.format(modle_path))
            exit()

    # logger.info('local found {} plugins'.format(len(CHECKER_INSTANCE_DICT)))
    return CHECKER_INSTANCE_DICT


def load_default_checkers(reload=False):
    """
    加载默认的插件
    :param refresh: 
    :return: 
    """
    if not CHECKER_INSTANCE_DICT or reload:
        load_checkers(get_module(), reload)
    # logger.info('local found %d plugins, %d plugins useable' % (len(CHECKER_INSTANCE_DICT), len(get_useable_checkers())))
    return CHECKER_INSTANCE_DICT


def modify_default_checkers():
    """
    修改插件状态，根据配置文件自动降级
    :return: 
    """
    from common.plugin_config.base_plugin_config import DegradablePluginConfig

    checkers = load_default_checkers()
    for (k, v) in DegradablePluginConfig.instance().get_plugin_config(True).items():
        if k in checkers:  # 确认配置文件和本地插件是否一致
            checkers[k].useable = v["useable"]

    logger.info('local found %d plugins, %d plugins useable' % (len(CHECKER_INSTANCE_DICT), len(get_useable_checkers())))


def get_useable_checkers():
    """
    列出可用插件列表
    :return: 
    """
    useable_checkers = list()
    for (checker_name, checker_instance) in CHECKER_INSTANCE_DICT.items():
        if checker_instance.useable:
            useable_checkers.append(checker_instance)

    return useable_checkers


def load_source(checker_instance_dict, plugin_file):
    """
    导入插件实体至checker_instance_dict
    新增插件路径
    :param checker_instance_list: 
    :param plugin_file: 
    :return: 
    """
    base_checker = imp.load_source('BaseChecker', plugin_file)
    checker_instance = base_checker.Checker()
    key = checker_instance.info["name"]
    checker_instance.absolute_plugin_path = os.path.normpath(plugin_file)
    checker_instance.relative_plugin_path = os.path.normpath(plugin_file).replace(PLUGIN_PATH, "")
    checker_instance_dict[key] = checker_instance


def get_plugin_uuid():
    """
    生成每次插件调用时的uuid
    :return: 
    """
    pass
