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
import os
from datetime import timedelta
from model.user import User
from model.request_log import RequestLog
from model.system_set import SystemSetting
from model.request_log_dup import RequestLogDup
from resolver.dns_server import DnsServer
from resolver.socket_server import TcpServer
from flask import Flask, session, Response, send_file, request
from flask import send_from_directory
from web.api.request_log import request_log
from web.api.request_log_dup import request_log_dup
from web.api.user import user
from web.api.system_set import system_set

flask_app = Flask(__name__, static_url_path="/static", static_folder="web/templates/static/")
flask_app.config['SECRET_KEY'] = os.urandom(24)
flask_app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)

# 注册到蓝图
flask_app.register_blueprint(request_log)
flask_app.register_blueprint(request_log_dup)
flask_app.register_blueprint(user)
flask_app.register_blueprint(system_set)


@flask_app.after_request
def handle_after_request(response):
    """
    设置CORS源
    :param response: 
    :return: 
    """
    if request.headers.has_key("Origin"):
        response.headers["Access-Control-Allow-Origin"] = request.headers["Origin"]
    response.headers["Access-Control-Allow-Methods"] = "GET,POST,PUT,HEAD,OPTIONS,DELETE,PATCH"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response


def print_banner():
    banner = """    
     _   _             _            _                
    | | | |_   _ _ __ | |_ ___ _ __| |    ___   __ _ 
    | |_| | | | | '_ \| __/ _ \ '__| |   / _ \ / _` |
    |  _  | |_| | | | | ||  __/ |  | |__| (_) | (_| |
    |_| |_|\__,_|_| |_|\__\___|_|  |_____\___/ \__, |
                                               |___/ 
    author:b5mali4   version:0.2  License:Apache License 2.0
    """
    print(banner)


if __name__ == "__main__":
    print_banner()
    flask_app.run(host="0.0.0.0", port=8888)
