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
import platform
import warnings
import logging.config
from common.path import HUNTER_LOG_PATH
from colorlog import ColoredFormatter
from logging.handlers import TimedRotatingFileHandler


class Logger:
    DEFAULT_LOGGER = None


def getLogger(name):
    """
    :return: 
    """
    logger = logging.getLogger(name=name)
    init_default_setting(logger)
    return logger


def get_default_logger():
    """
    To use:
    >>> logger = get_default_logger()
    >>> logger.info("success")
    :return: 
    """
    if Logger.DEFAULT_LOGGER is None:
        Logger.DEFAULT_LOGGER = logging.getLogger('DnsSocketLog')
        init_default_setting(Logger.DEFAULT_LOGGER)
    return Logger.DEFAULT_LOGGER


# handler2 = logging.handlers.TimedRotatingFileHandler("test.log", when="H", interval=1, backupCount=10)

def get_rotating_file_handler():
    """
    分割日志，按天划分文件
    :return rotating_file_handler: 
    """
    file_formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', "%Y-%m-%d %H:%M:%S")
    rotating_file_handler = TimedRotatingFileHandler(HUNTER_LOG_PATH, when="D", interval=1, backupCount=0)
    rotating_file_handler.setFormatter(file_formatter)
    return rotating_file_handler


def get_file_handler():
    """
    获取 file_handler设置
    :return: 
    """
    warnings.warn("建议直接使用get_rotating_file_handler")
    file_handler = logging.FileHandler(HUNTER_LOG_PATH)
    file_formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', "%Y-%m-%d %H:%M:%S")
    file_handler.setFormatter(file_formatter)
    return file_handler


def get_stream_handler():
    """
    获取 stream_handler配置
    :return stream_handler: 
    """
    stream_handler = logging.StreamHandler()
    stream_formatter = get_stream_formatter(platform.system())
    stream_handler.setFormatter(stream_formatter)
    return stream_handler


def get_stream_formatter(os):
    """
    根据操作系统选择是否调用ColoredFormatter，windows下对log颜色显示不好，默认去除
    :param os: 
    :return stream_formatter: 
    """
    if os == "Windows":
        stream_formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S")
    else:
        color_fmt = "%(log_color)s[%(asctime)s]%(reset)s %(log_color)s[%(levelname)s] %(message)s%(reset)s"
        stream_formatter = ColoredFormatter(color_fmt, "%Y-%m-%d %H:%M:%S")
    return stream_formatter


def init_default_setting(logger):
    """
    初始化默认配置，默认是INFO级别
    :return: 
    """
    assert isinstance(logger, logging.Logger)
    # file_handler = get_file_handler()
    stream_handler = get_stream_handler()
    rotating_file_handler = get_rotating_file_handler()
    logger.setLevel(logging.DEBUG)
    # logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    logger.addHandler(rotating_file_handler)
