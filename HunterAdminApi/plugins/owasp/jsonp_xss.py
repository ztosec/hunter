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
import urllib3

urllib3.disable_warnings()
import requests
from common.http_util import header_to_lowercase, HttpMethod
from plugins.base.vuln_enum import VulnType
from json.decoder import JSONDecodeError
from plugins.base.base_checker import BaseChecker


class Checker(BaseChecker):
    def check_logic(self, request_raw):
        """
        检测逻辑
        :param request_raw: 
        :return: 
        """
        http_method = str(request_raw["method"]).lower()
        temp_url = str(request_raw["url"]).strip()
        temp_headers = header_to_lowercase(json.loads(request_raw['headers']))

        if http_method == HttpMethod.GET:
            parameters = self.get_parser_class(request_raw).get_parameter(url=temp_url, data=None,
                                                                          http_method=HttpMethod.GET, content_type=None)
            if parameters is not None and "callback" in parameters:
                url = str(temp_url).replace(parameters["callback"], "<svg/onload=alert(1)>")
                try:
                    req = requests.get(url=url, headers=temp_headers, timeout=5)
                    response_content = req.content.decode("utf-8")
                    response_headers = req.headers
                    if "<svg/onload=alert(1)>" in response_content and ("Content-Type" not in response_headers or (
                                    "Content-Type" in response_headers and "text/html" in response_headers[
                                "Content-Type"])):
                        self.result['status'] = True
                        self.result['info'] = '%s 存在一个jsonp参数可控造成的xss漏洞' % request_raw['url']
                        self.result['payload'] = "访问: %s" % url
                except (JSONDecodeError) as e:
                    if str(e) not in self.result['error']:
                        self.result['error'].append(str(e))

    # 插件信息
    def init_plugin_info(self):
        tag = "owasp"
        name = "jsonp_xss"
        imp_version = "所有版本"
        description = "实现JSONP的时候,response content-type配置成text/html,造成XSS,参考链接http://wiki.dev.ztosys.com/pages" \
                      "/viewpage.action?pageId=21743578"
        repair = "将Content-Type设置为application/json并正确过滤掉可能造成xss的字符<,>,',\"(将其html实体化)"
        type = VulnType.XSS
        author = "b5mali4"
        temp_info = {"repair": repair, "name": name, "type": type, "description": description,
                     "imp_version": imp_version, "author": author, "tag": tag}
        self.info = dict(self.info, **temp_info)
