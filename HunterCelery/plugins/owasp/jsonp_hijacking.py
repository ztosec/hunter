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
import json
import urllib3

urllib3.disable_warnings()
import requests
from common.http_util import HttpMethod, header_to_lowercase
from json.decoder import JSONDecodeError
from plugins.base.vuln_enum import VulnType
from plugins.base.base_checker import BaseChecker


class Checker(BaseChecker):
    def check_logic(self, request_raw):
        """
        检测逻辑，jsonp 水坑攻击只会存在于GET请求中，检测方式，看能否自定义设置CALLBACK
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
                url = str(temp_url).replace(parameters["callback"], "hunter_jsonp")
                try:
                    req = requests.get(url=url, headers=temp_headers, timeout=5)
                    response_content = req.content.decode("utf-8")
                    response_json = re.findall(r'hunter_jsonp\(([\s\S\u4e00-\u9fa5]*)\)', response_content, re.S)[0]
                    response_json = json.loads(response_json)
                    self.result['status'] = True
                    self.result['info'] = '%s 存在一个jsonp劫持漏洞' % request_raw['url']
                    self.result['payload'] = "访问: %s" % url
                except (IndexError, JSONDecodeError) as e:
                    if str(e) not in self.result['error']:
                        self.result['error'].append(str(e))

    # 插件信息
    def init_plugin_info(self):
        """
        初插件始化信息
        :return: 
        """
        tag = "owasp"
        name = "jsonp_hijacking"
        imp_version = "所有版本"
        description = "JSON劫持又称JSON Hijacking, 由于同源策略配置不当，导致外部网页可以恶意直接访问接口数据,参考链接http://wiki." \
                      "dev.ztosys.com/pages/viewpage.action?pageId=21743542"
        repair = "限制请求来源"
        type = VulnType.JSONP
        author = "b5mali4"
        temp_info = {"repair": repair, "name": name, "type": type, "description": description,
                     "imp_version": imp_version, "author": author, "tag": tag}
        self.info = dict(self.info, **temp_info)
