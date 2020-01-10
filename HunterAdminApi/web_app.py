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
from flask import Flask, session, Response, jsonify, request, redirect, render_template
from api.hunter_user_web_api import user_web_api
from api.hunter_admin_web_api import admin_web_api
 
from api.authentication.default_auth_module import account_web_api
from api.authentication.ldap_auth_module import ldap_web_api
 

flask_app = Flask(__name__)
# flask_app = Flask(__name__, static_url_path="/static", static_folder="api/resource/templates/")
flask_app.config['SECRET_KEY'] = os.urandom(24)
flask_app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)
# flask_app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))

# 注册到蓝图
flask_app.register_blueprint(user_web_api)
flask_app.register_blueprint(admin_web_api)
 
flask_app.register_blueprint(account_web_api)
flask_app.register_blueprint(ldap_web_api)
 


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
    response.headers["Access-Control-Allow-Headers"] = "Content-Type,x-requested-with"
    return response


@flask_app.route('/', methods=['GET'], endpoint='index')
def index():
    return render_template("index.html")


if __name__ == "__main__":
    flask_app.config['JSON_AS_ASCII'] = False
    flask_app.run(host="0.0.0.0", port=8888)
