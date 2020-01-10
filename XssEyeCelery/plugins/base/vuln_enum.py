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


class PluginSwith(object):
    """
    插件开关类
    """
    ON = 1
    OFF = 0


class VulnLevel(object):
    HIGHT = 'high'
    MIDDLE = 'middle'
    LOW = 'low'


class VulnType(object):
    """
    xss = 'xss跨站脚本攻击' high
    xxe = 'xml外部实体攻击' high
    sql = 'sql注入', 'high'
    csrf = '跨站请求伪造' middle
    cors = '请求对象共享' high
    jsonp = 'jsonp劫持' middle
    weakpwd = '弱密码' high
    crlf = '回车键注入' low
    infoleak = '信息泄漏' high
    cmdect = '命令执行' high
    ddos = 'ddos漏洞' high
    fileread = '任意文件读取,包含任意下载之类的' high
    fileupload = '任意文件上传' high
    fileinclude = '文件包含' high
    other = '其它,包括越权之类的' middle
    ssrf = '服务器端请求伪造'
    """
    SQL_INJECT = {'fullname': 'sql_inject', 'fullchinesename': 'sql注入', 'level': VulnLevel.HIGHT}
    XSS = {'fullname': 'xss', 'fullchinesename': 'xss跨站脚本攻击', 'level': VulnLevel.HIGHT}
    XXE = {'fullname': 'xxe', 'fullchinesename': 'xml外部实体攻击', 'level': VulnLevel.HIGHT}
    WEAK_PWD = {'fullname': 'weak_pwd', 'fullchinesename': '弱密码', 'level': VulnLevel.HIGHT}
    CMD_ECT = {'fullname': 'cmdect', 'fullchinesename': '命令执行', 'level': VulnLevel.HIGHT}
    FILE_READ = {'fullname': 'file_read', 'fullchinesename': '任意文件读取', 'level': VulnLevel.HIGHT}
    FILE_UPLOAD = {'fullname': 'file_upload', 'fullchinesename': '任意文件上传', 'level': VulnLevel.HIGHT}
    FILE_INCLUDE = {'fullname': 'file_include', 'fullchinesename': '文件包含', 'level': VulnLevel.HIGHT}
    DDOS = {'fullname': 'ddos', 'fullchinesename': 'ddos', 'level': VulnLevel.HIGHT}
    CSRF = {'fullname': 'csrf', 'fullchinesename': '跨站请求伪造', 'level': VulnLevel.MIDDLE}
    CORS = {'fullname': 'cors', 'fullchinesename': '请求对象共享', 'level': VulnLevel.MIDDLE}
    JSONP = {'fullname': 'jsonp', 'fullchinesename': 'jsonp跨域劫持', 'level': VulnLevel.MIDDLE}
    INFO_LEAK = {'fullname': 'info_leak', 'fullchinesename': '信息泄漏', 'level': VulnLevel.MIDDLE}
    CRLF = {'fullname': 'crlf', 'fullchinesename': '回车键注入', 'level': VulnLevel.LOW}
    OTHER = {'fullname': 'other', 'fullchinesename': '其它', 'level': VulnLevel.LOW}
    HIDDEN_DANGER = {'fullname': 'hidden_danger', 'fullchinesename': '安全隐患', 'level': VulnLevel.LOW}
    SSRF = {'fullname': 'ssrf', 'fullchinesename': '服务器端请求伪造', 'level': VulnLevel.HIGHT}

    @staticmethod
    def get_fullnames():
        """
        获取所有的类型fullname
        :return: 
        """
        pass
