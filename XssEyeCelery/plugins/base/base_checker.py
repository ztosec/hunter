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

Simple subPlugin example code:

class Checker(BaseChecker):
    # 检测逻辑
    def check_logic(self, request_raw):
        host, port = get_host_port(request_raw['url'])
        if port == 9012:
            self.result["status"] = True
            self.result["info"] = '%s开放了9012端口服务' % http_poc_url
            self.result['payload'] = http_poc_url
        
    #插件信息
    def init_plugin_info(self):
        name = "name1"
        imp_version = "< spring 2.1"
        description = "see http://xxxxx/"
        repair = "升级到titans1.8.3或者其以上版本"
        type = VulnType.OTHER
        author = "b5mali4"
        temp_info = {"repair": repair, "name": name, "type": type, "description": description,
                     "imp_version": imp_version, "author": author}
        self.info = dict(self.info, **temp_info)
 
To use:
>>> req1 = {"url": "http://127.0.0.1:8080/", "method": "get", "headers": "{\"Cookie\":\"SESSION\"}"}
>>> checker = Checker()
>>> checker.check_vuln(req1)
>>> print(checker.result)
"""
import time
import json
from common import log
from sys import version_info
from json.decoder import JSONDecodeError
from abc import ABCMeta, abstractmethod
from common.system_util import encode_b64
from plugins.base.vuln_enum import PluginSwith
from parser.base_traffic_parser import BaseTrafficParser
from parser.chrome_traffic_parser import ChromeTrafficParser
from model.system_config import SystemConfig, SystemConfigService
from exception.hunter_web_exception import BaseHunterException
from exception.request_classification_exception import PluginInfoError
from exception.request_classification_exception import RequestParseError
from exception.request_classification_exception import HeaderParseError

if version_info < (3, 0):
    from exceptions import ValueError as JSONDecodeError
else:
    from json.decoder import JSONDecodeError


class BaseChecker(object):
    """
    抽象插件父类
    """
    __metaclass__ = ABCMeta
    logger = log.get_default_logger()
    # 解析类
    PARSER_DIC = {BaseTrafficParser.DEAFAULT_PARSER: BaseTrafficParser,
                  BaseTrafficParser.CHROME_PARSER: ChromeTrafficParser}

    def __init__(self):
        """
        初始化流程下:
        1.初始化插件基本信息
        2.检测插件信息必传字段是否完整
        
        disable表示是否禁用
        path表示插件的实际路径
        absolute_plugin_path 插件绝对路径
        relative_plugin_path 插件相对路径
        """
        self.info = dict()
        self.useable = PluginSwith.ON
        self.result = dict()
        self.init_plugin_info()
        self.absolute_plugin_path = None
        self.relative_plugin_path = None
        try:
            self.check_plugin_info()
        except BaseHunterException as e:
            BaseChecker.logger.exception("插件信息错误")

    def init_check_result(self):
        """
        初始化检测结果
        :return: 
        """
        self.result = {'status': False, 'info': '没有漏洞(默认的描述信息)', 'error': [], 'details': self.info, 'payload': ''}

    @abstractmethod
    def init_plugin_info(self):
        """
        初始化加载插件
        :return: 
        """
        pass

    def check_vuln(self, request_raw):
        """
        check_logic为基础检测逻辑，各个插件自己实现，首先判断插件是否为禁用状态
        :param request_raw: 
        :return: 
        """
        try:
            self.init_check_result()
            if self.useable == PluginSwith.ON:
                self.check_request_raw(request_raw)
                self.check_logic(request_raw)
                self.record_payload(request_raw)
        except BaseHunterException as e:
            BaseChecker.logger.exception("请求数据包格式出错")
        finally:
            return self.result

    @abstractmethod
    def check_logic(self, request_raw):
        """
        在里面对result进行赋值
        :param request_raw: 
        :return: 
        """
        pass

    async def async_check_vuln(self, request_raw):
        """
        新增异步函数
        :param package: 
        :return: 
        """
        return self.check_vuln(request_raw)

    def parse_headers(self, headers=dict()):
        """
        解析参数
        :param headers: 
        :return: 
        """
        if not isinstance(headers, dict):
            raise HeaderParseError()

    def check_request_raw(self, request_raw):
        """
        检查流量数据包中的必要字段是否完整
        :param request_raw: 
        :return: 
        """
        if not isinstance(request_raw, dict):
            raise BaseHunterException(
                "传入的request_raw不是一个dict类型，其类型为{type}".format(type=type(request_raw) if request_raw else None))

        keys = ["type", "url", "method", "headers"]
        miss_keys = []
        for key in keys:
            if key not in request_raw:
                miss_keys.append(key)
        if len(miss_keys) > 0:
            raise RequestParseError(request_raw, miss_keys)

    def check_plugin_info(self):
        """
        检查info的必要字段是否完整
        :param info: 
        :return: 
        """
        assert isinstance(self.info, dict), "传入的info不是一个dict类型"
        keys = ["tag", "author", "name", "imp_version", "description", "repair", "type"]
        miss_keys = []
        for key in keys:
            if key not in self.info:
                miss_keys.append(key)
        if len(miss_keys) > 0:
            raise PluginInfoError(self.info, miss_keys)

    def get_plugin_info(self):
        return self.info

    def parse_data(self, package):
        """
        解析data 
        data为空 
        data 为XML,data为合法str,data为非法str
        :param data: 
        :return: 
        """
        if isinstance(package, dict):
            if "data" in package:
                try:
                    result = json.loads(package['data'])
                except JSONDecodeError:
                    result = package['data']
            else:
                result = None
        if isinstance(package, str):
            try:
                result = json.loads(package)
            except JSONDecodeError:
                result = package
        return result

    def generate_uuid(self):
        """
        生成uuid，根据时间戳生成
        :return: 
        """
        current_time = str(time.time())
        return encode_b64(current_time.split(".")[1])

    def generate_blind_poc(self):
        """
        生成poc，生成无回显poc ，根据选择的是Dns模块还是Socket模块，选择规则如下:
        1.Dns模块单独开启了，优先使用Dns模块
        2.Socket模块单独开启了，使用Socket模块
        3.Dns模块和Socket模块开启了，使用Dns模块
        4.都没开启则不调用
        
        根据Dns或者Socket模块开关获取poc 如下代码为检测命令执行
        Simple example usage code:
          
            blind_poc, check_bilnd_poc_url, hunter_log_api_token = self.generate_blind_poc()
            
            if not blind_poc["data"]:
                return
            
            if blind_poc["type"] == "dns":
                attack_payload = "http://%s" % (blind_poc["data"]) # 得到的是一个域名，域名前缀为uuid
            elif blind_poc["type"] == "socket":
                attack_payload = "http://%s:%s/%s" % (blind_poc["data"]["host"], blind_poc["data"]["port"], blind_poc["data"]["uuid"])
            
            # 情况1 和情况2
            if http_method == HttpMethod.GET or (http_method == HttpMethod.POST and content_type is None):
                payload = UrlDataClassification.add_poc_data(url=temp_url, http_method=http_method, content_type=content_type, poc="|wget %s" % (attack_payload))
                self.request(method=http_method, url=payload, data=temp_data, headers=temp_headers)
            
            elif http_method == HttpMethod.POST and content_type is not None and temp_data is not None:
                payload = UrlDataClassification.add_poc_data(url=temp_data, http_method=http_method, content_type=content_type, poc="|wget %s" % (attack_payload))
                self.request(method=http_method, url=temp_url, json=json.loads(payload), headers=temp_headers)
            
            req = requests.get(check_bilnd_poc_url, headers={"token": hunter_log_api_token})
            response = req.json()
            
            if "status" in response and response["status"] == 200:
                self.result['status'] = True
                self.result['info'] = '%s 存在一个命令执行漏洞' % request_raw['url']
                self.result['payload'] = payload
                    
                        
        :return: 
        """
        system_config_single = SystemConfigService.get_single_instance(refresh=True)
        hunter_log_socket_switch = system_config_single.hunter_log_socket_switch
        hunter_log_dns_switch = system_config_single.hunter_log_dns_switch
        plugin_uuid = self.generate_uuid()

        # 生成poc , hunetr log平台查询api url，和 hunter_log 平台api 的查询token
        blind_poc = {"type": "dns", "data": None, "uuid": plugin_uuid}
        check_bilnd_poc_url = self.generate_check_bilnd_poc_url(system_config_single, plugin_uuid)
        hunter_log_api_token = system_config_single.hunter_log_token
        data = None
        if hunter_log_dns_switch:
            blind_poc["type"] = "dns"
            data = "%s.%s" % (plugin_uuid, system_config_single.hunter_log_dns_fake_root_domain)
        elif not hunter_log_dns_switch and hunter_log_socket_switch:
            blind_poc["type"] = "socket"
            data = {"host": system_config_single.hunter_log_socket_host,
                    "port": system_config_single.hunter_log_socket_port, "uuid": plugin_uuid}

        blind_poc["data"] = data
        return blind_poc, check_bilnd_poc_url, hunter_log_api_token

    def generate_check_bilnd_poc_url(self, system_config_single, plugin_uuid):
        """
        生成 hunetr log平台查询api url
        :param hunter_api_url: 
        :param plugin_uuid: 
        :return: 
        """
        if str(system_config_single.hunter_api_url).endswith("/"):
            check_bilnd_poc_url = "{}{}".format(system_config_single.hunter_api_url, plugin_uuid)
        else:
            check_bilnd_poc_url = "{}/{}".format(system_config_single.hunter_api_url, plugin_uuid)
        return check_bilnd_poc_url

    @staticmethod
    def get_parser_name(request_raw):
        """
        获取解析器名
        :param request_raw: 
        :return: 
        """
        parser_name = request_raw["parser"] if "parser" in request_raw else BaseTrafficParser.CHROME_PARSER
        return parser_name

    @staticmethod
    def get_parser_class(request_raw):
        """
        根据名字获得解析器类
        :return: 
        """
        parser_name = BaseChecker.get_parser_name(request_raw)
        parser_class = BaseChecker.PARSER_DIC[parser_name]
        return parser_class

    def record_payload(self, request_raw):
        """
        记录最终发送的payload数据包，展现原生数据格式
        :return: 
        """
        pass
