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
To use:
>>> from common.http_util import HttpMethod
>>> from common.http_util import ContentType
>>> from parser.chrome_traffic_parser import ChromeTrafficParser
>>> # 测试get 请求
>>> print(ChromeTrafficParser.add_poc_data(url="http://127.0.0.1/?name=23232&password=78812", data=None, http_method=HttpMethod.GET, content_type=None, poc="eval"))
>>> print(ChromeTrafficParser.add_poc_data(url="http://127.0.0.1/?name.jsp", http_method=HttpMethod.GET, data=None, content_type=None, poc="eval"))
>>> print(ChromeTrafficParser.add_poc_data(url="http://127.0.0.1/name.jsp", http_method=HttpMethod.GET, data=None, content_type=None, poc="eval"))
>>> print(ChromeTrafficParser.add_poc_data(url="http://127.0.0.1/name.jsp中文哦", http_method=HttpMethod.GET, data=None, content_type=None, poc="eval"))
>>>
>>> # 测试post 请求
>>>
>>> print("=========post=========")
>>> # 测试 post 请求
>>> # 参数放在 url中的请求
>>> print(ChromeTrafficParser.add_poc_data(url="http://127.0.0.1/?name=23232&password=78812", http_method=HttpMethod.POST, data=None, content_type=None, poc="eval"))
>>> # 普通 application/x-www-form-urlencoded 类型
>>> print(ChromeTrafficParser.add_poc_data(url="http://10.211.55.2:8887/v1/os_command_injection/test_case3", data="{\"name\":\"admin\",\"password\":\"admin888\"}", http_method=HttpMethod.POST, content_type=ContentType.ResourceContentType.DEFAULT, poc="eval"))
>>>
>>> # 普通 application/json 类型
>>> print(ChromeTrafficParser.add_poc_data(url="http://10.211.55.2:8887/v1/os_command_injection/test_case3", data="\"{\\\"username\\\":\\\"admin\\\",\\\"password\\\":\\\"passss\\\"}\"", http_method=HttpMethod.POST, content_type=ContentType.ResourceContentType.JSON, poc="eval"))
>>>

"""
import re
import json
from common.http_util import ContentType
from common.http_util import HttpMethod
from parser.base_traffic_parser import BaseTrafficParser
from abc import ABCMeta, abstractmethod


class ChromeTrafficParser(BaseTrafficParser):
    """
    流量解析器，chrome插件获取的流量解析器

    对于http请求，主要分为如下几类

    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    1.普通http get请求

    GET /show?name=23333
    Host: 127.0.0.1






    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    2.诡异的http post请求

    POST /show?name=23333
    Host: 127.0.0.1


    暂无

    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    3.普通http post请求

    POST /show HTTP/1.1
    Host: 127.0.0.1
    Content-Type: application/x-www-form-urlencoded; charset=UTF-8

    name=23333



    {
        "requestid": "3109",
        "data": {
            "requestid": "3109",
            "type": "main_frame",
            "url": "http://10.211.55.2:8887/v1/os_command_injection/test_case3",
            "method": "post",
            "data": "{\"name\":\"admin\",\"password\":\"admin888\"}",
            "data_type": "form_data",
            "headers": "{\"Origin\":\"http://10.211.55.2:8887\",\"Upgrade-Insecure-Requests\":\"1\",\"content-type\":\"application/x-www-form-urlencoded\",\"User-Agent\":\"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36\",\"Accept\":\"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3\",\"Referer\":\"http://10.211.55.2:8887/v1/os_command_injection/test_case3\",\"Accept-Encoding\":\"gzip, deflate\",\"Accept-Language\":\"zh-CN,zh;q=0.9\",\"Cookie\":\"session=.eJwtj9FPwjAYxP-XPpu1s6xB3r6J6IJkIZKBCwlp6jda2dqxdogY_3f74Nvl7n6X3A-RSqH3h-BOaMmM-G8OZtgUT9hxC_m6OjPD4BpMkT2moXrGMlWuLOdQV2tyR-RFBjlETofQ-xmljU9uwSXKdVGmdMUmlM9pKujXUueLirm3hQTQh1eAFy7EqtH1e8azpLfHONeMbWtlh3FwPz6IyXQ_CsEwJq5Haz6if9m0u1Nxm-7KbXFe1p8ar_c5xMbocfhnO2OPSsc_v3-fKEeY.ECpvpw.UI3gYbYgTVZta0KQjaxJ2mCPCL4\"}"
        }
    }

    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    4.json 格式的http post请求

    POST /show HTTP/1.1
    Host: 127.0.0.1
    Content-Type: application/json

    {"name":"23333"}

    chrome插件抓取到的数据包如下


    {
        "requestid": "3177",
        "data": {
            "requestid": "3177",
            "type": "xmlhttprequest",
            "url": "http://10.211.55.2:8887/v1/os_command_injection/test_case4",
            "method": "post",
            "data": "\"{\\\"username\\\":\\\"admin\\\",\\\"password\\\":\\\"passss\\\"}\"",
            "data_type": "raw",
            "headers": "{\"Accept\":\"application/json, text/javascript, */*; q=0.01\",\"Origin\":\"http://10.211.55.2:8887\",\"X-Requested-With\":\"XMLHttpRequest\",\"User-Agent\":\"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36\",\"content-type\":\"application/json\",\"Referer\":\"http://10.211.55.2:8887/v1/os_command_injection/test_case4\",\"Accept-Encoding\":\"gzip, deflate\",\"Accept-Language\":\"zh-CN,zh;q=0.9\",\"Cookie\":\"session=.eJwtj9FPwjAYxP-XPpu1s6xB3r6J6IJkIZKBCwlp6jda2dqxdogY_3f74Nvl7n6X3A-RSqH3h-BOaMmM-G8OZtgUT9hxC_m6OjPD4BpMkT2moXrGMlWuLOdQV2tyR-RFBjlETofQ-xmljU9uwSXKdVGmdMUmlM9pKujXUueLirm3hQTQh1eAFy7EqtH1e8azpLfHONeMbWtlh3FwPz6IyXQ_CsEwJq5Haz6if9m0u1Nxm-7KbXFe1p8ar_c5xMbocfhnO2OPSsc_v3-fKEeY.ECpvpw.UI3gYbYgTVZta0KQjaxJ2mCPCL4\"}"
        }
    }    

    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
    5.xml 格式的http post请求

    POST /show HTTP/1.1
    Host: 127.0.0.1
    Content-Type: text/xml

    <name>23333</name>



    {
        "requestid": "3187",
        "data": {
            "requestid": "3187",
            "type": "xmlhttprequest",
            "url": "http://10.211.55.2:8887/v1/os_command_injection/test_case5",
            "method": "post",
            "data": "\"<name>admin</name><password>password</password>\"",
            "data_type": "raw",
            "headers": "{\"Accept\":\"application/xml, text/xml, */*; q=0.01\",\"Origin\":\"http://10.211.55.2:8887\",\"X-Requested-With\":\"XMLHttpRequest\",\"User-Agent\":\"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36\",\"content-type\":\"text/xml\",\"Referer\":\"http://10.211.55.2:8887/v1/os_command_injection/test_case5\",\"Accept-Encoding\":\"gzip, deflate\",\"Accept-Language\":\"zh-CN,zh;q=0.9\",\"Cookie\":\"session=.eJwtj9FPwjAYxP-XPpu1s6xB3r6J6IJkIZKBCwlp6jda2dqxdogY_3f74Nvl7n6X3A-RSqH3h-BOaMmM-G8OZtgUT9hxC_m6OjPD4BpMkT2moXrGMlWuLOdQV2tyR-RFBjlETofQ-xmljU9uwSXKdVGmdMUmlM9pKujXUueLirm3hQTQh1eAFy7EqtH1e8azpLfHONeMbWtlh3FwPz6IyXQ_CsEwJq5Haz6if9m0u1Nxm-7KbXFe1p8ar_c5xMbocfhnO2OPSsc_v3-fKEeY.ECpvpw.UI3gYbYgTVZta0KQjaxJ2mCPCL4\"}"
        }
    }




    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    6.表单上传格式的http post请求

    POST /show HTTP/1.1
    Host: 127.0.0.1
    Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryH0TGOzR6zJhOJSVB

    ------WebKitFormBoundaryH0TGOzR6zJhOJSVB
    Content-Disposition: form-data; name="file"; filename="5.png"
    Content-Type: image/png

    XXXXXX
    ------WebKitFormBoundaryH0TGOzR6zJhOJSVB--




    {
        "requestid": "3197",
        "data": {
            "requestid": "3197",
            "type": "main_frame",
            "url": "http://10.211.55.2:8887/v1/os_command_injection/test_case6",
            "method": "post",
            "data": "\"------WebKitFormBoundarydnAY6LXdz8oOOXxy\\r\\nContent-Disposition: form-data; name=\\\"file\\\"; filename=\\\"5.png\\\"\\r\\nContent-Type: image/png\\r\\n\\r\\n\"",
            "data_type": "raw",
            "headers": "{\"Origin\":\"http://10.211.55.2:8887\",\"Upgrade-Insecure-Requests\":\"1\",\"content-type\":\"multipart/form-data; boundary=----WebKitFormBoundarydnAY6LXdz8oOOXxy\",\"User-Agent\":\"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36\",\"Accept\":\"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3\",\"Referer\":\"http://10.211.55.2:8887/v1/os_command_injection/test_case6\",\"Accept-Encoding\":\"gzip, deflate\",\"Accept-Language\":\"zh-CN,zh;q=0.9\",\"Cookie\":\"session=.eJwtj9FPwjAYxP-XPpu1s6xB3r6J6IJkIZKBCwlp6jda2dqxdogY_3f74Nvl7n6X3A-RSqH3h-BOaMmM-G8OZtgUT9hxC_m6OjPD4BpMkT2moXrGMlWuLOdQV2tyR-RFBjlETofQ-xmljU9uwSXKdVGmdMUmlM9pKujXUueLirm3hQTQh1eAFy7EqtH1e8azpLfHONeMbWtlh3FwPz6IyXQ_CsEwJq5Haz6if9m0u1Nxm-7KbXFe1p8ar_c5xMbocfhnO2OPSsc_v3-fKEeY.ECpvpw.UI3gYbYgTVZta0KQjaxJ2mCPCL4\"}"
        }
    }    


    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    对应chrome插件抓取到的数据包为

    """

    @staticmethod
    def get_parameter(url, data, http_method, content_type):
        """
        get和BaseTrafficParser一致, post不一致
        :param url: 
        :param data: 
        :param http_method: 
        :param content_type: 
        :return: 
        """
        if (http_method and http_method.lower() == HttpMethod.GET) or content_type is None:
            return BaseTrafficParser.get_parameter(url=url, data=data, http_method=http_method,
                                                   content_type=content_type)
        elif http_method and http_method == HttpMethod.POST:
            return ChromeTrafficParser._parse_post_parameter(data, content_type)

    @staticmethod
    def _parse_post_parameter(data, content_type):
        """
        解析chrome抓取到的流量
        :param data: 
        :param content_type: 
        :return: 
        """
        if content_type:
            content_type = content_type.lower()
        if content_type == ContentType.ResourceContentType.DEFAULT or content_type == ContentType.ResourceContentType.JSON:
            # data = "{\"name\":\"admin\",\"password\":\"admin888\"}" //application/x-www-form-urlencoded
            # data = "\"{\\\"username\\\":\\\"admin\\\",\\\"password\\\":\\\"passss\\\"}\"" //application/json
            return json.loads(data)
        elif content_type == ContentType.ResourceContentType.XML:
            # 暂不支持，去除"符号
            data = re.findall(u'"(.*?)"', data, re.S)[0]
            return data
        elif content_type == ContentType.ResourceContentType.FORM:
            filename = re.findall('filename=[\\\]*"([\w\.]*)[\\\]*"', data, re.S)[0]
            return {'filename': filename}

    @staticmethod
    def simplify_request(url, data=None, http_method=HttpMethod.GET, content_type=None):
        """
        解析请求参数，将数据转换成 requests能解析的类型
        :param url: 
        :param data: 
        :param http_method: 
        :param content_type: 
        :return: 
        """
        if (http_method and http_method.lower() == HttpMethod.GET) or content_type is None:
            return {"url": BaseTrafficParser._simplify_get_request(url), "data": data, "http_method": http_method,
                    "content_type": None}
        elif http_method and http_method.lower() == HttpMethod.POST:
            if ContentType.ResourceContentType.DEFAULT in content_type.lower():
                return {"url": url, "data": ChromeTrafficParser._simplify_post_request_default(data),
                        "http_method": http_method, "content_type": ContentType.ResourceContentType.DEFAULT}
            elif ContentType.ResourceContentType.JSON in content_type.lower():
                return {"url": url, "data": ChromeTrafficParser._get_json_parameter(
                    ChromeTrafficParser._parse_post_parameter(data, content_type)), "http_method": http_method,
                        "content_type": ContentType.ResourceContentType.JSON}
            elif ContentType.ResourceContentType.XML in content_type.lower():
                return {"url": url, "data": ChromeTrafficParser._parse_post_parameter(data, content_type),
                        "http_method": http_method, "content_type": ContentType.ResourceContentType.XML}
            elif ContentType.ResourceContentType.FORM in content_type.lower():
                # 暂时不处理
                return {"url": url, "data": data, "http_method": http_method,
                        "content_type": ContentType.ResourceContentType.FORM}
            elif ContentType.ResourceContentType.TXT in content_type.lower():
                return {"url": url, "data": data, "http_method": http_method,
                        "content_type": ContentType.ResourceContentType.TXT}

    @staticmethod
    def _simplify_post_request_default(data):
        """
        对 application/x-www-form-urlencoded类型参数解析
        :param data: 
        :param http_method: 
        :param content_type: 
        :return: 
        """
        result_urls_key = None
        have_parameter = False
        result_parameter = ""
        http_parameter = BaseTrafficParser._get_json_parameter(data)
        http_parameter = BaseTrafficParser._replace_param_val_to_identification(http_parameter)
        for key, value in http_parameter.items():
            result_parameter += "{}={}&".format(key, value)
            have_parameter = True
        if have_parameter:
            result_urls_key = result_parameter[:-1]
        return result_urls_key if result_urls_key else data

    @staticmethod
    def add_poc_data(url, data, http_method, content_type, poc):
        """
        在原来数据的基础上替换成poc数据
        :param url: get类型下完整url post为请求数据
        :param http_method: 
        :param content_type: 
        :param poc: 
        :return: 
        """
        try:
            poc_result = ChromeTrafficParser.simplify_request(url=url, data=data, http_method=http_method,
                                                              content_type=content_type)
            if (http_method and http_method.lower() == HttpMethod.GET) or content_type is None:
                poc_result["url"] = BaseTrafficParser.replace(poc_result["url"], poc)
            elif http_method and http_method.lower() == HttpMethod.POST:
                poc_result["data"] = BaseTrafficParser.replace(poc_result["data"], poc)
        except Exception:
            poc_result = {"url": url, "data": data, "http_method": http_method, "content_type": content_type}
        return poc_result

    @staticmethod
    def to_raw(url, data, http_method, content_type):
        """
        将chrome plugin 流量转换成raw
        :param url: 
        :param data: 
        :param http_method: 
        :param content_type: 
        :return: 
        """
        if (http_method and http_method.lower() == HttpMethod.GET) or content_type is None:
            return {"url": url, "data": data, "http_method": http_method, "content_type": content_type}
        elif http_method and http_method.lower() == HttpMethod.POST:
            if ContentType.ResourceContentType.DEFAULT in content_type.lower():
                http_parameter = json.loads(data)
                result_parameter = ""
                for key, value in http_parameter.items():
                    result_parameter += "{}={}&".format(key, value)
                return {"url": url, "data": result_parameter, "http_method": http_method, "content_type": content_type}
            elif ContentType.ResourceContentType.JSON in content_type.lower():
                return {"url": url, "data": json.loads(data), "http_method": http_method, "content_type": content_type}
            elif ContentType.ResourceContentType.XML in content_type.lower():
                data = re.findall(u'"(.*?)"', data, re.S)[0]
                return {"url": url, "data": data, "http_method": http_method, "content_type": content_type}
            elif ContentType.ResourceContentType.FORM in content_type.lower():
                return {"url": url, "data": data, "http_method": http_method, "content_type": content_type}
            elif ContentType.ResourceContentType.TXT in content_type.lower():
                return {"url": url, "data": data, "http_method": http_method, "content_type": content_type}
        return {"url": url, "data": data, "http_method": http_method, "content_type": content_type}
