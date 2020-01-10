#!/ usr/bin/env
# coding=utf-8
"""
author: b5mali4
Copyright (c) 2018
To use:
"""
import unittest


class MessageQueueTestCase(unittest.TestCase):
    def testPushXssRawTrafficMessage(self):
        """
        测试向消息队列中推送大量的流量数据
        :return: 
        """
        from hunter_celery import scan_celery
        from model.default_value import TaskStatus

        num = 0

        xssfork_raw_data = {'type': 'main_frame',
                            'url': 'http://10.211.55.2:65412/?foobar#lang=en',
                            'method': 'get',
                            'headers': '{"Upgrade-Insecure-Requests":"1","User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36","Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8","Accept-Encoding":"gzip, deflate","Accept-Language":"zh-CN,zh;q=0.9"}'}

        while num < 100:
            task_id = 1
            current_user_name = 'mingchen'
            scan_celery.delay(xssfork_raw_data, task_id, current_user_name, TaskStatus.DONE)
            num += 1

    def testCommandExecuteTrafficMessage(self):
        """
        测试命令执行
        :return: 
        """
        from hunter_celery import scan_celery
        from model.default_value import TaskStatus

        num = 0

        command_execute_raw_data = {'type': 'main_frame',
                            'url': 'http://10.211.55.2:65412/?domain=1',
                            'method': 'get',
                            'headers': '{"Upgrade-Insecure-Requests":"1","User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36","Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8","Accept-Encoding":"gzip, deflate","Accept-Language":"zh-CN,zh;q=0.9"}'}

        while num < 9:
            task_id = 2
            current_user_name = 'mingchen'
            scan_celery.delay(command_execute_raw_data, task_id, current_user_name, TaskStatus.DONE)
            num += 1


    def testPushFastJsonRceTrafficMessage(self):
        """
        测试向消息队列中推送大量的流量数据,测试fastjson漏洞
        :return: 
        """
        from hunter_celery import scan_celery
        from model.default_value import TaskStatus

        num = 0

        fastjson_raw_data = {'type': 'xmlhttprequest', 'url': 'http://10.211.55.2:8080/product/buy', 'method': 'post',
                             'data': '"{\\"id\\":\\"0\\",\\"productId\\":\\"1\\",\\"description\\":\\"2\\",\\"price\\":\\"3\\",\\"imageUrl\\":\\"4\\"}"',
                             'data_type': 'raw', 'parser': 'chrome-plugin',
                             'headers': '{"Accept":"*/*","Origin":"http://10.211.55.2:8080","X-Requested-With":"XMLHttpRequest","User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36","content-type":"application/json","Referer":"http://10.211.55.2:8080/product/new","Accept-Encoding":"gzip, deflate","Accept-Language":"zh-CN,zh;q=0.9","Cookie":"session=eyJ1c2VyX25hbWUiOiJtaW5nY2hlbiJ9.EFeQ4A.ivmaggQMMMCkNmch9u0UL_CB2gE"}'}

        while num < 100:
            task_id = 2567
            current_user_name = 'mingchen'
            scan_celery.delay(fastjson_raw_data, task_id, current_user_name, TaskStatus.DONE)
            num += 1

    def testPushHunterRawTrafficMessage(self):
        """
        测试向消息队列中推送大量的流量数据
        :return: 
        """
        from hunter_celery import scan_celery
        from model.default_value import TaskStatus

        num = 0
        post_data = {
            "requestid": "117723",
            "type": "main_frame",
            "url": "http://10.211.55.2:65412/?id=",
            "method": "get",
            "parser": "chrome-plugin",
            "headers": "{\"Upgrade-Insecure-Requests\":\"1\",\"User-Agent\":\"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36\",\"Accept\":\"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3\",\"Referer\":\"http://10.211.55.2:65412/\",\"Accept-Encoding\":\"gzip, deflate\",\"Accept-Language\":\"zh-CN,zh;q=0.9\",\"Cookie\":\"session=eyJ1c2VyX25hbWUiOiJtaW5nY2hlbiJ9.EEysIw.e8YSvUTd3A51RNLuU2FymcJnjyY\"}"
        }

        weak_pass_wprd_raw_data = {'type': 'main_frame',
                                   'url': 'http://10.211.55.4/xml/example1.php?user=admin&password=123456',
                                   'method': 'get',
                                   'headers': '{"Upgrade-Insecure-Requests":"1","User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36","Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8","Accept-Encoding":"gzip, deflate","Accept-Language":"zh-CN,zh;q=0.9"}'}

        sql_inject_raw_data = {'type': 'main_frame',
                               'url': 'http://10.211.55.2:65412/?id=2',
                               'method': 'get',
                               'headers': '{"Upgrade-Insecure-Requests":"1","User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36","Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8","Accept-Encoding":"gzip, deflate","Accept-Language":"zh-CN,zh;q=0.9"}'}

        while num < 10:
            task_id = 2
            current_user_name = 'mingchen'
            scan_celery.delay(sql_inject_raw_data, task_id, current_user_name, TaskStatus.DONE)
            num += 1

        exit()

        while num < 20000:
            task_id = 3
            current_user_name = 'test'
            post_data["url"] = "http://10.211.55.2:65412/?id=" + str(num)
            scan_celery.delay(post_data, task_id, current_user_name, TaskStatus.DONE)
            num += 1

    def testPushSystemNoticeMessage(self):
        """
        测试向消息队列中推送大量的系统广播消息
        :return: 
        """
        from hunter_celery import system_notice_celery
        from model.default_value import TaskStatus
        from common.broadcast_value import BroadCastType, BroadCastAction
        from plugins.base.vuln_enum import PluginSwith

        num = 0
        switch = True
        """测试禁用插件"""
        disables = ["fastjson1", "fastjson2", "kafaka2333", "cmd_exec"]
        while num < 4:
            switch = not switch
            """
            system_notice_celery.delay(broadcast={"type": BroadCastType.PLUGIN, "action": BroadCastAction.MODIFY_PLUGIN,
                                                  "data": {"name": disables[num],
                                                           "switch": PluginSwith.ON if switch else PluginSwith.OFF}})
            """
            system_notice_celery.delay(broadcast={"type": BroadCastType.PLUGIN, "action": BroadCastAction.MODIFY_PLUGIN,
                                                  "data": {"name": disables[num],
                                                           "switch": PluginSwith.ON}})
            num += 1

    def testPushSystemNoticeMessage(self):
        """
        测试向消息队列中推送大量的系统广播消息
        :return: 
        """
        from hunter_celery import system_notice_celery
        from model.default_value import TaskStatus
        from common.broadcast_value import BroadCastType, BroadCastAction
        from plugins.base.vuln_enum import PluginSwith

        num = 0
        switch = True
        """测试禁用插件"""
        disables = ["xssfork"]
        while num < 1:
            switch = not switch
            system_notice_celery.delay(broadcast={"type": BroadCastType.PLUGIN, "action": BroadCastAction.MODIFY_PLUGIN,
                                                  "data": {"name": disables[num],
                                                           "switch": PluginSwith.OFF}})
            num += 1

    def testPushRawTrafficMessageAndSendEmail(self):
        """
        测试向消息队列中推送大量的流量数据，发现任务完成之后是否能发送邮件
        :return: 
        """
        from hunter_celery import scan_celery
        from model.default_value import TaskStatus
        from model.task import Task, TaskService
        from model.url import Url, UrlService
        from model.vulnerability import Vulnerability, VulnerabilityService


        task_id = 2563
        current_user_name = 'mingchen'
        scan_celery.delay(None, task_id, current_user_name, TaskStatus.WORKING)

        num = 0

        xssfork_raw_data = {'type': 'main_frame',
                            'url': 'http://10.211.55.2:65412/?path=',
                            'method': 'get',
                            'headers': '{"Upgrade-Insecure-Requests":"1","User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36","Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8","Accept-Encoding":"gzip, deflate","Accept-Language":"zh-CN,zh;q=0.9"}'}

        while num < 1:
            current_user_name = 'mingchen'
            scan_celery.delay(xssfork_raw_data, task_id, current_user_name, TaskStatus.DONE)
            num += 1

        scan_celery.delay(None, task_id, current_user_name, TaskStatus.KILLED)


if __name__ == "__main__":
    unittest.main()
