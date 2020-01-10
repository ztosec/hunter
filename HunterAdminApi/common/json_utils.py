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


def loads(string):
    result = string
    while not isinstance(result, dict):
        result = json.loads(result)
    return result


def load(string, replace):
    """
    将null替换成replace
    :param string: 
    :param replace: 
    :return: 
    """
    result = loads(string)
    for key, value in result.items():
        if value is None:
            result[key] = replace
    return result


def has_dict_value_blank(dic, array):
    """
    检查字典中,键值为array数组中一员的值是否为空，如果有的话就true
    :param dic: 
    :param array: 
    :return: 
    """
    for key in array:
        if key in dic:
            value = dic[key]
            if isinstance(value, str) and str(value).strip() == "":
                return True
            elif isinstance(value, list) and list_is_blank(value):
                return True
            elif isinstance(value, object) and value is None:
                return True
        else:
            return True
    return False


def list_is_blank(items):
    """
    判断LIST是否出现NULL
    :param list: 
    :return: 
    """
    if not items or len(items) <= 0:
        return True
    assert isinstance(items, list)
    for item in items:
        if isinstance(item, str) and str(item).strip() == "":
            return True
        elif isinstance(item, object) and item is None:
            return True
    return False


def dict_auto_add(dic, key, num=None):
    """
    num为空的时候dict字段默认+1
    :param dic: 
    :param key: 
    :return: 
    """
    try:
        dic[key]
    except KeyError:
        dic[key] = 0
    finally:
        dic[key] += 1 if num is None else num


class Dict(dict):
    __setattr__ = dict.__setitem__
    __getattr__ = dict.__getitem__


def dict_to_object(dict_obj):
    """
    将dict类型转换成对象
    :param dict_obj: 
    :return: 
    """
    if not isinstance(dict_obj, dict):
        return dict_obj
    inst = Dict()
    for k, v in dict_obj.items():
        inst[k] = dict_to_object(v)
    return inst
