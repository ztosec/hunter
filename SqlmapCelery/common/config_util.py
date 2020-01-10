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
import configparser
from common import log
from common.path import HUNTER_CONFIG_PATH

logger = log.get_default_logger()
config = dict()
plugin = dict()
PAYLOAD_TAG = "65534"
HOOK_EVENTS = ['alert', 'confirm', 'prompt']
payloads = set()
weak_password_list = list()


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


def read_file_to_array(file_path):
    """
    从文件中读扫描字典
    :param file_path: 
    :return: 
    """
    results = []
    try:
        files = open(file_path, 'r')
        results = [line.replace("\n", "") for line in files.readlines()]
    except IOError as e:
        logger.exception("read_file_to_array rasie error")
    return results


def get_payloads(refresh=False):
    """
    初始化payload
    :return: 
    """
    from common.path import FUZZ_DIC_PATH
    global payloads
    global PAYLOAD_TAG
    if refresh or len(payloads) == 0:
        for payload in read_file_to_array(FUZZ_DIC_PATH):
            for hook_event in HOOK_EVENTS:
                payloads.add("{}//".format(payload.replace('alert', hook_event).replace("65534", PAYLOAD_TAG)))
                payloads.add("'{}//".format(payload.replace('alert', hook_event).replace("65534", PAYLOAD_TAG)))
                payloads.add("'>{}//".format(payload.replace('alert', hook_event).replace("65534", PAYLOAD_TAG)))
                payloads.add(">{}//".format(payload.replace('alert', hook_event).replace("65534", PAYLOAD_TAG)))
                payloads.add('"{}//'.format(payload.replace('alert', hook_event).replace("65534", PAYLOAD_TAG)))
                payloads.add('">{}//'.format(payload.replace('alert', hook_event).replace("65534", PAYLOAD_TAG)))
                payloads.add(str(payload.replace('alert', hook_event)).replace("'", "`").replace("65534", PAYLOAD_TAG))
                payloads.add(
                    str(payload.replace('alert', hook_event)).replace("'", "").replace("\"", "").replace("65534",
                                                                                                         PAYLOAD_TAG))
    return payloads
