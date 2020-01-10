#!/ usr/bin/env
# coding=utf-8
"""
author: b5mali4
Copyright (c) 2018
"""

import unittest
from common.http_util import ContentType
from common.http_util import HttpMethod
from common.url_data_classification import UrlDataClassification


class UrlDataClassIficationTestCase(unittest.TestCase):
    def testGetJsonParameter(self):
        """
        对url分类和提取关键字
        :return: 
        """
        str3 = '{"name":{"pass": [{"bb":"xxx", "aaa": "bb"}, {"bb":"xxx34444444", "aaa": "bb"}]}, "hello": "ssss"}'
        print(UrlDataClassification.get_json_parameter(str3))

    def testgetParameter(self):
        print(UrlDataClassification.get_parameter(url="http://127.0.0.1/xxx.php?id=<root>2333</root>"))
        print(UrlDataClassification.get_parameter(url='http://127.0.0.1/xxx.php?id=cdd&name=3344'))
        print(UrlDataClassification.get_parameter(url='http://127.0.0.1/xxx.php?id=cdd&name=3344'))

    def testAddXxe(self):
        print(UrlDataClassification.add_xxe(url="http://127.0.0.1/xxx.php?id=<root>2333</root>", xxe_poc="<xxx>"))
        print(UrlDataClassification.add_exec(url='http://127.0.0.1/xxx.php?id=cdd&name=3344',
                                             cmd_poc='|cat /etc/passwd'))

    def testSimplifyUrl(self):
        print(UrlDataClassification.simplify_url(url='{"name":"334456","whoamo":"xxxx344"}', http_method="post", content_type=ContentType.ResourceContentType.JSON))

        print(UrlDataClassification.simplify_url(url='name=233&pass=34', http_method="post",
                                                 content_type=ContentType.ResourceContentType.DEFAULT))

        print(UrlDataClassification.simplify_url(url='<root>2333</root>', http_method="post",
                                                 content_type=ContentType.ResourceContentType.XML))

        print(UrlDataClassification.simplify_url(url='<root><username>1212</username></root>', http_method="post",
                                                 content_type=ContentType.ResourceContentType.XML))

        print(UrlDataClassification.simplify_url(url='name=233&pass=34'))
        print(type(UrlDataClassification.simplify_url(url='{"name":"334456","whoamo":"xxxx344"}',
                                                      content_type=ContentType.ResourceContentType.JSON)))
        print(UrlDataClassification.simplify_url(url='http://10.211.55.4/css/bootstrap.css'))
        print(UrlDataClassification.simplify_url(url='http://127.0.0.1/xxx.php?id=cdd&name=3344'))
        print(UrlDataClassification.simplify_url('name=334456&whoamo=1', 'post'))
        print(UrlDataClassification.simplify_url(
            'http://127.0.0.1:65412/?xml=%3C!DOCTYPE%20xxe%20SYSTEM%20%22http://127.0.0.1:2333/xxe%22%3E%3Croot%3Etest%3C/root%3E',
            'get'))

    def testAddPocData(self):
        """
        测试poc替换
        :return: 
        """
        # get url
        print(UrlDataClassification.add_poc_data(url='http://127.0.0.1/xxx.php?id=cdd&name=3344', http_method=HttpMethod.GET, content_type=None, poc="kokoko"))
        # post url
        print(UrlDataClassification.add_poc_data(url='http://127.0.0.1/xxx.php?id=cdd&name=3344', http_method=HttpMethod.POST, content_type=None, poc="kokoko"))
        # post data
        print(UrlDataClassification.add_poc_data(url='name=233&pass=34', http_method=HttpMethod.POST, content_type=ContentType.ResourceContentType.DEFAULT, poc="kokoko"))
        # post data
        print(UrlDataClassification.add_poc_data(url='{"name":"334456","whoamo":"xxxx344"}', http_method=HttpMethod.POST, content_type=ContentType.ResourceContentType.DEFAULT, poc="kokoko"))
        # post json
        print(UrlDataClassification.add_poc_data(url='{"name":"334456","whoamo":"xxxx344"}', http_method=HttpMethod.POST, content_type=ContentType.ResourceContentType.JSON, poc="kokoko"))
        # post xml
        # post file_form


if __name__ == "__main__":
    unittest.main()
