#!/ usr/bin/env
# coding=utf-8
"""
author: b5mali4
Copyright (c) 2018
"""
import unittest


class TestCase(unittest.TestCase):
    def testGetParameter(self):
        """
        获取参数
        :return: 
        """
        from common.http_util import HttpMethod
        from common.http_util import ContentType
        from parser.base_traffic_parser import BaseTrafficParser

        # 测试get 请求
        print(BaseTrafficParser.get_parameter(url="http://127.0.0.1:65412/?path=", data=None,
                                              http_method=HttpMethod.GET, content_type=None))
        print(BaseTrafficParser.get_parameter(url="http://127.0.0.1/?name=23232&password=78812", data=None,
                                              http_method=HttpMethod.GET, content_type=None))
        print(
            BaseTrafficParser.get_parameter(url="http://127.0.0.1/?name=中文&password=78812", data=None,
                                            http_method=HttpMethod.GET))
        print(BaseTrafficParser.get_parameter(url="http://127.0.0.1/?name=%E4%B8%AD%E6%96%87&password=78812",
                                              http_method=HttpMethod.GET))
        print(BaseTrafficParser.get_parameter(url="http://127.0.0.1/?name=中文&password=78812#", data=None,
                                              http_method=HttpMethod.GET))
        print(BaseTrafficParser.get_parameter(url="http://127.0.0.1/?name=中文……**$$$&password=78812、#", data=None,
                                              http_method=HttpMethod.GET))
        print(BaseTrafficParser.get_parameter(
            url="http://127.0.0.1/?name=中文&password=78812！@#¥%……*()_+|}{QASDFGHJK<>MNZXCVBN#",
            http_method=HttpMethod.GET))

        print("=========post2=========")
        # 测试 post 请求
        # 普通 application/x-www-form-urlencoded 类型
        print(BaseTrafficParser.get_parameter(url="http://127.0.0.1/login", data="name=23333&",
                                              http_method=HttpMethod.POST,
                                              content_type=ContentType.ResourceContentType.DEFAULT))
        # 普通 application/json 类型
        print(BaseTrafficParser.get_parameter(url="http://127.0.0.1/login", data='{"name":"23333"}',
                                              http_method=HttpMethod.POST,
                                              content_type=ContentType.ResourceContentType.JSON))

        # print(BaseTrafficParser.get_parameter(url='{\\\"username\\\":\\\"admin\\\",\\\"password\\\":\\\"passss\\\"}', http_method=HttpMethod.POST, content_type=ContentType.ResourceContentType.JSON))
        # 普通 text/xml 类型，暂不支持
        print(BaseTrafficParser.get_parameter(url="http://127.0.0.1/login", data="<name>23333</name>",
                                              http_method=HttpMethod.POST,
                                              content_type=ContentType.ResourceContentType.XML))

        upload_data1 = """------WebKitFormBoundaryH0TGOzR6zJhOJSVB \n Content-Disposition: form-data; name="file"; filename="5.png" \n Content-Type: image/png \n XXXXXX \n ------WebKitFormBoundaryH0TGOzR6zJhOJSVB-- """
        upload_data2 = """
                ------WebKitFormBoundarydnAY6LXdz8oOOXxy\\r\\nContent-Disposition: form-data; name=\\\"file\\\"; filename=\\\"5.png\\\"\\r\\nContent-Type: image/png\\r\\n\\r\\n\
                """

        # 普通上传文件表单 multipart/form-data; boundary=----WebKitFormBoundaryH0TGOzR6zJhOJSVB，
        print(BaseTrafficParser.get_parameter(url="http://127.0.0.1/upload", data=upload_data1,
                                              http_method=HttpMethod.POST,
                                              content_type=ContentType.ResourceContentType.FORM))

    def test1SimplifyRequest(self):
        """
        测试对url或者参数进行归类
        :return: 
        """
        from common.http_util import HttpMethod
        from common.http_util import ContentType
        from parser.base_traffic_parser import BaseTrafficParser
        # 测试get 请求
        simplify_request0 = BaseTrafficParser.simplify_request(url="http://127.0.0.1:8889/?name=23232&password=78812",
                                                               data=None, http_method=HttpMethod.GET, content_type=None)
        print(simplify_request0)
        # self.send_data(simplify_request0)
        """
        print(BaseTrafficParser.simplify_request(url="http://127.0.0.1/?name.jsp", http_method=HttpMethod.GET, data=None, content_type=None))
        print(BaseTrafficParser.simplify_request(url="http://127.0.0.1/name.jsp", http_method=HttpMethod.GET, data=None, content_type=None))
        print(BaseTrafficParser.simplify_request(url="http://127.0.0.1/name.jsp中文哦", http_method=HttpMethod.GET, data=None, content_type=None))
        """
        # 测试post 请求

        print("=========post=========")
        # 测试 post 请求
        # 普通 application/x-www-form-urlencoded 类型
        simplify_request1 = BaseTrafficParser.simplify_request(
            url="http://10.211.55.2:8889/v1/os_command_injection/test_case3", data="name=23333&pass=1",
            http_method=HttpMethod.POST, content_type=ContentType.ResourceContentType.DEFAULT)
        self.send_data(simplify_request1)

        simplify_request2 = BaseTrafficParser.simplify_request(
            url="http://10.211.55.2:8889/v1/os_command_injection/test_case3", data="name=23333&pass=1&&",
            http_method=HttpMethod.POST, content_type=ContentType.ResourceContentType.DEFAULT)
        self.send_data(simplify_request2)

        simplify_request3 = BaseTrafficParser.simplify_request(
            url="http://10.211.55.2:8889/v1/os_command_injection/test_case3", data="name=23333",
            http_method=HttpMethod.POST, content_type=ContentType.ResourceContentType.DEFAULT)
        self.send_data(simplify_request3)

        simplify_request4 = BaseTrafficParser.simplify_request(
            url="http://10.211.55.2:8889/v1/os_command_injection/test_case3", data="name=23333&",
            http_method=HttpMethod.POST, content_type=ContentType.ResourceContentType.DEFAULT)
        self.send_data(simplify_request4)

        # 普通 application/json 类型
        print(BaseTrafficParser.simplify_request(url="http://10.211.55.2:8887/v1/os_command_injection/test_case3",
                                                 data='{"name":"23333"}', http_method=HttpMethod.POST,
                                                 content_type=ContentType.ResourceContentType.JSON))

        json1 = '{"name":{"pass": {"bb": 12222, "aa": {"hello": "xxx"}}}, "hello": "ssss"}'
        simplify_request5 = BaseTrafficParser.simplify_request(
            url="http://10.211.55.2:8889/v1/os_command_injection/test_case3", data=json1, http_method=HttpMethod.POST,
            content_type=ContentType.ResourceContentType.JSON)
        print(simplify_request5)
        self.send_data(simplify_request5)

        json2 = '{"name":"chenming","whoamo":"xxxx344"}'
        simplify_request6 = BaseTrafficParser.simplify_request(
            url="http://10.211.55.2:8889/v1/os_command_injection/test_case3", data=json2, http_method=HttpMethod.POST,
            content_type=ContentType.ResourceContentType.JSON)
        self.send_data(simplify_request6)

        # 普通 text/xml 类型，暂不支持
        print(BaseTrafficParser.simplify_request(url="http://10.211.55.2:8887/v1/os_command_injection/test_case3",
                                                 data="<name>23333</name>", http_method=HttpMethod.POST,
                                                 content_type=ContentType.ResourceContentType.XML))

        upload_data1 = """------WebKitFormBoundaryH0TGOzR6zJhOJSVB \nContent-Disposition: form-data; name="file"; filename="5.png" \nContent-Type: image/png \nXXXXXX \n------WebKitFormBoundaryH0TGOzR6zJhOJSVB--"""
        upload_data2 = """
               ------WebKitFormBoundarydnAY6LXdz8oOOXxy\\r\\nContent-Disposition: form-data; name=\\\"file\\\"; filename=\\\"5.png\\\"\\r\\nContent-Type: image/png\\r\\n\\r\\n\
               """

        # 普通上传文件表单 multipart/form-data; boundary=----WebKitFormBoundaryH0TGOzR6zJhOJSVB，
        simplify_request7 = BaseTrafficParser.simplify_request(
            url="http://10.211.55.2:8889/v1/os_command_injection/test_case3", data=upload_data1,
            http_method=HttpMethod.POST, content_type=ContentType.ResourceContentType.FORM)
        print(simplify_request7)
        # self.send_data(simplify_request7)

    def send_data(self, simplify_request):
        import requests
        http_method = simplify_request["http_method"]
        url = simplify_request["url"]
        data = simplify_request["data"]
        headers = {"Content-Type": simplify_request["content_type"]}
        print(simplify_request)
        # requests.request(method=http_method, url=url, data=data, headers=headers)

    def testADDPocData(self):
        # 测试增加poc
        from common.http_util import HttpMethod
        from common.http_util import ContentType
        from parser.base_traffic_parser import BaseTrafficParser

        # 测试get 请求
        print(BaseTrafficParser.add_poc_data(url="http://127.0.0.1/?name=23232&password=78812", data=None,
                                             http_method=HttpMethod.GET, content_type=None, poc="eval"))
        print(BaseTrafficParser.add_poc_data(url="http://127.0.0.1/?name=中文&password=78812", data=None,
                                             http_method=HttpMethod.GET, content_type=None, poc="eval"))
        print(BaseTrafficParser.add_poc_data(url="http://127.0.0.1/?name=%E4%B8%AD%E6%96%87&password=78812", data=None,
                                             http_method=HttpMethod.GET, content_type=None, poc="eval"))
        print(BaseTrafficParser.add_poc_data(url="http://127.0.0.1/?name=中文&password=78812#", data=None,
                                             content_type=None, http_method=HttpMethod.GET, poc="eval"))
        print(BaseTrafficParser.add_poc_data(url="http://127.0.0.1/?name=中文……**$$$&password=78812、#", data=None,
                                             content_type=None, http_method=HttpMethod.GET, poc="eval"))
        print(BaseTrafficParser.add_poc_data(
            url="http://127.0.0.1/?name=中文&password=78812！@#¥%……*()_+|}{QASDFGHJK<>MNZXCVBN#",
            http_method=HttpMethod.GET, data=None, content_type=None, poc="eval"))

        print("=========post2=========")
        # 测试 post 请求
        # 普通 application/x-www-form-urlencoded 类型
        print(BaseTrafficParser.add_poc_data(url="http://127.0.0.1/login", data="name=23333&",
                                             http_method=HttpMethod.POST,
                                             content_type=ContentType.ResourceContentType.DEFAULT, poc="hack"))

        print(BaseTrafficParser.add_poc_data(url="http://127.0.0.1/login?name=23333&", data=None,
                                             http_method=HttpMethod.POST,
                                             content_type=None, poc="hack"))
        # 普通 application/json 类型
        print(BaseTrafficParser.add_poc_data(url="http://127.0.0.1/login", data='{"name":"23333"}',
                                             http_method=HttpMethod.POST,
                                             content_type=ContentType.ResourceContentType.JSON, poc="hack"))

        # print(BaseTrafficParser.get_parameter(url='{\\\"username\\\":\\\"admin\\\",\\\"password\\\":\\\"passss\\\"}', http_method=HttpMethod.POST, content_type=ContentType.ResourceContentType.JSON))
        # 普通 text/xml 类型，暂不支持
        print(BaseTrafficParser.add_poc_data(url="http://127.0.0.1/login", data="<name>23333</name>",
                                             http_method=HttpMethod.POST,
                                             content_type=ContentType.ResourceContentType.XML, poc="hack"))

        upload_data1 = """------WebKitFormBoundaryH0TGOzR6zJhOJSVB \n Content-Disposition: form-data; name="file"; filename="5.png" \n Content-Type: image/png \n XXXXXX \n ------WebKitFormBoundaryH0TGOzR6zJhOJSVB-- """
        upload_data2 = """
                        ------WebKitFormBoundarydnAY6LXdz8oOOXxy\\r\\nContent-Disposition: form-data; name=\\\"file\\\"; filename=\\\"5.png\\\"\\r\\nContent-Type: image/png\\r\\n\\r\\n\
                        """

        # 普通上传文件表单 multipart/form-data; boundary=----WebKitFormBoundaryH0TGOzR6zJhOJSVB，
        print(BaseTrafficParser.add_poc_data(url="http://127.0.0.1/upload", data=upload_data1,
                                             http_method=HttpMethod.POST,
                                             content_type=ContentType.ResourceContentType.FORM, poc="hack"))


if __name__ == "__main__":
    unittest.main()
