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
ldap登录认证，可以直接现实，推荐使用后台默认ldap同步模块
"""
from common import log
from flask import request, jsonify, Blueprint
from ldap3 import Server, Connection, SUBTREE
from model.user import User, UserService
from model.ldap_config import LdapConfigService
from common.config_util import get_system_config
from api.authentication.base_auth_module import BaseAuthModule

logger = log.getLogger(__name__)
ldap_web_api = Blueprint('ldap_web_api', __name__, url_prefix="/api/v1/ldap/")
LDAP_OP_TIMEOUT = 10


def ldap_auth(user_name, password):
    """
    登录账号密码进行验证
    :param user_name: 
    :param pass_word: 
    :return: 
    """
    try:
        ldap_config = LdapConfigService.get_single_instance()
        # 认证账号密码
        ldap_server_pool = Server(ldap_config.ldap_host, connect_timeout=LDAP_OP_TIMEOUT)
        bind_dn = ldap_config.bind_dn
        bind_dn_password = ldap_config.bind_dn_password
        base_dn = ldap_config.base_dn
        search_filter = ldap_config.search_filter
        # 映射的字段
        user_name_field = ldap_config.user_name_field
        full_name_field = ldap_config.full_name_field
        email_field = ldap_config.email_field
        dept_name_field = ldap_config.dept_name_field
        mobile_field = ldap_config.mobile_field

        conn = Connection(ldap_server_pool, user=bind_dn, password=bind_dn_password, check_names=True, lazy=False,
                          raise_exceptions=True)
        conn.open()
        conn.bind()
        # (&(objectclass=person)(sAMAccountName={user_name}))
        searchFilter = search_filter.format(user_name=user_name)
        res = conn.search(
            search_base=base_dn,
            search_filter=searchFilter,
            search_scope=SUBTREE,
        )
        if res:
            entry = conn.response[0]
            dn = entry['dn']
            attr_dict = entry['attributes']
            conn2 = Connection(ldap_server_pool, user=dn, password=password, check_names=True, lazy=False,
                               raise_exceptions=True)
            conn2.bind()
            if conn2.result["description"] == "success":
                return True, {"user_name": "".join(attr_dict[user_name_field]),
                              "full_name": "".join(attr_dict[full_name_field]),
                              "email": "".join(attr_dict[email_field]),
                              "dept_name": "".join(attr_dict[dept_name_field]) if dept_name_field in attr_dict else "",
                              "mobile": "".join(attr_dict[mobile_field])}
        return False, None
    except Exception:
        logger.exception("ldap_auth raise error")
        return False, None


class LdapAuthModule(BaseAuthModule):
    def __init__(self):
        self.auth_redirect_url = "/login"

    @staticmethod
    @ldap_web_api.route('/login/', methods=['POST'])
    def authorize_route():
        """
        ldap认证账号体系
        :return: 
        """
        try:
            post_data = request.get_json(force=True)
            post_user_name = post_data.get("user_name")
            post_pass_word = post_data.get("pass_word")
            ldap_config = LdapConfigService.get_single_instance()
            if ldap_config.ldap_switch is False:
                return jsonify(status=500, message="登录失败", data={"extra_info": "不支持ldap认证，请后台配置并开启ldap模块"})

            status, result_dict = ldap_auth(post_user_name, post_pass_word)
            if status:
                user_name = result_dict["user_name"]
                # 保存更新数据库和Redis
                if UserService.count(where=(User.user_name == user_name)) <= 0:
                    UserService.save(user_name=result_dict["user_name"],
                                     full_name=result_dict["full_name"],
                                     dept_name=result_dict["dept_name"],
                                     email=result_dict["email"],
                                     mobile_phone=result_dict["mobile"])
                else:
                    UserService.update(fields=({User.full_name: result_dict["full_name"],
                                                User.dept_name: result_dict["dept_name"],
                                                User.email: result_dict["email"],
                                                User.mobile_phone: result_dict["mobile"]}),
                                       where=(User.user_name == user_name))

                db_user = UserService.get_fields_by_where(where=(User.user_name == user_name))[0]
                BaseAuthModule.modify_user_info_cache_session(user_name=db_user.user_name, db_user=db_user)
                return jsonify(status=200, message="认证成功",
                               data={"extra_info": "稍后自动跳转首页,请耐心等待", "site": get_system_config()['front_end']['index']})

            return jsonify(status=403, message="认证出错", data={"extra_info": "账号密码登录出错", "site": "/login"})

        except Exception as e:
            logger.exception("auth_account raise error")
            return jsonify(status=500, message="未知异常", data={"extra_info": "发生未知异常，请联系管理员查看异常日志"})