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
import threading
from model.default_value import Role
 
from api.authentication.default_auth_module import DefaultAuthModule
from api.authentication.ldap_auth_module import LdapAuthModule

# single_auto_module_lock = threading.Lock()
auto_module_instance = None


# __all__ = ["check_authentication"]

def get_auth_module():
    """
    获取单例对象，去除锁
    :return: 
    """
    global auto_module_instance
    if not auto_module_instance:
        """
        with single_auto_module_lock:
            if not auto_module_instance:
        auto_module_instance = DefaultAuthModule()
        """
        auto_module_instance = DefaultAuthModule()
    return auto_module_instance


def check_authentication(role=Role.USER):
    """
    检测权限,默认sso
    :param role: 
    :return: 
    """
    return get_auth_module().check_authentication(role)