#!/ usr/bin/env
# coding=utf-8
"""
author: b5mali4
Copyright (c) 2018
"""
import unittest
from common.http_util import ContentType


class TestCase(unittest.TestCase):
    def testGetParameter(self):
        """
        获取参数
        :return: 
        """
        from common.http_util import HttpMethod
        from common.http_util import ContentType
        from parser.chrome_traffic_parser import ChromeTrafficParser

        # 测试get 请求
        """
        print(ChromeTrafficParser.get_parameter(url="http://127.0.0.1/?name=23232&password=78812",data=None,
                                              http_method=HttpMethod.GET, content_type=None))
        print(
            ChromeTrafficParser.get_parameter(url="http://127.0.0.1/?name=中文&password=78812", data=None, http_method=HttpMethod.GET, content_type=None))
        print(ChromeTrafficParser.get_parameter(url="http://127.0.0.1/?name=%E4%B8%AD%E6%96%87&password=78812",
                                              http_method=HttpMethod.GET, content_type=None, data=None))
        print(ChromeTrafficParser.get_parameter(url="http://127.0.0.1/?name=中文&password=78812#",data=None,
                                              http_method=HttpMethod.GET, content_type=None))
        print(ChromeTrafficParser.get_parameter(url="http://127.0.0.1/?name=中文……**$$$&password=78812、#",data=None,
                                              http_method=HttpMethod.GET,content_type=None))
        print(ChromeTrafficParser.get_parameter(
            url="http://127.0.0.1/?name=中文&password=78812！@#¥%……*()_+|}{QASDFGHJK<>MNZXCVBN#",
            http_method=HttpMethod.GET, data=None,content_type=None))
        """

        print("=========post2=========")
        # 测试 post 请求
        # 普通 application/x-www-form-urlencoded 类型, 这是chrome浏览器抓到的内容
        print(ChromeTrafficParser.get_parameter(url="http://127.0.0.1/login",
                                                data="{\"name\":\"admin\",\"password\":\"admin888\"}",
                                                http_method=HttpMethod.POST,
                                                content_type=ContentType.ResourceContentType.DEFAULT))

        # 普通 application/json
        print(ChromeTrafficParser.get_parameter(url="http://127.0.0.1/login",
                                                data="\"{\\\"username\\\":\\\"admin\\\",\\\"password\\\":\\\"passss\\\"}\"",
                                                http_method=HttpMethod.POST,
                                                content_type=ContentType.ResourceContentType.JSON))

        # 普通text/xml
        print(ChromeTrafficParser.get_parameter(url="http://127.0.0.1/login",
                                                data="\"<name>admin</name><password>password</password>\"",
                                                http_method=HttpMethod.POST,
                                                content_type=ContentType.ResourceContentType.XML))
        # 普通文件上传
        upload_data1 = "\"------WebKitFormBoundarydnAY6LXdz8oOOXxy\\r\\nContent-Disposition: form-data; name=\\\"file\\\"; filename=\\\"5.png\\\"\\r\\nContent-Type: image/png\\r\\n\\r\\n\""

        print(ChromeTrafficParser.get_parameter(url="http://127.0.0.1/login",
                                                data=upload_data1,
                                                http_method=HttpMethod.POST,
                                                content_type=ContentType.ResourceContentType.FORM))

    def test1SimplifyRequest(self):
        """
        测试对url或者参数进行归类
        :return: 
        """
        from common.http_util import HttpMethod
        from common.http_util import ContentType
        from parser.chrome_traffic_parser import ChromeTrafficParser
        # 测试get 请求
        print(ChromeTrafficParser.simplify_request(url="http://127.0.0.1/?name=23232&password=78812", data=None,
                                                   http_method=HttpMethod.GET, content_type=None))
        print(
        ChromeTrafficParser.simplify_request(url="http://127.0.0.1/?name.jsp", http_method=HttpMethod.GET, data=None,
                                             content_type=None))
        print(
        ChromeTrafficParser.simplify_request(url="http://127.0.0.1/name.jsp", http_method=HttpMethod.GET, data=None,
                                             content_type=None))
        print(
        ChromeTrafficParser.simplify_request(url="http://127.0.0.1/name.jsp中文哦", http_method=HttpMethod.GET, data=None,
                                             content_type=None))

        print(ChromeTrafficParser.simplify_request(
            url="http://10.211.55.2:65412/?xml=%3Croot%3E111%3Croot%3E",
            http_method=HttpMethod.GET, data=None, content_type=None))

        # 测试post 请求

        print("=========post=========")
        # 测试 post 请求
        # 参数放在 url中的请求
        print(ChromeTrafficParser.simplify_request(url="http://127.0.0.1/?name=23232&password=78812",
                                                   http_method=HttpMethod.POST, data=None, content_type=None))
        # 普通 application/x-www-form-urlencoded 类型
        print(ChromeTrafficParser.simplify_request(url="http://10.211.55.2:8887/v1/os_command_injection/test_case3",
                                                   data="{\"name\":\"admin\",\"password\":\"admin888\"}",
                                                   http_method=HttpMethod.POST,
                                                   content_type=ContentType.ResourceContentType.DEFAULT))

        # 普通 application/json 类型
        print(ChromeTrafficParser.simplify_request(url="http://10.211.55.2:8887/v1/os_command_injection/test_case3",
                                                   data="\"{\\\"username\\\":\\\"admin\\\",\\\"password\\\":\\\"passss\\\"}\"",
                                                   http_method=HttpMethod.POST,
                                                   content_type=ContentType.ResourceContentType.JSON))

        # 普通xml不做处理
        print(ChromeTrafficParser.simplify_request(url="http://10.211.55.2:8887/v1/os_command_injection/test_case3",
                                                   data="\"<name>admin</name><password>password</password>\"",
                                                   http_method=HttpMethod.POST,
                                                   content_type=ContentType.ResourceContentType.XML))

        # 文件上传内容
        upload_data1 = "\"------WebKitFormBoundarydnAY6LXdz8oOOXxy\\r\\nContent-Disposition: form-data; name=\\\"file\\\"; filename=\\\"5.png\\\"\\r\\nContent-Type: image/png\\r\\n\\r\\n\""
        print(ChromeTrafficParser.simplify_request(url="http://127.0.0.1/upload", data=upload_data1,
                                                   http_method=HttpMethod.POST,
                                                   content_type=ContentType.ResourceContentType.FORM))

    def testTORaw(self):
        """
        增加poc脚本
        :return: 
        """
        from common.http_util import HttpMethod
        from common.http_util import ContentType
        from parser.chrome_traffic_parser import ChromeTrafficParser
        # 测试get 请求
        print(ChromeTrafficParser.to_raw(url="http://127.0.0.1/?name=23232&password=78812", data=None,
                                         http_method=HttpMethod.GET, content_type=None))
        print(ChromeTrafficParser.to_raw(url="http://127.0.0.1/?name.jsp", http_method=HttpMethod.GET, data=None,
                                         content_type=None))
        print(ChromeTrafficParser.to_raw(url="http://127.0.0.1/name.jsp", http_method=HttpMethod.GET, data=None,
                                         content_type=None))
        print(ChromeTrafficParser.to_raw(url="http://127.0.0.1/name.jsp中文哦", http_method=HttpMethod.GET, data=None,
                                         content_type=None))

        print("=========post=========")
        # 测试 post 请求
        # 参数放在 url中的请求
        print(ChromeTrafficParser.to_raw(url="http://127.0.0.1/?name=23232&password=78812",
                                         http_method=HttpMethod.POST, data=None, content_type=None))

        # 普通 application/x-www-form-urlencoded 类型
        print(ChromeTrafficParser.to_raw(url="http://10.211.55.2:8887/v1/os_command_injection/test_case3",
                                         data="{\"name\":\"admin\",\"password\":\"admin888\"}",
                                         http_method=HttpMethod.POST,
                                         content_type=ContentType.ResourceContentType.DEFAULT))

        # 普通 application/json 类型
        print(ChromeTrafficParser.to_raw(url="http://10.211.55.2:8887/v1/os_command_injection/test_case3",
                                         data="\"{\\\"username\\\":\\\"admin\\\",\\\"password\\\":\\\"passss\\\"}\"",
                                         http_method=HttpMethod.POST,
                                         content_type=ContentType.ResourceContentType.JSON))
        # 普通xml不做处理
        print(ChromeTrafficParser.to_raw(url="http://10.211.55.2:8887/v1/os_command_injection/test_case3",
                                         data="\"<name>admin</name><password>password</password>\"",
                                         http_method=HttpMethod.POST,
                                         content_type=ContentType.ResourceContentType.XML))
        # 文件上传内容
        upload_data1 = "\"------WebKitFormBoundarydnAY6LXdz8oOOXxy\\r\\nContent-Disposition: form-data; name=\\\"file\\\"; filename=\\\"5.png\\\"\\r\\nContent-Type: image/png\\r\\n\\r\\n\""
        print(ChromeTrafficParser.simplify_request(url="http://127.0.0.1/upload", data=upload_data1,
                                                   http_method=HttpMethod.POST,
                                                   content_type=ContentType.ResourceContentType.FORM))


if __name__ == "__main__":
    unittest.main()
