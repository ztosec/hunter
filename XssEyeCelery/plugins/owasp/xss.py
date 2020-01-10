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
from plugins.base.vuln_enum import VulnType
from plugins.base.base_checker import BaseChecker


class Checker(BaseChecker):
    """
    xss 检测插件，使用chromeheadless来检测xss
    """

    def init_plugin_info(self):
        """
        初始化xssfork检测插件
        :return: 
        """
        tag = "owasp"
        name = "xsseye"
        imp_version = "所有版本"
        description = "XSS攻击全称跨站脚本攻击，XSS是一种在web应用中的计算机安全漏洞，它允许恶意web用户将代码植入到提供给其它用户使用的页面中m，详情请参考http://wiki.dev.ztosys.com/pages/viewpage.action?pageId=21743578"
        repair = "过滤掉<,>,',等特殊字符"
        type = VulnType.XSS
        author = "b5mali4"
        temp_info = {"repair": repair, "name": name, "type": type, "description": description,
                     "imp_version": imp_version, "author": author, "tag": tag}
        self.info = dict(self.info, **temp_info)

    def check_logic(self, request_raw):
        pass
