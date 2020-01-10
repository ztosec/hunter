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
>>> python xsseye.py -u "http://10.211.55.2:8090/?v=0.2"
>>> python xsseye.py -u "http://10.211.55.2:8090/login" -d "name=1&password=233" -H "{\"Content-Type\": \"application/x-www-form-urlencoded\"}"
>>> python xsseye.py -u "http://10.211.55.2:8090/login" -d "{\"name\":\"23333\"}" -H "{\"Content-Type\": \"application/json\"}"
"""
import os
import copy
import logging
import json
import argparse
import asyncio
import multiprocessing
from ctypes import c_bool
from common import log
from pyppeteer import launch
from common import http_util
from common.logo import logo
from common.system_util import split_array
from common.settings import BROWSER_DEAD_TIME
from common.config_util import get_payloads, PAYLOAD_TAG
from pyppeteer.errors import PyppeteerError
from pyppeteer.errors import NetworkError
from prettytable import PrettyTable
from parser.base_traffic_parser import BaseTrafficParser

# 发现漏洞后结束
logger = log.get_default_logger()


class Request:
    # 发现漏洞后结束
    finshed = multiprocessing.Value('i', 0)
    url = None
    method = http_util.HttpMethod.GET
    data = None
    headers = None
    celery_task_id = None
    result_queue = multiprocessing.Manager().Queue()


async def open_browser():
    """
    :return: 
    """
    browser = await launch(headless=True, args=['--disable-xss-auditor', '--no-sandbox'])
    return browser


def save_vulnerability(poc_result, task_id):
    """
    保存漏洞到数据库
    :param poc_result: 
    :param task_id: 
    :return: 
    """
    from model.vulnerability import Vulnerability, VulnerabilityService

    if task_id is None:
        return
    # 保存漏洞到数据库
    xss_type = {'fullname': 'xss', 'fullchinesename': 'xss跨站脚本攻击', 'level': 'high'}
    info = "{}存在一个xss漏洞".format(poc_result["url"])
    imp_version = "所有版本"
    repair = "过滤掉<,>,',等特殊字符"
    type = xss_type["fullname"]
    chinese_type = xss_type["fullchinesename"]
    description = "XSS攻击全称跨站脚本攻击，XSS是一种在web应用中的计算机安全漏洞，它允许恶意web用户将代码植入到提供给其它用户使用的页面中m，详情请参考http://wiki.dev.ztosys.com/pages/viewpage.action?pageId=21743578"
    level = xss_type["level"]
    VulnerabilityService.save(info=info, payload=json.dumps(poc_result), imp_version=imp_version, repair=repair,
                              type=type, chinese_type=chinese_type, description=description, level=level,
                              task_id=task_id)


def print_result():
    """
    :param url: 
    :return: 
    """
    if Request.result_queue.empty():
        return
    logger.warn("[!] xsseye find 1 XSS Vulnerability")
    table = PrettyTable(["url", "data", "http_method", "headers"])
    table.align["url"] = "l"
    table.align["data"] = "l"
    table.align["http_method"] = "l"
    table.align["headers"] = "l"
    table.padding_width = 1  # 填充宽度
    for i in range(0, Request.result_queue.qsize()):
        result = Request.result_queue.get_nowait()
        table.add_row([result["url"], result["data"], result["http_method"], result["headers"]])
        # 保存到数据库
        if Request.celery_task_id and Request.finshed.value == 0:
            Request.finshed.value = 1
            save_vulnerability(poc_result=result, task_id=Request.celery_task_id)
    logger.warn("\n" + str(table))


def add_result_queue(poc_result):
    Request.result_queue.put(poc_result)


async def hook_request(req, url, method, data, headers, payload):
    """
    修改请求方式和请求头,请求数据，修复重复跳转问题
    await req.respond({'body': 'YO, GOOGLE.COM'})
    data = {
        'method': 'POST',
        'postData': 'paramFoo=valueBar&paramThis=valueThat'
    }
    await req.continue_(data)
    :param req: 
    :return: 
    """
    if req.method == method and req.url == url and req.postData == data:
        content_type, headers_dic = get_content_type_headers(method, headers)
        poc_result = BaseTrafficParser.add_poc_data(url=url, data=data, content_type=content_type, http_method=method,
                                                    poc=payload)
        try:
            overrides = dict()
            if poc_result["data"]:
                overrides["postData"] = poc_result["data"]
            if headers_dic:
                overrides["headers"] = headers_dic
            if method:
                overrides["method"] = method
            if poc_result["url"]:
                overrides["url"] = poc_result["url"]
            await req.continue_(overrides)
        except PyppeteerError:
            await req.continue_()
    else:
        await req.continue_()


def get_content_type_headers(method, headers):
    """
    根据请求方式和请求头确定content_type
    :return: 
    """
    content_type = None
    headers_dic = None
    if method == http_util.HttpMethod.POST:
        content_type = http_util.ContentType.ResourceContentType.DEFAULT

    try:
        headers_dic = json.loads(headers)
        for (header_name, headers_value) in headers_dic.items():
            headers_dic.pop(header_name)
            headers_dic[header_name.lower()] = headers_value

        if headers_dic is not None and http_util.ContentType.NAME.lower() in headers_dic:
            content_type = headers_dic["content-type"]
    except Exception:
        pass
    return content_type, headers_dic


async def hook_dialog(dialog, url, method, data, headers, celery_task_id, payload):
    """
    hook dialog事件，然后输出payload
    :param dialog: 
    :return: 
    """
    if dialog.message == PAYLOAD_TAG:
        content_type, headers_dic = get_content_type_headers(method, headers)
        poc_result = BaseTrafficParser.add_poc_data(url=url, data=data, content_type=content_type, http_method=method,
                                                    poc=payload)
        poc_result["headers"] = headers_dic
        # notify(poc_result, headers, celery_task_id)
        add_result_queue(poc_result)
    await dialog.dismiss()


async def fuzz_payload(browser, url, method, data, headers, celery_task_id, payload):
    """
    测试是否插入新标签，测试是否执行触发payload，增加是否跳转判断，有缺陷，fuzz到漏洞之后应该推出
    :param url: 
    :param method: 
    :param data: 
    :param headers: 
    :param payload: 
    :return: 
    """
    try:
        page = await browser.newPage()
        await page.setRequestInterception(True)
        page.on(
            'dialog',
            lambda dialog: asyncio.ensure_future(
                hook_dialog(dialog, url, method, data, headers, celery_task_id, payload))
        )
        page.on('request', lambda req: hook_request(req, url, method, data, headers, payload))
        await page.goto(url)
        # await asyncio.wait([page.waitForNavigation(),])
        await page.evaluate('() => {var len=document.getElementsByTagName("xss").length;if (len > 0){alert("65534")}}')
        # await asyncio.wait([page.waitForNavigation(), ])
        # await page.close()
    except Exception as e:
        pass
        # if not isinstance(e, NetworkError, ):
        #    logger.exception("fuzz_payload error")


async def fuzz_payloads(payloads):
    """
    这个函数执行进程数次
    :param websites: 
    :return: 
    """
    try:
        browser = await open_browser()
        # 顺序打开
        if isinstance(payloads, str):
            payloads = [payloads]
        tasks = [
            fuzz_payload(browser, Request.url, Request.method, Request.data, Request.headers, Request.celery_task_id,
                         payload) for payload in payloads]
        await asyncio.wait(tasks)
        await asyncio.sleep(BROWSER_DEAD_TIME)
        await browser.close()
    except Exception:
        pass


def help():
    """
    帮助，主要显示各个传参
    :return: 
    """
    apiparser = argparse.ArgumentParser()
    apiparser.add_argument("-u", "--url", help="请求的路径,完整例子如下:http://127.0.0.1/xss1?name=1", action="store", default='')
    apiparser.add_argument("-m", "--method", help="请求方式", action="store", default='get')
    apiparser.add_argument("-d", "--data", help="请求的数据", action="store")
    apiparser.add_argument("-H", "--headers", help="请求头", action="store")
    apiparser.add_argument("-c", "--celery", help="celery中的任务id", action="store")

    args = apiparser.parse_args()
    try:
        if args.url:
            main(args)
    except Exception:
        logger.exception("check error")


def handle_single_process(payloads):
    """
    :param websites: 
    :return: 
    """
    event_loop = asyncio.get_event_loop()
    try:
        event_loop.run_until_complete(fuzz_payloads(payloads))
    finally:
        event_loop.close()


def main(args):
    """
    使用多进程+协程模式执行fuzz_payload函数
    :param args: 
    :return: 
    """
    if http_util.check_is_alive(args.url, args.method, args.data, args.headers):
        Request.url = args.url
        Request.method = args.method.upper()
        Request.data = args.data
        Request.headers = args.headers
        Request.celery_task_id = args.celery
        payloads = list(get_payloads())
        # payloads = ["<xss></xss>"]
        processes_num = len(payloads) if len(payloads) <= os.cpu_count() else os.cpu_count()
        payloadss = split_array(payloads, processes_num)
        # 进程池
        with multiprocessing.Pool(processes_num) as porcess_pool:
            porcess_pool.map(handle_single_process, payloadss)
        print_result()


def print_logo():
    logger = log.get_default_logger()
    logger.setLevel(logging.DEBUG)
    logger.info(logo)


if __name__ == "__main__":
    print_logo()
    help()
