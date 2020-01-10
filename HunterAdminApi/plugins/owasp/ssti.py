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
from plugins.base.vuln_enum import VulnType
from plugins.base.base_checker import BaseChecker


class Checker(BaseChecker):
    def check_logic(self, request_raw):
        """
        比较多步骤 1.判断是 {{ '7'*7 }} ,${{ '7'*7 }} {'7'*7} ${'7'*7} ('7'*7)  $('7'*7) $(('7'*7)) (('7'*7))是否变成 7777777
        :param request_raw: 
        :return: 
        """
        http_method = str(request_raw["method"]).lower()
        temp_url = str(request_raw["url"]).strip()
        temp_headers = http_util.header_to_lowercase(json.loads(request_raw['headers']))
        content_type = temp_headers[
            "content-type"] if temp_headers is not None and http_util.ContentType.NAME.lower() in temp_headers else None
        temp_data = request_raw['data'] if "data" in request_raw else None

        operation_result = "7777777"
        for ssti_inject_poc in ["{{ '7'*7 }}", "${{ '7'*7 }}", "{'7'*7}", "${'7'*7}", "('7'*7)", "$('7'*7)",
                                "$(('7'*7))", "(('7'*7))"]:
            payload = self.get_parser_class(request_raw).add_poc_data(url=temp_url, data=temp_data,
                                                                      http_method=http_method,
                                                                      content_type=content_type, poc=ssti_inject_poc)
            req = None
            try:
                req = requests.request(method=payload["http_method"], url=payload["url"], data=payload["data"],
                                       headers=temp_headers, timeout=5, verify=False)
            except Exception:
                pass
            if req:
                res_content = req.content.decode("utf-8")
                if res_content and operation_result in res_content:
                    self.result['status'] = True
                    self.result['info'] = '%s 存在一个模版注入漏洞' % request_raw['url']
                    self.result['payload'] = payload
                    return

    def init_plugin_info(self):
        tag = "owasp"
        author = "b5mali4"
        name = "ssti"
        imp_version = "所有版本"
        description = "由于过滤不当，导致模版注入，可以通过控制参数执行任意代码,参考链接" \
                      "http://wiki.dev.ztosys.com/pages/viewpage.action?pageId=25270159"
        repair = "过滤参数"
        type = VulnType.CMD_ECT
        temp_info = {"repair": repair, "name": name, "type": type, "description": description,
                     "imp_version": imp_version, "author": author, "tag": tag}
        self.info = dict(self.info, **temp_info)
