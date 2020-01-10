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

import string
import random
import hashlib
from common import log
from networkproxy.authentication.ldap_auth import NetWorkProxyLdapAuth
from networkproxy.authentication.account_auth import NetWorkProxyAccountAuth
from model.network_proxy import NetWorkProxyConfig, NetWorkProxyConfigService
from api.service.redis_service import RedisService
from exception.hunter_web_exception import UserNotFoundInRedisException
from exception.hunter_web_exception import BaseHunterException

logger = log.get_default_logger()
__all__ = ["auth_login"]


def generate_session():
    """
    随机生成SESSION
    :return: 
    """
    random_byte = ''.join(random.sample(string.ascii_letters + string.digits + string.punctuation, 32))
    m = hashlib.md5()
    m.update(random_byte.encode("utf-8"))
    return m.hexdigest()


def auth_login(username, password, sessionid):
    """
    代理认证模块，LDAP认证和账户认证，根据开关选择账号认证或者LDAP认证，如果两个开关都开启了，两种方式都支持
    :param role: 
    :return: 
    """
    try:
        user = RedisService.get_user(user_name=username)
        if sessionid and hasattr(user, "proxy_sessionid") and user.proxy_sessionid == sessionid:
            return True, user
        raise UserNotFoundInRedisException("账号%s proxy_sessionid不存在或者认证错误" % username)
    except UserNotFoundInRedisException:
        if auth_login_logic(username, password):
            # 设置proxy_session_id
            proxy_sessionid = generate_session()
            RedisService.update_user(username, {"proxy_sessionid": proxy_sessionid})
            user = RedisService.get_user(user_name=username)
            return True, user
        return False, None


def auth_login_logic(username, password):
    """
    具体的登录逻辑
    :param user_name: 
    :param pass_word: 
    :return: 
    """
    cacert_config_single = NetWorkProxyConfigService.get_single_instance()
    if not cacert_config_single.account_auth_switch and not cacert_config_single.ldap_auth_switch:
        logger.exception("请开启代理的基础认证模块")
        return False

    proxy_account_auth_status = NetWorkProxyAccountAuth.auth_login_logic(username, password)
    proxy_ldap_auth_status = NetWorkProxyLdapAuth.auth_login_logic(username, password)
    if not proxy_account_auth_status and not proxy_ldap_auth_status:
        return False
    return True
