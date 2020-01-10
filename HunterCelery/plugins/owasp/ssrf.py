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
import urllib3

urllib3.disable_warnings()
import json
import requests
from common import http_util
from urllib import parse
from plugins.base.vuln_enum import VulnType
from plugins.base.base_checker import BaseChecker


class Checker(BaseChecker):
    def check_logic(self, request_raw):
        """
        1.抓取到请求，获取参数
        2.将参数逐个换成检测连接
        :param request_raw: 
        :return: 
        """
        http_method = str(request_raw["method"]).lower()
        temp_url = str(request_raw["url"]).strip()
        temp_headers = http_util.header_to_lowercase(json.loads(request_raw['headers']))
        content_type = temp_headers[
            "content-type"] if temp_headers is not None and http_util.ContentType.NAME.lower() in temp_headers else None
        temp_data = request_raw['data'] if "data" in request_raw else None

        # 获取检测api
        blind_poc, check_bilnd_poc_url, hunter_log_api_token = self.generate_blind_poc()
        if not blind_poc["data"]:
            return

        if blind_poc["type"] == "dns":
            attack_payload = "http://%s" % (blind_poc["data"])  # 得到的是一个域名，域名前缀为uuid
        elif blind_poc["type"] == "socket":
            attack_payload = "http://%s:%s/%s" % (
            blind_poc["data"]["host"], blind_poc["data"]["port"], blind_poc["data"]["uuid"])

        try:
            payload = self.get_parser_class(request_raw).add_poc_data(url=temp_url, data=temp_data,
                                                                      http_method=http_method,
                                                                      content_type=content_type,
                                                                      poc="%s " % (attack_payload))
            requests.request(method=payload["http_method"], url=payload["url"], data=payload["data"],
                             headers=temp_headers, timeout=5, verify=False)
        except Exception:
            pass

        req = requests.get(check_bilnd_poc_url, headers={"token": hunter_log_api_token}, timeout=5)
        if req:
            response = req.json()
            if "status" in response and response["status"] == 200:
                self.result['status'] = True
                self.result['info'] = '%s 存在一个ssrf漏洞' % request_raw['url']
                self.result['payload'] = payload

    def init_plugin_info(self):
        tag = "owasp"
        name = "ssrf"
        imp_version = "所有版本"
        description = "SSRF 形成的原因大都是由于服务端提供了从其他服务器应用获取数据的功能，且没有对目标地址做过滤与限制,参考链接 " \
                      "https://www.freebuf.com/column/157466.html"
        repair = "过滤"
        type = VulnType.SSRF
        author = "b5mali4"
        temp_info = {"repair": repair, "name": name, "type": type, "description": description,
                     "imp_version": imp_version, "author": author, "tag": tag}
        self.info = dict(self.info, **temp_info)
