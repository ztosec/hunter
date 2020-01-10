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
import re
import json
from sys import version_info

if version_info < (3, 0):
    from urllib import quote
else:
    from urllib.parse import quote

__all__ = ["is_uploadordownload", "remove_http", "get_host_port", "get_host_port_protocol", "get_top_domain",
           "header_to_lowercase",
           "url_encode", "get_parent_route", "get_parent_route"]


def is_uploadordownload(package):
    """
    是否为上传类
    :param package: 
    :return: 
    """
    if package["data"] and "headers" in package["data"]:
        headers = json.loads(package["data"]["headers"])
        if "Content-Type" in headers:
            if ContentType.StaticResourceContentType.UPLOAD_FORM in headers["Content-Type"] or \
                            ContentType.StaticResourceContentType.DOWNLOAD in headers["Content-Type"]:
                return True
        if "content-type" in headers:  # 来自插件的请求
            if ContentType.StaticResourceContentType.UPLOAD_FORM in headers["content-type"] or \
                            ContentType.StaticResourceContentType.DOWNLOAD in headers["content-type"]:
                return True
    return False


def remove_http(url):
    """
    1.先判断是否是已 http或者https开头
    将http://xxxx/中的主机名提取出来
    :return: 
    """
    domain = re.findall(r'(?:http[s]?://)?([\w\.\-]*)/*', url)
    if len(domain) > 0:
        host = str(domain[0]).replace("/", "")
    else:
        host = url.replace("/", "")
    return host


def get_host_port(url, default_port=80):
    """
    从url中提取出域名和端口,例如 http://xxxx:8090
    :param url: 
    :return: 
    """
    host_port = re.findall(r'(?:http[s]?://)?([\w\.-]*)[:]?(\d*)/*', url)
    if len(host_port) > 0:
        host, port = host_port[0][0], default_port if host_port[0][1] == '' else int(host_port[0][1])
    else:
        host = url, port = 80
    return host, port


def get_host_port_protocol(url, default_port=80):
    """
    提取host port protocol
    :param url: 
    :param default_port: 
    :return: 
    """
    host, port = get_host_port(url)
    if str(url).startswith("https://"):
        protocol = "https"
    else:
        protocol = "http"
    return host, port, protocol


def get_top_domain(url):
    """
    通过url获得顶级域名
    :param url: 
    :return: 
    """
    sub_domain = remove_http(url)
    return sub_domain if len(sub_domain.split(".")) == 2 else ".".join(sub_domain.split(".")[-2:])


def header_to_lowercase(headers):
    """
    :param header: 
    :return: 
    """
    result = dict()
    for key in headers.keys():
        if key.lower() == "content-type":
            result['content-type'] = headers[key]
        result[key] = headers[key]
    return result


def url_encode(str):
    return quote(str).replace("/", "%2F")


def get_parent_route(url):
    """
    获得父级路由
    :param url: 
    :return: 
    """
    parameter = re.split(r'/[^/]*$', url, re.S)
    try:
        result = parameter[0] + "/"
    except IndexError:
        result = url + "/"
    if result == "https://" or result == "http://":
        result = url + "/"
    return result


class ContentType:
    NAME = "Content-Type"

    class ResourceContentType:
        # 静态资源类型
        PNG = "image/png"
        TIF = "image/tiff"
        FAX = "image/fax"
        GIF = "image/gif"
        ICO = "image/x-icon"
        JPE = "image/jpeg"
        JPEG = "image/jpeg"
        PNG = "image/png"
        WBMP = "image/vnd.wap.wbmp"
        CSS = "text/css"
        MP2 = "audio/mp2"
        MP3 = "audio/mp3"
        MPA = "video/x-mpg"
        MPE = "video/x-mpeg"
        MPG = "video/mpg"
        MP2V = "video/mpeg"
        MP4 = "video/mpeg4"
        MPEG = "video/mpg"
        MPS = "video/x-mpeg"
        WMZ = "video/x-ms-wmv"
        WRM = "video/x-ms-wm"
        WMX = "video/x-ms-wmx"
        WVX = "video/x-ms-wvx"
        # 非静态资源类型
        UPLOAD_FORM = "multipart/form-data; boundary="
        DOWNLOAD = "application/octet-stream"
        JSON = "application/json"
        XML = "text/xml"
        DEFAULT = "application/x-www-form-urlencoded"
        HTML = "text/html"
        FORM = "multipart/form-data"
        TXT = "text/plain"

        static_resource_list = [PNG, TIF, FAX, GIF, ICO, JPE, JPEG, PNG, WBMP, CSS, MP2, MP3, MPA, MPE, MPG, MP2V, MP4,
                                MPEG, MPS, WMZ, WRM, WMX, WVX]


class UserAgent:
    NAME = "Content-Type"

    class MobileDevices:
        """
        移动设备的UA
        """
        ANDROID = "Dalvik/2.1.0 (Linux; U; Android 5.1; OPPO R9m Build/LMY47I)"

    class PCDevices:
        """
        PC UA
        """
        CHROME_MAC = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) " \
                     "Chrome/65.0.33 25.181 Safari/537.36"


class AcceptCharset():
    UTF8 = "UTF-8"


class HttpMethod():
    GET = "get"
    POST = "post"
    PUT = "put"
    DELETE = "delete"


def check_is_alive(url, method, data, headers):
    """
    检测接口是否能正常访问
    :param package: 
    :return: 
    """
    import requests
    from common import log
    logger = log.get_default_logger()
    headers = json.loads(headers) if isinstance(headers, str) else headers
    try:
        logger.info("check if the target URL content is stable")
        requests.request(method=method, url=url, data=data, headers=headers, timeout=5)
        logger.info("the target URL content is stable")
        return True
    except Exception as e:
        logger.warn("the target URL content is not stable")
        return False


def json_to_urlencoded(data):
    """
    将{'B1': '信息', 'id': '1', 'msg': 'abc'} 转换成B1=信息&id=1&msg=abc
    :param json: 
    :return: 
    """
    # import sys
    # reload(sys)
    # sys.setdefaultencoding('utf8')
    result = ""
    for key, value in data.items():
        temp_data = "{}={}".format(key, value)
        result = "{}&{}".format(result, temp_data) if result != "" else temp_data
    return result


def header_to_lowercase(headers):
    """
    转小写并且去掉http头中的*
    :param header: 
    :return: 
    """
    result = dict()
    for key in headers.keys():
        if key.lower() == "content-type":
            result['content-type'] = headers[key]
        if "*" not in key and "*" not in headers[key]:
            result[key] = headers[key]
    return result


def header_to_str(headers):
    """
    将headrs由{'name': 'pass', 'whoami', 'root'}dict转成   name:pass\nwhoami:root
    :param headers: 
    :return: 
    """
    result = ""
    for key, value in headers.items():
        if result != "":
            result = "{}\\n{}:{}".format(result, key, value)
        else:
            result = "{}:{}".format(key, value)
    return result
