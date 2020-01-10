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
import os
import sys
import json
import time
import datetime
from flask import request, session, jsonify, Blueprint, make_response, send_file, send_from_directory
from common import json_utils
from common import log
from common.system_util import minutes_
from common.path import CLIENT_ROOT_PATH, CHROME_CLIENT_NAME
from common.aes_util import generate_access_key
from model.task import Task, TaskService
from model.default_value import TaskStatus
from model.user_task import UserTask, UserTaskService
from model.url import Url, UrlService
from model.user import User, UserService
from model.default_value import Role
from model.system_config import SystemConfigService
from model.vulnerability import VulnerabilityService
from api.service.redis_service import RedisService
from hunter_celery import scan_celery
from common.system_util import get_current_time
from exception.hunter_web_exception import UserNotFoundInRedisException
from api.authentication.auth_module_factory import check_authentication

logger = log.get_default_logger()
user_web_api = Blueprint('user_web_api', __name__, url_prefix="/api/v1/user/")


@user_web_api.route('/tasks/', methods=['POST'], endpoint='create_task')
@check_authentication(role=Role.USER)
def create_task():
    """
    创建任务，可以由浏览器插件或者直接在平台上创建，redis缓存查询用户信息
    :return: 
    """
    try:
        post_data = request.get_json(force=True)
        if json_utils.has_dict_value_blank(post_data, ['hook_rule', 'read_agreement', 'task_name']):
            return jsonify(status=400, message="创建任务失败", data={"extra_info": "新建任务时没有设置网址正则或任务名称"})
        if not post_data.get("read_agreement"):
            return jsonify(status=400, message="创建任务失败", data={"extra_info": "请阅读用户协议并点击同意"})
        current_user_name = session["user_name"]
        post_hook_rule = post_data.get("hook_rule")
        post_task_name = post_data.get("task_name")

        current_user = RedisService.get_user(user_name=current_user_name)
        receivers_email = current_user["email"] if "email" in current_user else None
        task = TaskService.save(create_user_id=current_user["id"], task_name=post_task_name,
                                receivers_email=receivers_email, hook_rule=post_hook_rule)
        #if UserTaskService.count(where=(UserTask.task_id == task.id, UserTask.user_id == current_user["id"])) == 0:
        UserTaskService.save(task_id=task.id, user_id=current_user["id"])
        RedisService.create_task(task.id, post_hook_rule, current_user_name, TaskStatus.WORKING)
        RedisService.update_user_field(current_user_name, "current_task_id", task.id)
        UserService.update(fields=({User.recent_operation_time: datetime.datetime.now()}),
                           where=(User.user_name == current_user_name))
        task_access_key = generate_access_key(task.id, current_user_name).decode("utf-8")
        TaskService.update(fields=({Task.access_key: task_access_key}), where=(Task.id == task.id))
        scan_celery.delay(post_data, task.id, current_user_name, TaskStatus.WORKING)
        return jsonify(status=200, message="创建任务成功", data={"task_id": task.id, "full_name": current_user["full_name"],
                                                           "create_time": get_current_time(),
                                                           "task_access_key": task_access_key})

    except Exception as e:
        logger.exception("create_task exception")
        return jsonify(status=500, message="未知异常", data={"extra_info": "创建任务时出现未知异常，请联系管理员查看异常日志"})


@user_web_api.route('/tasks/', methods=['DELETE'], endpoint='stop_task')
@check_authentication(role=Role.USER)
def stop_task():
    """
    关闭任务，关闭任务之后将用户任务信息进行持久化到数据库，包括结束任务时间
    
    :return: 
    """
    post_data = request.get_json(force=True)
    if json_utils.has_dict_value_blank(post_data, ["task_id"]):
        return jsonify(status=400, message="结束任务失败", data={"extra_info": "task_id缺失,无法结束任务"})

    post_task_id = int(post_data.get("task_id"))
    current_user_name = session["user_name"]
    try:
        user = RedisService.get_user(current_user_name)
        if UserTaskService.count(where=(UserTask.user_id == user["id"], UserTask.task_id == post_task_id)) == 0:
            return jsonify(status=403, message="结束任务失败", data={"extra_info": "请勿尝试非法关闭非自己权限任务"})
        task = TaskService.get_fields_by_where(fields=(Task.task_status), where=(Task.id == post_task_id))[0]
        if task.task_status in [TaskStatus.DONE, TaskStatus.KILLED]:
            return jsonify(status=200, message="结束任务成功",
                           data={"fullname": user["full_name"], "extra_info": "该任务早已经结束,请登录后台查看扫描结果",
                                 "stop_time": get_current_time()})
        TaskService.update(fields=({Task.task_status: TaskStatus.KILLED, Task.killed_time: datetime.datetime.now()}),
                           where=(Task.id == post_task_id))
        UserService.update(fields=({User.recent_operation_time: datetime.datetime.now()}),
                           where=(User.user_name == current_user_name))
        scan_celery.delay(post_data, post_task_id, current_user_name, TaskStatus.KILLED)
        RedisService.stop_task(post_task_id)
        RedisService.clean_urlclassifications(post_task_id)
        return jsonify(status=200, message="结束任务成功",
                       data={"full_name": user["full_name"], "extra_info": "请登录后台查看扫描结果",
                             "stop_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")})
    except Exception as e:
        logger.exception("stop_task exception")
        if isinstance(e, UserNotFoundInRedisException):
            return jsonify(status=403, message="结束任务失败", data={"extra_info": "认证失败,请重新登录进行授权", "auth_site": ""})
        return jsonify(status=500, message="未知异常", data={"extra_info": "创建任务时出现未知异常，请联系管理员查看异常日志"})


@user_web_api.route('/tasks/', methods=['PUT'], endpoint='update_task')
@check_authentication(role=Role.USER)
def update_task():
    """
    更新任务信息，最主要的是修改hook_url
    :return: 
    """
    post_data = request.get_json(force=True)
    if json_utils.has_dict_value_blank(post_data, ["hook_rule", "task_id"]):
        return jsonify(status=400, message="更新任务失败", data={"extra_info": "请确认是否正确传入hook_rule,task_id参数"})

    try:
        post_hook_rule = post_data.get("hook_rule")
        post_task_id = post_data.get("task_id")
        current_user_name = session["user_name"]
        # current_user_name = "b5mali4"
        current_user = RedisService.get_user(current_user_name)
        if UserTaskService.count(
                where=(UserTask.user_id == int(current_user["id"]), UserTask.task_id == post_task_id)) == 0:
            return jsonify(status=403, message="更新任务失败", data={"extra_info": "请勿尝试非法更改非自己权限的任务"})
        TaskService.update(fields=({Task.hook_rule: post_hook_rule}), where=(Task.id == post_task_id))
        RedisService.update_task_hook_rule(post_task_id, post_hook_rule)
        return jsonify(status=200, message="更新任务成功", data={"extra_info": "修改成功,刷新页面即可看到更改结果"})
    except Exception as e:
        logger.exception("update_task exception")
        if isinstance(e, UserNotFoundInRedisException):
            return jsonify(status=403, message="结束任务失败", data={"extra_info": "请勿尝试非法关闭非自己权限任务"})
        return jsonify(status=500, message="未知异常", data={"extra_info": "创建任务时出现未知异常，请联系管理员查看异常日志"})


@user_web_api.route('/task/<int:task_id>/url/task_access_key/<string:task_access_key>', methods=['POST'], endpoint='check_url')
@check_authentication(role=Role.USER)
def check_url(task_id, task_access_key):
    """
    接收来自浏览器的流量，对流量进行解析分类之后，存放到redis中，支持多个用户同时协作对一个任务进行测试
    
    :param task_id: 
    :param task_access_key: 
    :return: 
    """
    from common.config_util import get_system_config
    try:
        post_data = request.get_json(force=True)
        current_user_name = session["user_name"]

        if TaskService.count(where=(Task.id == task_id, Task.access_key == task_access_key)) == 0:
            return jsonify(status=403, message="发送失败", data={"extra_info": "taskid或者accesskey不正确，插件请同步一次最新任务",
                                                             "site": get_system_config()['front_end']['index']})
        tasks = TaskService.get_fields_by_where(where=(Task.id == task_id, Task.access_key == task_access_key))

        if tasks[0].task_status in [TaskStatus.DONE, TaskStatus.KILLED]:
            return jsonify(status=400, message="发送失败", data={"extra_info": "该任务已经结束，客户端请重新同步或者创建最新任务",
                                                             "site": get_system_config()['front_end']['index']})

        if post_data is not None and "data" in post_data and RedisService.create_urlclassifications(task_id, post_data):
            raw_request_data = post_data.get('data', '{}')
            scan_celery.delay(raw_request_data, task_id, current_user_name, TaskStatus.NONE)
            return jsonify(status=200, message="发送成功", data={"extra_info": "发送到后端扫描引擎成功"})

        return jsonify(status=200, message="发送失败", data={"extra_info": "发送到后端引擎的数据不符合格式或者已经发送过"})

    except Exception as e:
        logger.exception("check_url exception")
        return jsonify(status=500, message="未知异常", data={"extra_info": "创建任务时出现未知异常，请联系管理员查看异常日志"})


@user_web_api.route('/current_task/', methods=['GET'], endpoint='show_current_task')
@check_authentication(role=Role.USER)
def show_current_task():
    """
    显示当前任务正在运行的任务
    :return: 
    """
    try:
        current_user_name = session["user_name"]
        current_user = RedisService.get_user(current_user_name)
        current_task = TaskService.get_working_tasks(user_id=current_user.id)[0]
        if current_task:
            hook_rule = RedisService.get_task(current_task.id)["hook_rule"]
            unscaned_url_num = UrlService.count(where=(Url.task_id == current_task.id, Url.status != TaskStatus.DONE))
            scaned_url_num = UrlService.count(where=(Url.task_id == current_task.id, Url.status == TaskStatus.DONE))
            total_url_num = unscaned_url_num + scaned_url_num
            if current_task.task_status in [TaskStatus.KILLED, TaskStatus.DONE]:
                percent = 100
            else:
                percent = 0 if total_url_num == 0 else (scaned_url_num / total_url_num) * 100
            response_data = jsonify(status=200, message="查询成功",
                                    data={'receiver_emails': current_task.receivers_email,
                                          'task_name': current_task.task_name,
                                          'create_time': current_task.created_time.strftime("%Y-%m-%d %H:%M"),
                                          'percent': percent,
                                          'unscaned_url_num': unscaned_url_num, 'scaned_url_num': scaned_url_num,
                                          'total_url_num': total_url_num, 'hook_rule': hook_rule,
                                          'task_id': current_task.id, "task_access_key": current_task.access_key,
                                          'task_status': current_task.task_status, 'user_name': current_user_name})
            return response_data
    except Exception as e:
        if isinstance(e, IndexError):
            return jsonify(status=400, message="获取失败", data={"extra_info": "后台无正在运行任务，请登录后台并创建任务"})
        logger.exception("show_current_task rasie error")
        return jsonify(status=500, message="获取失败", data={"extra_info": "未知异常，可以联系管理员到后台查看"})


@user_web_api.route('/current_tasks/', methods=['GET'], endpoint='show_current_tasks')
@check_authentication(role=Role.USER)
def show_current_tasks():
    """
    显示当前所有的任务列表，在响应中返回的结果为task_list和已经扫描的和未扫描的任务数目
    :return: 
    """
    try:
        working_tasks = list()
        completed_tasks = list()
        working_task_info_list = list()
        current_user_name = session["user_name"]
        current_user = RedisService.get_user(current_user_name)
        tasks = TaskService.get_tasks_url_vuln_num(user_id=current_user.id)
        for task in tasks:
            if task.task_status <= TaskStatus.WORKING:
                working_tasks.append(task)
            if task.task_status == TaskStatus.DONE:
                completed_tasks.append(task)

        for working_task in working_tasks:
            hook_rule = RedisService.get_task(working_task.id)["hook_rule"]
            unscaned_url_num = working_task.unscaned_urls_num
            scaned_url_num = working_task.scaned_urls_num
            total_url_num = unscaned_url_num + scaned_url_num
            if working_task.task_status in [TaskStatus.KILLED, TaskStatus.DONE]:
                percent = 100
            else:
                percent = 0 if total_url_num == 0 else int((scaned_url_num / total_url_num) * 100)

            working_task_info_list.append({'receiver_emails': working_task.receivers_email,
                                           'task_name': working_task.task_name,
                                           'create_time': working_task.created_time.strftime("%Y-%m-%d %H:%M"),
                                           'percent': percent,
                                           'unscaned_url_num': unscaned_url_num, 'scaned_url_num': scaned_url_num,
                                           'total_url_num': total_url_num, 'hook_rule': hook_rule,
                                           'task_id': working_task.id, "task_access_key": working_task.access_key,
                                           'task_status': working_task.task_status})
        response = jsonify(status=200, message="查询成功", data={"working_task_info_list": working_task_info_list,
                                                             "working_task_num": len(working_tasks) - 1 if len(
                                                                 working_tasks) > 0 else 0,
                                                             "completed_task_num": len(completed_tasks)})
        return response

    except Exception:
        logger.exception("show_current_tasks rasie error")
        return jsonify(status=500, message="未知异常", data={"extra_info": "创建任务时出现未知异常，请联系管理员查看异常日志"})


@user_web_api.route('/scan_record/', methods=['GET'], endpoint='show_scan_records')
@check_authentication(role=Role.USER)
def show_scan_records():
    try:
        current_user_name = session.get('user_name')
        current_user = RedisService.get_user(current_user_name)
        
        tasks = TaskService.get_tasks_url_vuln_num(user_id=current_user.id)
        response_data = list()

        for task in tasks:
            risk_level = VulnerabilityService.get_risk_level(task)
            response_data.append({"task_name": task.task_name, "created_time": task.created_time.strftime("%Y-%m-%d %H:%M"),
                          "task_id": task.id,
                          "urls_num": task.urls_num, "vulns_num": task.vulns_num, "risk_level": risk_level})

        response_data.reverse()

        return jsonify(status=200, message="查询成功", data=response_data)

    except Exception:
        logger.exception("show_current_tasks rasie error")
        return jsonify(status=500, message="未知异常", data={"extra_info": "创建任务时出现未知异常，请联系管理员查看异常日志"})


@user_web_api.route('/vulnerability/details/filter/', methods=['GET'], endpoint='vulnerability_details')
@check_authentication(role=Role.USER)
def vulnerability_details():
    """
    获取漏洞详情

    :return: 
    """
    try:
        task_id = request.args.get("task_id")
        current_user_name = session.get('user_name')
        current_user = RedisService.get_user(current_user_name)
        if int(current_user.role) < Role.ADMIN:
            current_user_task_count = UserTaskService.count(
                where=(UserTask.user_id == int(current_user.id), UserTask.task_id == task_id))
            if current_user_task_count == 0:
                return jsonify(status=403, message="查询失败", data={"extra_info": "请勿尝试非法查看"})
        return jsonify(status=200, message="查询成功", vlun=VulnerabilityService.get_vulnerabilitys_nltdr(task_id))

    except Exception as e:
        logger.exception("vulnerability_details rasie error")
        if isinstance(e, KeyError):
            return jsonify(status=400, message="查询失败", data={"extra_info": "未传递参数task_id"})
        return jsonify(status=500, message="未知异常", data={"extra_info": "获取漏洞详情出现未知异常，请联系管理员查看异常日志"})


@user_web_api.route('/vulnstatistics/count/', methods=['GET'], endpoint='show_vulnerability_count')
@check_authentication(role=Role.USER)
def show_vulnerability_count():
    """
    获取当前用户所有扫描记录漏洞集合，按照type和level分类

    :return: 
    """
    try:
        current_user_name = session.get('user_name')
        current_user = RedisService.get_user(current_user_name)
        vlun_level_type_nums = VulnerabilityService.get_vulnerability_count(current_user.id)
        return jsonify(status=200, message="查询成功", data=vlun_level_type_nums)
    except Exception as e:
        logger.exception("vulnerability_count rasie error")
        return jsonify(status=500, message="未知异常", data={"extra_info": "创建任务时出现未知异常，请联系管理员查看异常日志"})


@user_web_api.route('/tasksurlsvulns/count/filter/', methods=['GET'], endpoint='show_task_url_vulnerability_count')
@check_authentication(role=Role.USER)
def show_task_url_vulnerability_count():
    """
    获取n天内的，任务，url，漏洞的数量
    :return: 
    """
    try:
        current_user_name = session.get('user_name')
        current_user = RedisService.get_user(current_user_name)
        day_range = int(request.args.get("day_range"))
        tasks_urls_vulns_num = VulnerabilityService.get_tasks_urls_vulns_num_by_days(user_id=current_user.id,
                                                                                     day_range=day_range)
        return jsonify(status=200, message="查询成功", data=tasks_urls_vulns_num)
    except Exception as e:
        logger.exception("show_task_url_vulnerability_count rasie error")
        if isinstance(e, KeyError):
            return jsonify(status=400, message="查询失败", data={"extra_info": "未传递参数day_range"})
        return jsonify(status=500, message="未知异常", data={"extra_info": "创建任务时出现未知异常，请联系管理员查看异常日志"})


@user_web_api.route('/tasktime/filter/', methods=['GET'], endpoint='show_task_spent_time')
@check_authentication(role=Role.USER)
def show_task_spent_time():
    """
    展示每个任务从创建到结束的时间

    :return: 
    """
    try:
        current_user_name = session.get('user_name')
        current_user = RedisService.get_user(current_user_name)
        count = int(request.args.get("count"))
        tasks = TaskService.get_tasks(user_id=current_user.id)
        tasks = tasks[-count:]
        tasks_json = [
            {"id": task.id, "task_name": task.task_name,
             "created_time": task.created_time.strftime("%Y-%m-%d %H:%M") if task.created_time else "",
             "killed_time": task.killed_time.strftime("%Y-%m-%d %H:%M") if task.killed_time else "",
             "spend_time": minutes_(task.killed_time, task.created_time)} for task in tasks]
        return jsonify(status=200, message="查询成功", data=tasks_json)

    except Exception as e:
        logger.exception("show_task_spent_time rasie error")
        if isinstance(e, KeyError):
            return jsonify(status=400, message="查询失败", reason="请传递参数count")
        return jsonify(status=500, message="未知异常", data={"extra_info": "创建任务时出现未知异常，请联系管理员查看异常日志"})


@user_web_api.route('/user_info/', methods=['GET'], endpoint='get_user_info')
@check_authentication(role=Role.USER)
def get_user_info():
    """
    获取用户信息，从session中获取用户名称，然后通过redis中查询，获取用户权限，根据用户权限来展示不同的页面，可以显示头像之类的
    :return: 
    """
    try:
        current_user_name = session.get("user_name")
        current_user = RedisService.get_user(current_user_name)
        return jsonify(status=200, message="查询成功",
                       data={"full_name": current_user.full_name, "role": current_user.role})
    except Exception as e:
        logger.exception("check_sso raise error")
        return jsonify(status=500, message="未知异常", data={"extra_info": "发生未知异常，请联系管理员查看异常日志"})


@user_web_api.route('/logout/', methods=['GET'], endpoint='logout')
@check_authentication(role=Role.USER)
def logout():
    """
    注销登录，并且跳转到首页需要登录的地方，不能删除redis中的用户信息，因为get_working_task_info要使用
    :return: 
    """
    try:
        session.clear()
        return jsonify(status=200, message="注销成功", data={"site": "/taskmanagement"})
    except Exception:
        logger.exception("logout raise error")
        return jsonify(status=500, message="未知异常", data={"extra_info": "发生未知异常，请联系管理员查看异常日志"})


@user_web_api.route('/task/filter/', methods=['GET'], endpoint='get_working_task_info')
def get_working_task_info():
    """
    根据用户名获取得到任务信息，用于openrestry代理模块取得最新未结束的任务，接口无需鉴权
    :param user_name: 
    :return: 
    """
    try:
        user_name = request.args.get("user_name")
        user = RedisService.get_user(user_name)
        tasks = TaskService.get_working_tasks(user.id)
        descriptions = ["该任务处于激活状态", "该任务正在进行扫描", "该任务已经扫描完成", "该任务已被用户关闭"]
        if tasks is None or len(tasks) == 0:
            return jsonify(status=200, message="查询成功",
                           data={"id": -1, "status": TaskStatus.NONE, "description": "不存在正在工作的任务，请登录平台先创建任务"})
        current_working_task = tasks[0]
        return jsonify(status=200, message="查询成功",
                       data={"id": current_working_task.id, "status": current_working_task.task_status,
                             "description": descriptions[current_working_task.task_status]})

    except Exception as e:
        logger.exception("get_task_info raise error")
        if isinstance(e, KeyError):
            return jsonify(status=400, message="查询失败", data={"extra_info": "未传递参数user_name"})
        elif isinstance(e, UserNotFoundInRedisException):
            return jsonify(status=400, message="查询失败", data={"extra_info": "未找到该用户信息"})
        return jsonify(status=500, message="未知异常", data={"extra_info": "发生未知异常，请联系管理员查看异常日志"})


@user_web_api.route('/notice/', methods=['GET'], endpoint='show_system_notice')
@check_authentication(role=Role.USER)
def show_system_notice():
    """
    显示系统最新通知 
    v2.5.2 新增接口
    :return: 
    """
    try:
        notice_message = SystemConfigService.get_single_instance().notice_message
        return jsonify(status=200, message="查询成功", data=notice_message)
    except Exception as e:
        logger.exception("show_system_notice error")
        return jsonify(status=500, message="未知异常", data={"extra_info": "创建任务时出现未知异常，请联系管理员查看异常日志"})


@user_web_api.route('/client/', methods=['GET'], endpoint='download_client')
@check_authentication(role=Role.USER)
def download_client():
    """
    下载插件
    :return: 
    """
    return send_from_directory(CLIENT_ROOT_PATH, CHROME_CLIENT_NAME, as_attachment=True, cache_timeout=0)
