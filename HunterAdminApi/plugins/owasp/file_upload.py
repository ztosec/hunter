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
from plugins.base.base_checker import BaseChecker
from plugins.base.vuln_enum import VulnType


class Checker(BaseChecker):
    def check_logic(self, request_raw):
        """
        任意文件上传漏洞，不做检测
        :param request_raw: 
        :return: 
        """
        pass

    def init_plugin_info(self):
        tag = "owasp"
        name = "file_upload"
        imp_version = "所有版本"
        description = "该接口存在任意文件上传漏洞，详情请参考http://wiki.dev.ztosys.com/pages/viewpage.action?pageId=49817330"
        repair = "严格过滤"
        type = VulnType.FILE_UPLOAD
        author = "b5mali4"
        temp_info = {"repair": repair, "name": name, "type": type, "description": description,
                     "imp_version": imp_version, "author": author, "tag": tag}
        self.info = dict(self.info, **temp_info)
