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
import urllib3

urllib3.disable_warnings()
import requests
from common.http_util import get_top_domain, header_to_lowercase, ContentType, UserAgent
from plugins.base.vuln_enum import VulnType
from plugins.base.base_checker import BaseChecker
from parser.chrome_traffic_parser import ChromeTrafficParser
from parser.base_traffic_parser import BaseTrafficParser


class Checker(BaseChecker):
    def check_logic(self, request_raw):
        """
        cors 检测漏洞模块
        作用域: request  header
        增加 origin:*.xx*.com来看具体的结果，因为有些可以绕过正则
        """
        origins = ["b{}".format(get_top_domain(request_raw['url'])), "NULL"]
        http_method = str(request_raw["method"]).lower()
        temp_url = str(request_raw["url"]).strip()
        temp_headers = header_to_lowercase(json.loads(request_raw['headers']))
        content_type = temp_headers[
            "content-type"] if temp_headers is not None and ContentType.NAME.lower() in temp_headers else None
        temp_data = request_raw['data'] if "data" in request_raw else None

        if "User-Agent" not in temp_headers:
            temp_headers['User-Agent'] = UserAgent.PCDevices.CHROME_MAC
        response = None
        for origin in origins:
            temp_headers['Origin'] = origin
            if BaseChecker.get_parser_name(request_raw) == BaseTrafficParser.CHROME_PARSER:
                raw_data = ChromeTrafficParser.to_raw(temp_url, temp_data, http_method, content_type)
            elif BaseChecker.get_parser_name(request_raw) == BaseTrafficParser.DEAFAULT_PARSER:
                raw_data = {"url": temp_url, "data": temp_data, "http_method": http_method,
                            "content_type": content_type}

            try:
                response = requests.request(method=raw_data["http_method"], url=raw_data['url'],
                                            data=raw_data["data"].encode('utf-8'), headers=temp_headers, timeout=5)

                # 判断是否为静态文件
                if response and "Content-Type" in response.headers and response.headers["Content-Type"].split(";")[
                    0] in ContentType.StaticResourceContentType.static_resource_list:
                    return
                if response and "Access-Control-Allow-Origin" in response.headers and (
                        response.headers['Access-Control-Allow-Origin'] == "*" or response.headers[
                    "Access-Control-Allow-Origin"] == origin):
                    self.result['status'] = True
                    self.result['info'] = '%s 存在一个cors漏洞' % request_raw['url']
                    self.result['payload'] = "origin: %s" % origin
            except Exception:
                pass

    def init_plugin_info(self):
        tag = "owasp"
        name = "cors"
        imp_version = "所有版本"
        description = "由于配置不当，导致可以通过设置Origin来控制Access-Control-Allow-Origin,参考链接" \
                      "http://wiki.dev.ztosys.com/pages/viewpage.action?pageId=21743499"
        repair = "将Access-Control-Allow-Origin强制设置为目标子域名"
        type = VulnType.CORS
        author = "b5mali4"
        temp_info = {"repair": repair, "name": name, "type": type, "description": description,
                     "imp_version": imp_version, "author": author, "tag": tag}
        self.info = dict(self.info, **temp_info)
