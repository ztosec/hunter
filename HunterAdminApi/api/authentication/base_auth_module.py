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
支持自定义认证模块，需要做如下两件事，实现check_authentication函数，然后做认证判断，如果认证失败则跳转到自定义路由，需要自己实现并注入到flask

Simple AuthModule example code:

@ldap_web_api.route('/login/', methods=['POST'])
def ldap_authorization():
    pass

class LdapAuthModule(BaseAuthModule):
    def __init__(self):
        self.auth_redirect_url = "/login"

"""
import threading
from common import log
from model.default_value import Role
from model.task import TaskService
from flask import jsonify, session
from abc import ABCMeta, abstractmethod
from api.service.redis_service import RedisService
from exception.hunter_web_exception import UserNotFoundInRedisException

logger = log.getLogger(__name__)


class BaseAuthModule(object):
    __metaclass__ = ABCMeta

    @staticmethod
    def authorize_route():
        """
        auth_redirect_url对应前端页面中登录路由处理逻辑
        :return: 
        """
        pass

    def check_authentication(self, role=Role.USER):
        """
        统一的权限登录认证模块，可以自定义sso认证，ldap认证，多因子认证者其他认证方式，写好逻辑之后需要注册进来，未授权跳转到auth_redirect_url对应的前端页面
        :param role: 
        :return: 
        """

        def _check_account(func):
            def __check_account(*args, **kwargs):

                current_user_name = session.get("user_name")
                if current_user_name is None:  # session过期或者根本没有登录
                    return jsonify(status=403, message="会话失效",
                                   data={"extra_info": "session非法或者已过期,请重新授权登录", "site": self.auth_redirect_url})
                try:
                    role_legal = BaseAuthModule.valid_role(current_user_name, role)
                    if role_legal:
                        return func(*args, **kwargs)
                    else:
                        return BaseAuthModule.generate_invalid_permission_rep(self.auth_redirect_url)
                except Exception as e:
                    logger.exception("ldap raise error")
                    if isinstance(e, UserNotFoundInRedisException):
                        return jsonify(status=403, message="会话失效",
                                       data={"extra_info": "session非法或者已过期,请重新授权登录", "site": self.auth_redirect_url})
                    else:
                        return jsonify(status=500, message="未知异常", data={"extra_info": "发生未知异常，请联系管理员查看异常日志"})

            return __check_account

        return _check_account

    @staticmethod
    def modify_user_info_cache_session(user_name, db_user):
        """
        认证成功之后，修改redis中用户信息并设置session
        :return: 
        """
        # 存入到redis，和数据库中的数据一致，用户id是最关键的
        RedisService.update_user(user_name,
                                 {"id": db_user.id, "user_name": db_user.user_name, "full_name": db_user.full_name,
                                  "dept_name": db_user.dept_name, "role": db_user.role,
                                  "mobile_phone": db_user.mobile_phone, "email": db_user.email})
        try:
            current_task = TaskService.get_working_tasks(user_id=db_user.id)[0]
            RedisService.update_user(user_name, {"current_task_id": current_task.id})
        except IndexError:
            pass
        # 设置session
        session["user_name"] = user_name

    @staticmethod
    def valid_role(current_user_name, role):
        """
        判断当前用户权限是否符合API权限
        如果用户登录过期，直接抛出异常，不同的登录认证方式自己可以做跳转之类的工作
        :param current_user_name: 
        :param role: 
        :return: 
        """
        try:
            user = RedisService.get_user(user_name=current_user_name)
            return int(user.role) >= role
        except Exception as e:
            raise e

    @staticmethod
    def generate_invalid_permission_rep(redirect_url):
        """
        当前用户权限和api所需要的权限不符合
        :param redirect_url: 跳转到认证的api
        :return: 
        """
        return jsonify(status=403, message="访问非法", data={"extra_info": "当前用户没有权限操作此API", "site": redirect_url})

    @staticmethod
    def generate_cookie_invalid_rep(redirect_url):
        """
        cookie过期无效响应
        :param redirect_url: 
        :return: 
        """
        return jsonify(status=403, message="会话失效", data={"extra_info": "session非法或者已过期,请重新授权登录", "site": redirect_url})
