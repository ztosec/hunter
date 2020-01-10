#!/ usr/bin/env
# coding=utf-8
#
# Copyright 2019 ztosec & https://sec.zto.com/
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
import os
import re
import base64
import json
import sys
import tornado.httpserver
import tornado.ioloop
import tornado.iostream
import tornado.web
import tornado.curl_httpclient

try:
    from common import log
except (ModuleNotFoundError, ImportError):
    HUNTER_PATH = "{}/../".format(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, HUNTER_PATH)
finally:
    from common import log
    from hunter_celery import scan_celery
    from networkproxy import CACERT_FILE
    from networkproxy import CERTKEY_FILE
    from networkproxy import CAKEY_FILE
    from networkproxy.socket_wrapper import wrap_socket
    from model.network_proxy import NetWorkProxyConfig, NetWorkProxyConfigService
    from networkproxy.authentication import auth_login
    from api.service.redis_service import RedisService
    from model.default_value import TaskStatus
    from common.path import HUNTER_PATH
    from common.http_util import StatusCode
    from networkproxy.proxy_handler import ProxyHandler
    from networkproxy import get_http_server
    from networkproxy import set_http_server

logger = log.get_default_logger()


class HunterHandler(ProxyHandler):
    def request_handler(self, request, user_info):
        """
        将请求发送到MQ中
        :param request: 
        :return: 
        Simple example code:

        print(request.body_arguments)
        print(request.headers)
        print(request.body)
        print(request.cookies)
        print(request.version)
        print(request.protocol)
        print(request.host_name)
        print(request.uri)
        print(request.method)
        """
        if not user_info:
            return
        task_id = user_info.current_task_id
        current_user_name = user_info.user_name
        raw_request_data = self.wrap_request(request, user_info)

        # 是否为满足条件的请求
        current_task = RedisService.get_task(task_id)
        if current_task and "hook_rule" in current_task:
            # *.xx.com
            hook_rule = str(current_task.hook_rule).replace("*", ".*")
            if not str(raw_request_data["data"]["url"]).startswith(hook_rule) and re.match(r'' + hook_rule,
                                                                                           raw_request_data["data"][
                                                                                               "url"], re.S) is None:
                return

        if RedisService.create_urlclassifications(task_id, raw_request_data):
            logger.info("满足正则条件,发送流量到MQ中")
            scan_celery.delay(raw_request_data["data"], task_id, current_user_name, TaskStatus.NONE)

    def wrap_request(self, request, user_info):
        """
        转换请求数据格式
        :param request: 
        :return: 
        """
        from parser.base_traffic_parser import BaseTrafficParser
        raw_request_data = dict()
        url = request.uri
        if url is None or not url.startswith("http"):
            url = request.protocol + "://" + request.host_name + request.uri
        method = request.method
        headers = request.headers._dict
        request_wraper = {"data": request.body.decode("utf-8"), "type": "hunter-proxy", "url": url, "method": method,
                          "parser": BaseTrafficParser.DEAFAULT_PARSER,
                          "headers": json.dumps(headers), "requestid": None}
        raw_request_data["data"] = request_wraper
        return raw_request_data

    def retrieve_credentials(self):
        """
        弹出账号密码基础认证，成功则写session
        :return: 
        """
        auth_header = self.request.headers.get('Authorization', None)
        proxy_session_id = self.get_cookie('proxy_sessionid', None)

        if auth_header is not None:
            # Basic Zm9vOmJhcg==
            auth_mode, auth_base64 = auth_header.split(' ', 1)
            assert auth_mode == 'Basic'
            auth_username, auth_password = base64.b64decode(auth_base64).decode("UTF-8").split(':', 1)
            status, user_info = auth_login(auth_username, auth_password, proxy_session_id)
            # 认证失败
            if not status:
                self.write("认证失败,请确认账号密码是否正确")
                self.set_status(401)
                self.set_header('WWW-Authenticate', 'Basic realm="hunter"')
            else:
                self.set_cookie("proxy_sessionid", user_info["proxy_sessionid"])
                # 任务状态为关闭，或者任务不存在
                if "current_task_id" not in user_info or ("current_task_id" in user_info
                                                          and user_info["current_task_id"] != ""
                                                          and RedisService.get_task(
                        user_info.current_task_id).status != str(TaskStatus.WORKING)):
                    self.write("后台无正在运行的任务,你需要重建一个新任务")
                    self.set_status(400)
                    self.finish()
                    status = False
            return status, user_info
        else:
            self.set_status(401)
            self.set_header('WWW-Authenticate', 'Basic realm="hunter"')
            self.finish()
            return False, None

    def show_cacert_page(self):
        """
        下载CA证书
        :return: 
        """
        html_content = """

               <html><head><title>Burp Suite Professional</title>
               <style type="text/css">
               body { background: #dedede; font-family: Arial, sans-serif; color: #404042; -webkit-font-smoothing: antialiased; }
               #container { padding: 0 15px; margin: 10px auto; background-color: #ffffff; }
               a { word-wrap: break-word; }
               a:link, a:visited { color: #e06228; text-decoration: none; }
               a:hover, a:active { color: #404042; text-decoration: underline; }
               h1 { font-size: 1.6em; line-height: 1.2em; font-weight: normal; color: #404042; }
               h2 { font-size: 1.3em; line-height: 1.2em; padding: 0; margin: 0.8em 0 0.3em 0; font-weight: normal; color: #404042;}
               .title, .navbar { color: #ffffff; background: #70BAFE; padding: 10px 15px; margin: 0 -15px 10px -15px; overflow: hidden; }
               .title h1 { color: #ffffff; padding: 0; margin: 0; font-size: 1.8em; }
               div.navbar {position: absolute; top: 18px; right: 25px;}div.navbar ul {list-style-type: none; margin: 0; padding: 0;}
               div.navbar li {display: inline; margi-left: 20px;}
               div.navbar a {color: white; padding: 10px}
               div.navbar a:hover, div.navbar a:active {text-decoration: none; background: #404042;}
               </style>
               </head>
               <body>
               <div id="container">
               <div class="title"><h1>Hunter Proxy</h1></div>
               <div class="navbar"><ul>
               <li><a href="/cert">CA Certificate</a></li>
               </ul></div>
               <p>Welcome to Hunter Proxy.</p><p>&nbsp;</p>
               </div>
               </body>
               </html>

               """
        self.set_status(200)
        self.write(html_content)
        self.finish()

    def download_cacert(self):
        """
        下载证书
        :return: 
        """
        self.set_header('Content-Type', 'application/octet-stream')
        self.set_header('Content-Disposition', 'attachment; filename=ca.crt')
        # 读取的模式需要根据实际情况进行修改
        with open(CACERT_FILE, 'rb') as f:
            while True:
                data = f.read(1)
                if not data:
                    break
                self.write(data)
        self.finish()

    def handle_hunter_cacert_page(self):
        """
        处理证书页面
        :return: 
        """
        if self.request.host == "hunterca":
            if self.request.uri == "http://hunterca/cert":
                self.download_cacert()
            else:
                self.show_cacert_page()
            return

    def handle_hunter_authentication_record(self):
        """
        处理认证，保存流量到mq
        :return: 
        """
        user_info = None
        # 只对非白名单其属于要测试站点等我 开启401认证
        if not NetWorkProxyConfigService.is_white_hosts(self.request.host):
            status, user_info = self.retrieve_credentials()
            if not status or user_info is None:
                return
                # Hook request
        self.request_handler(self.request, user_info)

    @tornado.web.asynchronous
    def get(self):
        """
        下载证书页面
        :return: 
        """
        self.handle_hunter_cacert_page()
        self.handle_hunter_authentication_record()
        ProxyHandler.get(self)
