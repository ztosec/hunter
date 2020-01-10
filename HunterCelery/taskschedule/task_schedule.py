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
使用协程asyncio
"""
import json
import requests
import asyncio
import queue
from prettytable import PrettyTable
from deprecated import deprecated
from common import http_util
from common import log
from common.path import PLUGIN_ZIP_PATH, PLUGIN_PATH
from common.config_util import get_system_config
from common.system_util import unzip_file
from common.http_util import download_file
from common.plugin_config.localfile_plugin_config import LocalFilePluginConfig
from plugins.base.vuln_enum import PluginSwith
from plugins.base.base_checker import BaseChecker
from model.vulnerability import Vulnerability, VulnerabilityService
from common.plugins_util import load_checkers, load_default_checkers, modify_default_checkers
from model.default_value import TaskStatus

logger = log.get_default_logger()


async def run_plugin(package, plugin_instance, results_queue):
    """
    异步执行插件结果
    :param package: 
    :param plugin_instance: 
    :param results_queue: 
    :return: 
    """
    try:
        if plugin_instance.useable == PluginSwith.ON:
            logger.info('plugin {} task start'.format(plugin_instance.info['name']))
            result = await plugin_instance.async_check_vuln(package)
            if result is not None and result['status']:
                results_queue.put(result)
            logger.info('plugin {} task done'.format(plugin_instance.info['name']))
    except Exception as e:
        logger.exception("run_plugin error")


def modify_checker(broadcast):
    """
    修改本地插件配置信息，只修改本地配置文件
    
    {"type": "plugin", "action": "modify", "data": {"name": checker_name, "switch": PluginSwith.ON}
    :param broadcast: 
    :return: 
    """
    checker_name = broadcast["data"]["name"]
    switch = broadcast["data"]["switch"]
    checkers_dict = load_default_checkers()
    if checker_name in checkers_dict:
        logger.info('接收到修改插件{}状态为{}的请求'.format(checker_name, switch))
        LocalFilePluginConfig().modify_plugin_config(checker_name, "useable", switch)
        modify_default_checkers()


def remove_checker(broadcast):
    """
    移除插件，不做物理删除，只从内存中移除

    {"type": "plugin", "action": "modify", "data": {"name": checker_name, "switch": PluginSwith.ON}
    :param broadcast: 
    :return: 
    """
    checker_name = broadcast["data"]["name"]
    checkers_dict = load_default_checkers()
    if checker_name in checkers_dict:
        logger.info('从插件列表中移除插件{}'.format(checker_name))
        checkers_dict.pop(checker_name)


def insert_checker(broadcast):
    """
    新增插件，新增指定插件名插件，简单操作
    :param broadcast: 
    :return: 
    """
    checker_name = broadcast["data"]["name"]
    logger.info("download %s checkers from master" % checker_name)
    # logger.info("%s checkers save to path %s" % (checker_name, checker_path))
    download_newest_checkers()


def download_newest_checkers():
    """
    第一次启动时同步插件，从服务端下载最新的插件，
    :return: 
    """
    logger.info("download newest checkers when the system starts up")
    try:
        master_checkers_url = get_system_config()["front_end"]["master_checkers_url"]
        download_file(url=master_checkers_url, save_fp=PLUGIN_ZIP_PATH)
        unzip_file(origin_file=PLUGIN_ZIP_PATH, target_folder=PLUGIN_PATH)
        logger.info("download newest checkers successfully, it still using newest checkers")
    except Exception as e:
        if isinstance(e, requests.exceptions.ConnectTimeout):
            logger.warn("sorry,download newest checkers timeout, it still using old checkers")
        else:
            logger.warn("sorry,download newest checkers error, it still using old checkers")
    finally:
        load_default_checkers(True)
        modify_default_checkers()


def scan(package, task_id, create_user, status):
    """
    
    :param package: 
    :param task_id: 
    :param create_user: 
    :param status: 
    :return: 
    """
    from model.url import UrlService, Url

    # logger.setLevel(logging.DEBUG)

    classification_url, classification_data = parse_package(package)
    # 保存URL
    url_task = UrlService.save(status=TaskStatus.WAITING, origin_data=package, task_id=task_id,
                               classification_url=classification_url, classification_data=classification_data)

    result_queue = queue.Queue()  # 结果队列
    logger.info("hunter task has started")
    # 加载插件
    checker_list = load_default_checkers()
    # checker_list = load_checkers(modle_names)
    logger.info('loading package success')
    logger.info('loading plugin success')
    try:
        future_tasks = list()
        for checker_name, checker_instance in checker_list.items():
            future_tasks.append(asyncio.ensure_future(run_plugin(package, checker_instance, result_queue)))
        # 更新URL数据库状态
        UrlService.update(fields=({Url.status: TaskStatus.WORKING}), where=(Url.id == url_task.id))
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(future_tasks))
        # loop.close()
    except KeyboardInterrupt as e:
        logger.exception("scan error")
    finally:
        UrlService.update(fields=({Url.status: TaskStatus.DONE}), where=(Url.id == url_task.id))
        # UrlService.update_url_status(TaskStatus.DONE, url_task.id)
        logger.info("hunter task has done")
        print_result(url_task, result_queue)


def parse_package(package):
    """
    解析数据包
    :param package: 
    :return: 
    """
    http_method = str(package["method"]).lower()
    temp_url = str(package["url"]).strip()
    temp_headers = http_util.header_to_lowercase(json.loads(package['headers']))
    content_type = temp_headers[
        "content-type"] if temp_headers is not None and http_util.ContentType.NAME.lower() in temp_headers else None
    temp_data = package['data'] if "data" in package else None

    parser_result = BaseChecker.get_parser_class(package).simplify_request(url=temp_url, data=temp_data,
                                                                           http_method=http_method,
                                                                           content_type=content_type)

    return parser_result["url"], json.dumps(parser_result)


@deprecated(version='2.0', reason="You should use another function")
def add_job(jobqueue, modle_names):
    """
    addjob
    :param targets: 
    :param jobqueue: 
    :return: 
    """
    plugin_list = load_checkers(modle_names)
    for plugin in plugin_list:
        jobqueue.put(plugin)


def print_result(url, results):
    """
    输出结果到表格
    :return:
    info: 为该漏洞的信息
    path: 该插件的实际位置(保留，用于验证)
    payload: payload
    imp_version: 影响版本
    error:错误日志
    repair: 修复建议
    type:漏洞类型  'cors',
    chinese_type: 中文漏洞类型 请求对象共享
    description: 漏洞详情 由于配置不当，导致可以通过设置Origin来控制Access-Control-Allow-Methods,参考链接http://www.freebuf.com/articles/web/18493.html
    level:等级 middle
    """
    # logger.setLevel(logging.DEBUG)
    logger.info('hunter find %s vulnerables' % results.qsize())
    table = PrettyTable(["id", "name", "info", "payload", "imp_version"])
    table.align["id"] = "l"
    table.align["name"] = "l"
    table.align["info"] = "l"
    table.align["payload"] = "l"
    table.align["imp_version"] = "l"
    table.padding_width = 1  # 填充宽度
    for i in range(0, results.qsize()):
        result = results.get_nowait()
        table.add_row(
            [i + 1, result['details']['name'], result['info'], result['payload'], result['details']['imp_version']])
        # 保存漏洞到数据库
        task_id = url.task_id if url.task_id else None
        VulnerabilityService.save(url_id=url.id, task_id=task_id, info=result['info'], plugin_info=None,
                                  payload=result["payload"],
                                  imp_version=result['details']['imp_version'], error=''.join(result['error']),
                                  repair=result['details']['repair'], type=result['details']['type']['fullname'],
                                  chinese_type=result['details']['type']['fullchinesename'],
                                  description=result['details']['description'],
                                  level=result['details']['type']['level'],
                                  origin_data=None)
    logger.warn("\n" + str(table))
