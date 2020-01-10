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
from common.http_util import header_to_lowercase, ContentType
from common.config_util import get_weak_password_list
from plugins.base.vuln_enum import VulnType
from plugins.base.base_checker import BaseChecker
from parser.base_traffic_parser import BaseTrafficParser


class Checker(BaseChecker):
    def check_logic(self, request_raw):
        """
        检测password字段是否为弱密码
        :param package: 
        :return: 
        """
        http_method = str(request_raw["method"]).lower()
        temp_url = str(request_raw["url"]).strip()
        temp_headers = header_to_lowercase(json.loads(request_raw['headers']))
        content_type = temp_headers[
            "content-type"] if temp_headers is not None and ContentType.NAME.lower() in temp_headers else None
        temp_data = request_raw['data'] if "data" in request_raw else None
        http_parameter = self.get_parser_class(request_raw).get_parameter(url=temp_url, data=temp_data,
                                                                          http_method=http_method,
                                                                          content_type=content_type)
        for key, value in http_parameter.items():
            if key.lower() in ["pass", "password", "pass_word", "passwd"]:
                if self.is_weak_password(http_parameter[key]):
                    self.result['status'] = True
                    self.result['info'] = '%s 存在一个weak_pass漏洞' % request_raw['url']
                    self.result['payload'] = http_parameter
                    return

    def init_plugin_info(self):
        tag = "owasp"
        name = "weak_pass"
        imp_version = "所有版本"
        description = "不能将密码设置为弱密码,这样可能会存在账号被泄漏的风险参考链接http://wiki.dev.ztosys.com/pages/viewpage.action?pageId=21732575"
        repair = "设置为强密码"
        type = VulnType.WEAK_PWD
        author = "b5mali4"
        temp_info = {"repair": repair, "name": name, "type": type, "description": description,
                     "imp_version": imp_version, "author": author, "tag": tag}
        self.info = dict(self.info, **temp_info)

    def is_weak_password(self, password, username=None):
        """
        检查是否为弱密码
        :param password: 
        :return: 
        """
        weak_password_list = get_weak_password_list()
        if username is not None:
            weak_password_list += [username + weak_password for weak_password in weak_password_list]
            weak_password_list += [weak_password + username for weak_password in weak_password_list]
            weak_password_list += [weak_password + "+" + username for weak_password in weak_password_list]
        for weak_password in weak_password_list:
            if password == weak_password:
                return True

        return False
