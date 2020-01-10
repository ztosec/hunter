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
    >>> from common.http_util import HttpMethod
    >>> from common.http_util import ContentType
    >>> from parser.base_traffic_parser import BaseTrafficParser
    >>> # 测试get 请求
    >>> print(BaseTrafficParser.get_parameter(url="http://127.0.0.1/?name=23232&password=78812", http_method=HttpMethod.GET, content_type=HttpMethod.GET))
    >>> print(BaseTrafficParser.get_parameter(url="http://127.0.0.1/login", data="name=23333&", http_method=HttpMethod.POST, content_type=ContentType.ResourceContentType.DEFAULT))
"""
import re
import json
import warnings
from urllib import parse
from abc import ABCMeta, abstractmethod

from common.http_util import HttpMethod
from common.http_util import ContentType


class BaseTrafficParser:
    # 原生流量格式
    DEAFAULT_PARSER = "raw"
    # 浏览器插件流量格式
    CHROME_PARSER = "chrome-plugin"

    DIGITAL = (1, 'hunter_int')
    LETTER = (2, 'hunter_str')
    DIGMIXEDLETER = (3, 'hunter_mix')
    OTHER = (4, 'hunter_other')
    FLOAT = (5, 'hunter_float')

    """
    流量解析器，chrome插件获取的流量和http请求获取的流量不太一样
    """

    @staticmethod
    def _parse_get_parameter(url):
        """
        解析http get请求参数
        :return: 
        """
        result = dict()
        temp_keys_value = re.findall(u'\?((?:\w*=[\s\S\u4e00-\u9fa5]*&?)*)', url, re.S)
        if len(temp_keys_value) > 0:
            temp_keys_value = temp_keys_value[0]
            keys = re.findall('(\w{1,})=', temp_keys_value, re.S)
            for key in keys:
                regular = u'{}=([\s\S\u4e00-\u9fa5][^&^\n]*)'.format(key)
                try:
                    value = re.findall(regular, temp_keys_value)[0]
                except IndexError:
                    value = ""
                result[key] = value
        return result

    @staticmethod
    def _parse_post_parameter(data, content_type):
        """
        解析post参数，主要和content_type有关
        :param data: 
        :return: 
        """
        result = dict()
        if not content_type or ContentType.ResourceContentType.DEFAULT in content_type.lower():
            temp_keys_value = re.findall(u'\?*((?:\w*=[\s\S\u4e00-\u9fa5]*&?)*)', data, re.S)[0]
        elif ContentType.ResourceContentType.JSON in content_type.lower():
            return json.loads(data)
        elif ContentType.ResourceContentType.XML in content_type.lower():
            return data  # 暂时不支持
        elif ContentType.ResourceContentType.FORM in content_type.lower():
            filename = re.findall('filename="([\S\s]*)"', data, re.S)[0]
            return {'filename': filename}
        if len(temp_keys_value) > 0:
            keys = re.findall('(\w{1,})=', temp_keys_value, re.S)
            for key in keys:
                regular = u'{}=([\s\S\u4e00-\u9fa5][^&^\n]*)'.format(key)
                value = re.findall(regular, temp_keys_value)[0]
                result[key] = value
        return result

    @staticmethod
    def get_parameter(url, data=None, http_method=HttpMethod.GET, content_type=None):
        """
        解析参数，主要目的是为了去重使用
        :param url: 
        :param data: get 请求下为None
        :param http_method: 
        :param content_type: 
        :return: 
        """

        if http_method and http_method.lower() == HttpMethod.GET:
            return BaseTrafficParser._parse_get_parameter(url)
        elif http_method and http_method.lower() == HttpMethod.POST and data:
            return BaseTrafficParser._parse_post_parameter(data, content_type)

    @staticmethod
    def _replace_param_val_to_identification(http_parameter):
        """
        替换成参数值为 hunter_int
        :param http_parameter: 
        :return: 
        """
        result = {}
        for key, value in http_parameter.items():
            result[key] = value if key == "submit" else BaseTrafficParser._replace_identification(value)
        return result

    @staticmethod
    def simplify_request(url, data=None, http_method=HttpMethod.GET, content_type=None):
        """
        解析请求，并带上分类标记
        :param url: 
        :param data: 
        :param http_method: 
        :param content_type: 
        :return: 
        """
        if (http_method and http_method.lower() == HttpMethod.GET) or content_type is None:
            return {"url": BaseTrafficParser._simplify_get_request(url), "data": data, "http_method": http_method,
                    "content_type": None}
        elif http_method and http_method.lower() == HttpMethod.POST:
            if ContentType.ResourceContentType.DEFAULT in content_type:
                return {"url": url, "data": BaseTrafficParser._simplify_post_request_default(data),
                        "http_method": http_method, "content_type": ContentType.ResourceContentType.DEFAULT}
            elif ContentType.ResourceContentType.JSON in content_type:
                return {"url": url, "data": json.dumps(BaseTrafficParser._simplify_post_request_json(data)),
                        "http_method": http_method, "content_type": ContentType.ResourceContentType.JSON}
            elif ContentType.ResourceContentType.XML in content_type:
                return {"url": url, "data": data, "http_method": http_method,
                        "content_type": ContentType.ResourceContentType.XML}
            elif ContentType.ResourceContentType.FORM in content_type:
                return {"url": url, "data": BaseTrafficParser._simplify_post_request_form(data),
                        "http_method": http_method, "content_type": ContentType.ResourceContentType.FORM}
            elif ContentType.ResourceContentType.TXT in content_type:
                return {"url": url, "data": data, "http_method": http_method,
                        "content_type": ContentType.ResourceContentType.TXT}

    @staticmethod
    def _simplify_get_request(url):
        """
        解析请求，并带上分类标记，解析get请求
        :param data: 
        :param http_method: 
        :param content_type: 
        :return: 
        """
        have_parameter = False
        result_urls_key = None
        result_parameter = ""
        http_parameter = BaseTrafficParser._parse_get_parameter(url)
        http_parameter = BaseTrafficParser._replace_param_val_to_identification(http_parameter)
        for key, value in http_parameter.items():
            result_parameter += "{}={}&".format(key, value)
            have_parameter = True
        if have_parameter:
            result_parameter = "?{}".format(result_parameter[:-1])
            result_urls_key = re.subn(u'\?((?:\w*=[\s\S\u4e00-\u9fa5]*&?)*)', result_parameter, url)[0]
        return result_urls_key if result_urls_key else url

    @staticmethod
    def _simplify_post_request_default(data):
        """
        对 application/x-www-form-urlencoded类型参数解析
        :param data: 
        :param http_method: 
        :param content_type: 
        :return: 
        """
        result_urls_key = None
        have_parameter = False
        result_parameter = ""
        http_parameter = BaseTrafficParser._parse_post_parameter(data, ContentType.ResourceContentType.DEFAULT)
        http_parameter = BaseTrafficParser._replace_param_val_to_identification(http_parameter)
        for key, value in http_parameter.items():
            result_parameter += "{}={}&".format(key, value)
            have_parameter = True
        if have_parameter:
            result_urls_key = result_parameter[:-1]
        return result_urls_key if result_urls_key else data

    @staticmethod
    def _simplify_post_request_json(data):
        """
        对 application/json 类型参数解析
        :param data: 
        :return: 
        """
        return BaseTrafficParser._get_json_parameter(data)

    @staticmethod
    def _simplify_post_request_form(data):
        """
        上传文件 类型参数解析 multipart/form-data; boundary=----WebKitFormBoundaryH0TGOzR6zJhOJSVB
        :return: 
        """
        result_parameter = ""
        identification_result_parameter = None
        http_parameter = BaseTrafficParser._parse_post_parameter(data, ContentType.ResourceContentType.FORM)
        for key, value in http_parameter.items():
            result_parameter += '{}="{}"'.format(key, value)
        http_parameter = BaseTrafficParser._replace_param_val_to_identification(http_parameter)
        for key, value in http_parameter.items():
            identification_result_parameter = ""
            identification_result_parameter += '{}="{}"'.format(key, value)
        if result_parameter.strip() != "" and identification_result_parameter:
            data = str(data).replace(result_parameter, identification_result_parameter)
        return data

    def _simplify_post_request(url, data, http_method, content_type):
        """
        解析请求，并带上分类标记，解析get请求
        :param data: 
        :param http_method: 
        :param content_type: 
        :return: 
        """
        result_parameter = None
        http_parameter = BaseTrafficParser.get_parameter(url, data, http_method, content_type)
        http_parameter = BaseTrafficParser.replace_param_val_to_identification(http_parameter)
        for key, value in http_parameter.items():
            result_parameter += "{}={}&".format(key, value)
            have_parameter = True
        if have_parameter:
            result_parameter = "?{}".format(result_parameter[:-1])
            result_urls_key = re.subn(u'\?((?:\w*=[\s\S\u4e00-\u9fa5]*&?)*)', result_parameter, url)[0]
        return result_urls_key if result_urls_key else url

    @staticmethod
    def _get_json_parameter(str):
        """
        str1 = '{"name":{"pass": {"bb": 12222, "aa": {"hello": "xxx"}}}, "hello": "ssss"}'
        str2 = ```
        {"video":{"id":"29BA6ACE7A9427489C33DC5901307461","title":"体验课01","desp":"","tags":" ","duration":503,"category":"07AD1E11DBE6FDFC","image":"http://2.img.bokecc.com/comimage/0DD1F081022C163E/2016-03-09/29BA6ACE7A9427489C33DC5901307461-0.jpg","imageindex":0,"image-alternate":[{"index":0,"url":"http://2.img.bokecc.com/comimage/0DD1F081022C163E/2016-03-09/29BA6ACE7A9427489C33DC5901307461-0/0.jpg"},{"index":1,"url":"http://2.img.bokecc.com/comimage/0DD1F081022C163E/2016-03-09/29BA6ACE7A9427489C33DC5901307461-0/1.jpg"},{"index":2,"url":"http://2.img.bokecc.com/comimage/0DD1F081022C163E/2016-03-09/29BA6ACE7A9427489C33DC5901307461-0/2.jpg"},{"index":3,"url":"http://2.img.bokecc.com/comimage/0DD1F081022C163E/2016-03-09/29BA6ACE7A9427489C33DC5901307461-0/3.jpg"}]}}
        ```
        str3 = '{"name":{"pass": [{"bb":"xxx", "aaa": "bb"}, {"bb":"xxx34444444", "aaa": "bb"}]}, "hello": "ssss"}'
        str = '{"name":[{"bb":"xxx"}]}'
        str4 = '{"name":"chenming","whoamo":"11123333"}'
        递归解决json解析问题，解析多重json
        :param str: 
        :return: 
        """
        result = {}
        temp_jsons = BaseTrafficParser.loads(str)
        if temp_jsons is not None:
            if isinstance(temp_jsons, list):
                temp_result = dict()
                temp_result_list = list()
                for temp_json in temp_jsons:
                    BaseTrafficParser.set_type(temp_result, temp_json)
                    temp_result_list.append(temp_result)
                return temp_result_list
            else:
                BaseTrafficParser._set_type(result, temp_jsons)
                return result
        return result

    @staticmethod
    def _set_type(result, temp_json):
        """
        set type 主要被get_json_parameter调用
        :param result: 
        :param temp_json: 
        :return: 
        """
        for key, value in temp_json.items():
            if BaseTrafficParser.loads(value) is not None:
                result[key] = BaseTrafficParser._get_json_parameter(value)
            else:
                result[key] = BaseTrafficParser._replace_identification(value)

    @staticmethod
    def loads(object):
        result = None
        if isinstance(object, dict) or isinstance(object, list):
            return object
        try:
            result = json.loads(object)
            int(result)
            result = None
        except Exception as e:
            pass
        finally:
            return result

    @staticmethod
    def check_type(value):
        value = str(value)
        if sum([n.isdigit() for n in value.strip().split('.')]) == 2:
            return BaseTrafficParser.FLOAT[0]
        if value.isdigit():
            return BaseTrafficParser.DIGITAL[0]
        elif value.isalpha():
            return BaseTrafficParser.LETTER[0]
        elif value.isalnum():
            return BaseTrafficParser.DIGMIXEDLETER[0]
        else:
            return BaseTrafficParser.OTHER[0]

    @staticmethod
    def surround_with_single_quote(value):
        if str(value).startswith("'") and str(value).endswith("'"):
            return True, value[1:-1]
        else:
            return False, value

    @staticmethod
    def _replace_identification(value):
        is_surround_with_single_quote, value = BaseTrafficParser.surround_with_single_quote(value)
        value_type = None
        try:
            value_type = BaseTrafficParser.check_type(parse.quote(value))
        except TypeError:
            value_type = BaseTrafficParser.check_type(value)

        if value_type == BaseTrafficParser.DIGITAL[0]:
            value = BaseTrafficParser.remove_int_same()
        elif value_type == BaseTrafficParser.LETTER[0]:
            value = BaseTrafficParser.remove_str_same()
        elif value_type == BaseTrafficParser.DIGMIXEDLETER[0]:
            value = BaseTrafficParser.remove_mix_same()
        elif value_type == BaseTrafficParser.FLOAT[0]:
            value = BaseTrafficParser.remove_float_same()
        else:
            value = BaseTrafficParser.remove_other_same()
        if is_surround_with_single_quote:
            value = "'{}'".format(value)
        return value

    @staticmethod
    def remove_int_same():
        return BaseTrafficParser.DIGITAL[1]

    @staticmethod
    def remove_str_same():
        return BaseTrafficParser.LETTER[1]

    @staticmethod
    def remove_mix_same():
        return BaseTrafficParser.DIGMIXEDLETER[1]

    @staticmethod
    def remove_other_same():
        return BaseTrafficParser.OTHER[1]

    @staticmethod
    def remove_float_same():
        return BaseTrafficParser.FLOAT[1]

    @staticmethod
    def replace(str, substr):
        """
        :param old_str: 
        :param new_str: 
        :return: 
        """
        if isinstance(str, dict):
            str = json.dumps(str)
        return str.replace(BaseTrafficParser.DIGITAL[1], substr).replace(BaseTrafficParser.LETTER[1], substr).replace(
            BaseTrafficParser.DIGMIXEDLETER[1], substr).replace(BaseTrafficParser.OTHER[1], substr).replace(
            BaseTrafficParser.FLOAT[1], substr)

    @staticmethod
    def add_poc_data(url, data, http_method, content_type, poc):
        """
        在原来数据的基础上替换成poc数据
        :param url: get类型下完整url post为请求数据
        :param http_method: 
        :param content_type: 
        :param poc: 
        :return: 
        """
        try:
            poc_result = BaseTrafficParser.simplify_request(url=url, data=data, http_method=http_method,
                                                            content_type=content_type)
            if (http_method and http_method.lower() == HttpMethod.GET) or content_type is None:
                poc_result["url"] = BaseTrafficParser.replace(poc_result["url"], poc)
            elif http_method and http_method.lower() == HttpMethod.POST:
                poc_result["data"] = BaseTrafficParser.replace(poc_result["data"], poc)
        except Exception:
            poc_result = {"url": url, "data": data, "http_method": http_method, "content_type": content_type}
        return poc_result
