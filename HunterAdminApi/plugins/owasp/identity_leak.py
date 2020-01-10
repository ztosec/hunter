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
import re
import ssl
import urllib3

urllib3.disable_warnings()
import json
import requests
from common import http_util
from plugins.base.vuln_enum import VulnType
from plugins.base.base_checker import BaseChecker
from parser.base_traffic_parser import BaseTrafficParser
from parser.chrome_traffic_parser import ChromeTrafficParser


class Checker(BaseChecker):
    def check_logic(self, request_raw):
        """
        检测响应中是否泄漏身份证
        :param request_raw: 
        :return: 
        """
        http_method = str(request_raw["method"]).lower()
        temp_url = str(request_raw["url"]).strip()
        temp_headers = http_util.header_to_lowercase(json.loads(request_raw['headers']))
        content_type = temp_headers[
            "content-type"] if temp_headers is not None and http_util.ContentType.NAME.lower() in temp_headers else None
        temp_data = request_raw['data'] if "data" in request_raw else None
        if BaseChecker.get_parser_name(request_raw) == BaseTrafficParser.CHROME_PARSER:
            raw_data = ChromeTrafficParser.to_raw(temp_url, temp_data, http_method, content_type)
        else:
            raw_data = {"url": request_raw["url"], "data": request_raw["data"],
                        "http_method": request_raw["http_method"], "content_type": content_type}

        try:
            req = requests.request(method=raw_data["method"], url=raw_data["url"], json=raw_data["data"],
                                   headers=temp_headers, timeout=5)
            if req:
                res_content = req.content.decode("utf-8")
                identity = re.findall(
                    r'(^[1-9]\d{5}(?:18|19|(?:[23]\d))\d{2}(?:(?:0[1-9])|(?:10|11|12))(?:(?:[0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$)',
                    res_content, re.S)

                if identity is None:
                    identity = re.match(
                        r'(^[1-9]\d{5}\d{2}(?:(?:0[1-9])|(?:10|11|12))(?:(?:[0-2][1-9])|10|20|30|31)\d{2}$)',
                        res_content,
                        re.S)

            if identity and len(identity) > 0:
                self.result['status'] = True
                self.result['info'] = '%s 疑似存在一个身份证泄漏' % request_raw['url']
                self.result['payload'] = identity[0]
        except Exception:
            pass

    def init_plugin_info(self):
        """
        初始化信息
        :return: 
        """
        tag = "owasp"
        name = "identity_leak"
        imp_version = "所有版本"
        description = "该接口可能泄漏身份证等敏感信息，详情请参考http://wiki.dev.ztosys.com/pages/viewpage.action?pageId=21732569"
        repair = "对相关数据打码"
        type = VulnType.WEAK_PWD
        author = "b5mali4"
        temp_info = {"repair": repair, "name": name, "type": type, "description": description,
                     "imp_version": imp_version, "author": author, "tag": tag}
        self.info = dict(self.info, **temp_info)
