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

__all__ = ["CookieNotFoundException", "UserNotLoginZtoException", "PrivateKeyNotFound", "PublicKeyNotFound",
           "SystemConfigNotFound", "AuthenticationTimeoutError"]


class BaseHunterException(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)


class CookieNotFoundException(BaseHunterException):
    """
    未找到cookie
    """

    def __init__(self, message):
        BaseHunterException.__init__(self, message)


class UserNotFoundInRedisException(BaseHunterException):
    """
    未从Redis中找到用户
    """

    def __init__(self, message):
        BaseHunterException.__init__(self, message)


class RedisError(BaseHunterException):
    """
    执行RedisSevice中的函数出错，即Redis操作出错
    """

    def __init__(self, message):
        BaseHunterException.__init__(self, message)


class UserNotLoginException(BaseHunterException):
    """
    用户未登录或者登录过期
    """

    def __init__(self, message):
        BaseHunterException.__init__(self, message)


class PrivateKeyNotFound(BaseHunterException):
    """
    秘钥未设置抛出异常，秘钥需要设置在数据库中
    """

    def __init__(self, message):
        BaseHunterException.__init__(self, message)


class PublicKeyNotFound(BaseHunterException):
    """
    公钥未设置抛出异常，秘钥需要设置在数据库中
    """

    def __init__(self, message):
        BaseHunterException.__init__(self, message)


class SystemConfigNotFound(BaseHunterException):
    """
    网站设置未设置抛出异常，需要设置在数据库中，并且主键为1
    """

    def __init__(self, message):
        BaseHunterException.__init__(self, message)


class AuthenticationTimeoutError(BaseHunterException):
    """
    认证身份接口超时
    """

    def __init__(self, message):
        BaseHunterException.__init__(self, message)
