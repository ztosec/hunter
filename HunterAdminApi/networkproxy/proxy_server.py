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
To use:
>>> python proxy_server.py
"""
import os
import re
import ssl
import sys
import json
import base64
import socket
import threading
import tornado.httpserver
import tornado.ioloop
import tornado.iostream
import tornado.web
import tornado.curl_httpclient
import tornado.escape
import tornado.httputil

try:
    from common import log
except (ModuleNotFoundError, ImportError):
    HUNTER_PATH = "{}/../".format(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, HUNTER_PATH)
finally:
    from common import log
    from hunter_celery import scan_celery
    from networkproxy.socket_wrapper import wrap_socket
    from model.network_proxy import NetWorkProxyConfig, NetWorkProxyConfigService
    from networkproxy.authentication import auth_login
    from api.service.redis_service import RedisService
    from model.default_value import TaskStatus
    from common.path import HUNTER_PATH
    from common.http_util import StatusCode
    from networkproxy.proxy_handler import ProxyHandler
    from networkproxy.hunter_handler import HunterHandler
    from networkproxy import get_http_server
    from networkproxy import set_http_server

logger = log.get_default_logger()


class ProxyServer(object):
    _instance_lock = threading.Lock()

    def __init__(self, inbound_ip="0.0.0.0", inbound_port=8088, outbound_ip=None, outbound_port=None, visited=False):
        self.application = tornado.web.Application(handlers=[(r".*", HunterHandler)], debug=False, gzip=True)
        self.application.inbound_ip = inbound_ip
        self.application.inbound_port = inbound_port
        self.application.outbound_ip = outbound_ip
        self.application.outbound_port = outbound_port
        self.server = tornado.httpserver.HTTPServer(self.application, decompress_request=True)
        set_http_server(self.server)
        self.show_tornado_logger(visited)

    def start(self, instances=1, visited=False):
        logger.info("proxy启动中，监听{}.....".format(self.application.inbound_port))
        try:
            self.server.bind(self.application.inbound_port, address=self.application.inbound_ip)
            self.server.start(instances)
            tornado.ioloop.IOLoop.instance().start()
        except Exception as e:
            logger.exception("proxy启动失败.....")

    def stop(self):
        try:
            tornado.ioloop.IOLoop.instance().stop()
            logger.info("proxy关闭成功.....")
        except Exception as e:
            logger.exception("proxy关闭失败.....")

    @staticmethod
    def instance():
        """
        获取单例
        :return: 
        """
        if not hasattr(ProxyServer, "_instance"):
            with ProxyServer._instance_lock:
                if not hasattr(ProxyServer, "_instance"):
                    ProxyServer._instance = ProxyServer(ProxyHandler)
        return ProxyServer._instance

    @staticmethod
    def initialized():
        return hasattr(ProxyServer, "_instance")

    def show_tornado_logger(self, visited=False) -> None:
        """
        屏蔽tornado原有的log模块
        :return: 
        """
        import logging
        null_handler = logging.NullHandler()
        null_handler.setLevel(logging.DEBUG)
        logging.getLogger("tornado.access").addHandler(null_handler)
        logging.getLogger("tornado.access").propagate = False


if __name__ == "__main__":
    try:
        proxy = ProxyServer()
        proxy.start()
    except KeyboardInterrupt:
        proxy.stop()
