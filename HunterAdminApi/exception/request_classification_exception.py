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
from exception.hunter_web_exception import BaseHunterException


class RequestClassificationException(BaseHunterException):
    def __init__(self, message):
        BaseHunterException.__init__(self, message)


class RequestParseError(BaseHunterException):
    def __init__(self, package, miss_keys):
        BaseHunterException.__init__(self, "{}不完整,请求报文有待补充项,待补充的字段有{}".format(package, ','.join(miss_keys)))


class HeaderParseError(BaseHunterException):
    def __init__(self):
        BaseHunterException.__init__(self, "解析http头出错")


class PluginInfoError(BaseHunterException):
    def __init__(self, info, miss_keys):
        BaseHunterException.__init__(self, "插件信息{}不完整,待补充的字段有{}".format(info, ','.join(miss_keys)))


class PluginNotFoundError(BaseHunterException):
    def __init__(self, plugin):
        BaseHunterException.__init__(self, "模块{}未找到".format(plugin))
