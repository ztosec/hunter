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
内置的账号密码登录
"""
from common import log
from flask import request, jsonify, Blueprint
from api.authentication.base_auth_module import BaseAuthModule
from common.config_util import get_system_config
from model.user import User, UserService

logger = log.getLogger(__name__)
account_web_api = Blueprint('account_web_api', __name__, url_prefix="/api/v1/account/")


class DefaultAuthModule(BaseAuthModule):
    """
    使用HUNTER内置的账号密码体系认证，账号密码登录认证方式
    """

    def __init__(self):
        self.auth_redirect_url = "/login"

    @staticmethod
    @account_web_api.route('/login/', methods=['POST'])
    def authorize_route():
        """
        基础账号密码认证体系
        :return: 
        """
        try:
            post_data = request.get_json(force=True)
            post_user_name = post_data.get("user_name")
            post_pass_word = post_data.get("pass_word")

            if UserService.count(where=(User.user_name == post_user_name, User.pass_word == post_pass_word)) <= 0:
                return jsonify(status=403, message="认证出错", data={"extra_info": "账号密码登录出错", "site": "/login"})

            db_user = UserService.get_fields_by_where(where=(User.user_name == post_user_name, User.pass_word == post_pass_word))[0]

            BaseAuthModule.modify_user_info_cache_session(user_name=db_user.user_name, db_user=db_user)
            return jsonify(status=200, message="认证成功",
                           data={"extra_info": "稍后自动跳转首页,请耐心等待", "site": get_system_config()['front_end']['index']})
        except Exception as e:
            logger.exception("auth_account raise error")
            return jsonify(status=500, message="未知异常", data={"extra_info": "发生未知异常，请联系管理员查看异常日志"})
