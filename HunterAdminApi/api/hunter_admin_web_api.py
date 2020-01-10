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
管理员api
"""
import os

from flask import jsonify, Blueprint, request, send_file
from peewee import *
from plugins.base.vuln_enum import PluginSwith
from api.authentication.auth_module_factory import check_authentication
from api.service.redis_service import RedisService
from common import log
from common.broadcast_value import BroadCastAction, BroadCastType
from common.json_utils import has_dict_value_blank
from common.path import CLIENT_ROOT_PATH, CHROME_CLIENT_NAME
from common.path import PLUGIN_PATH
from common.plugins_util import load_default_checkers
from common.system_util import zip_floder_skip
from exception.hunter_web_exception import BaseHunterException
from exception.hunter_web_service_exception import UsersDataNotExistException
from hunter_celery import system_notice_celery
from model.default_value import Role, TaskStatus
from model.hunter_model import OrmModelJsonSerializer
from model.ldap_config import LdapConfig, LdapConfigService
from model.network_proxy import NetWorkProxyConfig, NetWorkProxyConfigService
from model.plugin_info import PluginInfoService, PluginInfo
from model.system_config import SystemConfig, SystemConfigService
from model.task import Task, TaskService
from model.user import User, UserService
from model.vulnerability import VulnerabilityService
from plugins.base.vuln_enum import VulnLevel

logger = log.getLogger(__name__)
admin_web_api = Blueprint('admin_web_api', __name__, url_prefix="/api/v1/admin/")


@admin_web_api.route('/users/', methods=['GET'], endpoint='list_user')
@check_authentication(role=Role.ADMIN)
def list_users():
    """
    显示用户列表
    一个用户包含 用户名,扫描次数,最新扫描时间,扫描记录 动作包含是否加入管理员等等
    v2.5 可条件查询
    路由请求格式  
        fullname=XX&department=&role= 参数值为''表示所有
        fullname=XX 参数名也表示所有，例如这里表示只查询fullname

    :return: 
    """

    def change_user_dic(user):
        """
        将user转换成DIC
        :param user: 
        :return: 
        """
        # from model.user_task import UserTask, UserTaskService
        # scan_count = UserTaskService.count(where=(UserTask.user_id == user.id))
        recent_operation_time = user.recent_operation_time.strftime(
            "%Y-%m-%d %H:%M") if user.recent_operation_time else ""
        return {"id": user.id, "user_name": user.user_name, "full_name": user.full_name,
                "mobile_phone": user.mobile_phone, "email": user.email, "depart_ment": user.dept_name,
                "role": user.role, "scan_count": user.scan_count, "recent_operation_time": recent_operation_time,
                "user_info": user.user_info}

    def generate_search_query(full_name, depart_ment, role, id):
        result = list()
        if full_name is not None and full_name != "":
            result.append(User.full_name == full_name)
        if depart_ment is not None and depart_ment != "":
            result.append(User.dept_name == depart_ment)
        if role is not None and role != "":
            result.append(User.role == role)
        if id is not None and id != "":
            result.append(User.id == id)
        return result

    try:
        full_name = request.args.get("full_name")
        depart_ment = request.args.get('depart_ment')
        role = request.args.get("role")
        id = request.args.get("id")
        # 构造条件查询元组
        query = generate_search_query(full_name, depart_ment, role, id)
        if len(query) > 0:
            users = [change_user_dic(user) for user in UserService.get_users_scan_count(where=tuple(query))]
        else:
            users = [change_user_dic(user) for user in UserService.get_users_scan_count()]
        return jsonify(status=200, message="查询成功", data=users)
    except Exception as e:
        logger.exception("list_user raise error")
        return jsonify(status=500, message="未知异常", data={"extra_info": "发生未知异常，请联系管理员查看异常日志"})


@admin_web_api.route('/users/<int:user_id>/', methods=['PUT'], endpoint='update_user')
@check_authentication(role=Role.ADMIN)
def modify_user(user_id):
    """
    更新用户资料，主要包含权限，部门等等
    data: {department: "信息安全部", emails: "", mobilephone: "18324742048", role: "管理员"}
    :return: 
    """
    try:
        put_data = request.get_json(force=True)
        param_list = ["email", "mobile_phone", "role", "depart_ment"]
        if has_dict_value_blank(put_data, param_list):
            return jsonify(status=400, message="更新失败", data={"extra_info": "请保证%s任一参数值不为空" % ','.join(param_list)})

        email = put_data.get("email")
        mobile_phone = put_data.get("mobile_phone")
        role = put_data.get("role")
        depart_ment = put_data.get("depart_ment")

        UserService.update(
            fields=({User.email: email, User.mobile_phone: mobile_phone, User.role: role, User.dept_name: depart_ment}),
            where=(User.id == user_id))
        user = UserService.get_fields_by_where(where=(User.id == user_id))[0]
        RedisService.update_user(user.user_name,
                                 {"dept_name": depart_ment, "role": role, "mobile_phone": mobile_phone, "email": email})
        return jsonify(status=200, message="更新用户成功", data={})
    except Exception as e:
        logger.exception("update_user error")
        return jsonify(status=500, message="未知异常", data={"extra_info": "发生未知异常，请联系管理员查看异常日志"})


@admin_web_api.route('/tasks/', methods=['GET'], endpoint='list_tasks')
@check_authentication(role=Role.USER)
def list_tasks():
    """
    显示所有任务列表，方便管理任务
    :return: 
    """
    try:
        task_id = request.args.get("task_id")
        task_status = request.args.get('status')
        # 构造条件查询元组
        task_info_list = list()
        tasks = TaskService.get_tasks_url_num(task_id=task_id, task_status=task_status)
        for task in tasks:
            hook_rule = task.hook_rule
            # RedisService.get_task(task.id)["hook_rule"]
            unscaned_urls_num = task.unscaned_urls_num
            scaned_urls_num = task.scaned_urls_num
            total_url_num = unscaned_urls_num + scaned_urls_num

            if task.task_status in [TaskStatus.KILLED, TaskStatus.DONE]:
                percent = 100
            else:
                percent = 0 if total_url_num == 0 else int((scaned_urls_num / total_url_num) * 100)

            task_info_list.append({'receiver_emails': task.receivers_email, 'task_name': task.task_name,
                                   'create_time': task.created_time.strftime("%Y-%m-%d %H:%M"), 'percent': percent,
                                   'unscaned_url_num': unscaned_urls_num, 'scaned_url_num': scaned_urls_num,
                                   'total_url_num': total_url_num, 'hook_rule': hook_rule, 'task_id': task.id,
                                   'task_access_key': task.access_key, 'task_status': task.task_status,
                                   "create_user_name": task.create_user_name})
        task_info_list.reverse()
        response = jsonify(status=200, message="查询成功", data=task_info_list)
        return response

    except Exception as e:
        logger.exception("show_current_tasks rasie error")
        if isinstance(e, BaseHunterException):
            return jsonify(status=400, message=str(e), data={"extra_info": "查询任务时传入非法的task_id"})
        return jsonify(status=500, message="未知异常", data={"extra_info": "查询任务时出现未知异常，请联系管理员查看异常日志"})


@admin_web_api.route('/tasks/', methods=['DELETE'], endpoint='stop_task')
@check_authentication(role=Role.ADMIN)
def stop_task():
    """
    关闭任务，关闭任务之后将用户任务信息进行持久化到数据库，包括结束任务时间
    :return: 
    """
    post_data = request.get_json(force=True)
    if has_dict_value_blank(post_data, ["task_id"]):
        return jsonify(status=400, message="结束任务失败", data={"extra_info": "task_id缺失,无法结束任务"})
    try:
        post_task_id = int(post_data.get("task_id"))
        TaskService.update(fields=({Task.task_status: TaskStatus.KILLED}), where=(Task.id == post_task_id))
        RedisService.stop_task(post_task_id)
        RedisService.clean_urlclassifications(post_task_id)
        return jsonify(status=200, message="结束任务成功",
                       data={"extra_info": "该任务由管理员关闭"})
    except Exception as e:
        logger.exception("stop_task exception")
        return jsonify(status=500, message="未知异常", data={"extra_info": "创建任务时出现未知异常，请联系管理员查看异常日志"})


@admin_web_api.route('/plugins/', methods=['GET'], endpoint='list_plugins')
@check_authentication(role=Role.USER)
def list_plugins():
    """
    显示所有插件信息，从数据库加载信息，只做展示使用
    :return: 

    """
    try:
        checker_info_list = list()
        middle_num = 0
        hight_num = 0
        low_num = 0
        plugin_infos = PluginInfoService.get_fields_by_where()

        for plugin_info in plugin_infos:
            checker_info_list.append(
                {"name": plugin_info.plugin_name, "tag": plugin_info.plugin_tag, "imp_version": plugin_info.imp_version,
                 "type": plugin_info.chinese_type, "level": plugin_info.level, "description": plugin_info.description,
                 "useable": plugin_info.useable})

            if plugin_info.level == VulnLevel.HIGHT:
                hight_num += 1

            if plugin_info.level == VulnLevel.MIDDLE:
                middle_num += 1

            if plugin_info.level == VulnLevel.LOW:
                low_num += 1

        response = jsonify(status=200, message="查询成功",
                           data={"checker_info_list": checker_info_list, "hight_num": hight_num,
                                 "middle_num": middle_num, "low_num": low_num})
        return response
    except Exception:
        logger.exception("show_current_tasks rasie error")
        return jsonify(status=500, message="未知异常", data={"extra_info": "加载插件时出现未知异常，请联系管理员查看异常日志"})


@admin_web_api.route('/plugins/', methods=['POST'], endpoint='insert_plugin')
@check_authentication(role=Role.ADMIN)
def insert_plugin():
    """
    新增插件，
    服务端:1.保存插件到本地，先上传到tmp目录，然后解析插件是否满足格式出tag并移动到tag目录，刷新插件列表 2.向MQ发送一条消息包含插件
    引擎端:2.消费到MQ发送消息，并下载最新插件并新增到CHECKER_INSTANCE_DICT
    :return: 
    """
    import shutil
    from common.system_util import mkdir
    from common.path import PLUGIN_PATH
    from common.plugins_util import load_default_checkers

    def allowed_file(filename):
        """
        检测是否为python文件
        :param filename: 
        :return: 
        """
        return '.' in filename and filename.rsplit('.', 1)[1] in ["py"]

    def parse_plugin_file(plugin_file_path):
        """
        warnning: 插件文件路径，这里会存在安全隐患，请按照实际需求考虑是否用imp.load_source
        :param plugin_file_path: 
        :return: 
        """
        import imp
        from exception.hunter_web_exception import BaseHunterException

        # 解析插件并且分类
        base_checker = imp.load_source('BaseChecker', plugin_file_path)
        checker_instance = base_checker.Checker()
        checker_instance.check_plugin_info()
        # 检测插件是否重名
        checker_name = checker_instance.info["name"]
        if checker_name in load_default_checkers():
            raise BaseHunterException("插件%s已经存在，请重新命名" % checker_name)
        return checker_instance

    def move_plugin(tmp_plugin_file_path, checker_instance, filename):
        """
        :param checker_instance: 
        :return: 
        """
        # 移动插件到指定目录
        tag = checker_instance.info["tag"]
        mkdir(PLUGIN_PATH + tag)
        formal_plugin_file_path = os.path.join(PLUGIN_PATH + tag, filename)
        shutil.move(tmp_plugin_file_path, formal_plugin_file_path)

    def save_plugin_info(checker_instance):
        if PluginInfoService.count(where=(PluginInfo.plugin_name == checker_instance.info["name"])) == 0:
            PluginInfoService.save(author=checker_instance.info["author"], plugin_name=checker_instance.info["name"],
                                   plugin_tag=checker_instance.info["tag"],
                                   imp_version=checker_instance.info["imp_version"],
                                   description=checker_instance.info["description"],
                                   repair=checker_instance.info["repair"],
                                   type=checker_instance.info["type"]["fullname"],
                                   chinese_type=checker_instance.info["type"]["fullchinesename"],
                                   level=checker_instance.info["type"]["level"], )

    try:
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = file.filename
            tmp_plugin_file_path = os.path.join(PLUGIN_PATH + "tmp/", filename)
            file.save(tmp_plugin_file_path)
            # 解析插件
            checker_instance = parse_plugin_file(tmp_plugin_file_path)
            move_plugin(tmp_plugin_file_path, checker_instance, filename)
            # 保存到数据
            save_plugin_info(checker_instance)
            load_default_checkers(True)
            RedisService.modify_plugin_switch(checker_instance, PluginSwith.ON)
            system_notice_celery.delay(broadcast={"type": BroadCastType.PLUGIN, "action": BroadCastAction.INSERT_PLUGIN,
                                                  "data": {"name": checker_instance.info["name"]}})
            return jsonify(status=200, message="上传成功", data={"extra_info": "您可以刷新网页后使用新插件"})
        return jsonify(status=500, message="上传失败", data={"extra_info": "您上传的插件不是py文件"})
    except Exception as e:
        logger.exception("create_plugin raise error")
        # 解析插件是否满足格式
        return jsonify(status=500, message="上传失败", data={"extra_info": str(e)})


@admin_web_api.route('/plugins/', methods=['DELETE'], endpoint='delete_plugin')
@check_authentication(role=Role.ADMIN)
def delete_plugin():
    """
    删除指定的插件
    :return: 
    """
    return jsonify(status=500, message="删除失败", data={"extra_info": "暂不支持删除功能,可使用禁用插件"})


@admin_web_api.route('/plugins/', methods=['PUT'], endpoint='modify_plugin')
@check_authentication(role=Role.ADMIN)
def modify_plugin():
    """
    禁用指定的插件，
    服务端:1.从CHECKER_INSTANCE_DICT指定插件设置disable 2.并向MQ中发送一条消息
    引擎端:1.等到引擎消费到指令从CHECKER_INSTANCE_DICT，也将该插件的disable设置为True
    :return: 
    """
    from plugins.base.vuln_enum import PluginSwith
    from common.plugins_util import modify_default_checkers
    post_data = request.get_json(force=True)
    param_list = ["name", "switch"]
    if has_dict_value_blank(post_data, param_list):
        return jsonify(status=400, message="更新失败", data={"extra_info": "请保证%s任一参数值不为空" % ','.join(param_list)})
    try:
        post_checker_name = post_data.get("name")
        post_switch = post_data.get("switch")
        plugin_switch = PluginSwith.ON if post_switch else PluginSwith.OFF
        checkers = load_default_checkers()
        if post_checker_name not in checkers:
            return jsonify(status=400, message="更新失败", data={"extra_info": "不存在名为%s的插件" % post_checker_name})

        PluginInfoService.update(fields=({PluginInfo.useable: plugin_switch}), where=(PluginInfo.plugin_name == post_checker_name))

        RedisService.modify_plugin_switch(checkers[post_checker_name], plugin_switch)

        system_notice_celery.delay(broadcast={"type": BroadCastType.PLUGIN, "action": BroadCastAction.MODIFY_PLUGIN,
                                              "data": {"name": post_checker_name,
                                                       "switch": plugin_switch}})
        modify_default_checkers()
        return jsonify(status=200, message="更新成功",
                       data={"extra_info": "{}插件{}".format("启用" if plugin_switch else "禁用", post_checker_name)})
    except Exception as e:
        logger.exception("modify_plugin raise error")
        return jsonify(status=500, message="未知异常", data={"extra_info": "修改插件信息时出现未知异常，请联系管理员查看异常日志"})


@admin_web_api.route('/checkers/', methods=['GET'], endpoint='download_checkers')
def download_checkers():
    """
    下载所有的插件，不做鉴权
    :return: 
    """
    checker_name = request.args.get("name")

    if not checker_name:
        zip_floder_skip(target_file="%stmp/plugins.zip" % PLUGIN_PATH, origin_folder=PLUGIN_PATH, is_regular=True,
                        skip_list=["*DS_Store", "*__pycache__*", "tmp/*"])
        return send_file(filename_or_fp="%stmp/plugins.zip" % PLUGIN_PATH, as_attachment=True, cache_timeout=0)

    checkers = load_default_checkers()
    if checker_name not in checkers:
        return jsonify(status=400, message="下载失败", data={"extra_info": "不存在名字为%s的插件" % checker_name})

    return send_file(filename_or_fp=checkers[checker_name].plugin_file_path, as_attachment=True, cache_timeout=0)


@admin_web_api.route('/task/', methods=['PUT'], endpoint='update_task')
@check_authentication(role=Role.ADMIN)
def update_task():
    """
    更新任务信息，最主要的是修改hook_url
    :return: 
    """
    try:
        put_data = request.get_json(force=True)
        if has_dict_value_blank(put_data, ["hook_rule", "task_id"]):
            return jsonify(status=400, message="更新任务失败", data={"extra_info": "请确认是否正确传入hook_rule,task_id参数"})
        hook_rule = put_data.get("hook_rule")
        task_id = put_data.get("task_id")
        # Task表修改一下hook_rule
        TaskService.update(fields=({Task.hook_rule: hook_rule}), where=(Task.id == task_id))
        # redis更改任务hook_rule
        RedisService.update_task_hook_rule(task_id, hook_rule)
        return jsonify(status=200, message="更新任务成功", data={"extra_info": "修改成功,该任务由管理员修改"})
    except Exception as e:
        logger.exception("update_task exception")
        return jsonify(status=500, message="未知异常", data={"extra_info": "创建任务时出现未知异常，请联系管理员查看异常日志"})


@admin_web_api.route('/scan_record/filter/', methods=['GET'], endpoint='list_scan_record')
@check_authentication(role=Role.ADMIN)
def list_scan_record():
    """
    根据task_id查询扫描记录
    :return: 
    """
    try:
        user_id = request.args.get("user_id")
        tasks = TaskService.get_tasks_url_vuln_num(user_id=user_id)
        response_data = list()

        for task in tasks:
            risk_level = VulnerabilityService.get_risk_level(task)
            response_data.append(
                {"task_name": task.task_name, "created_time": task.created_time.strftime("%Y-%m-%d %H:%M"),
                 "task_id": task.id, "urls_num": task.urls_num, "vulns_num": task.vulns_num, "risk_level": risk_level})

        response_data.reverse()

        return jsonify(status=200, message="查询成功", data=response_data)
    except Exception as e:
        logger.exception("list_scan_record raise error")
        if isinstance(e, KeyError):
            return jsonify(status=400, message="查询失败", data={"extra_info": "未传递taskid"})
        return jsonify(status=500, message="未知异常", data={"extra_info": "发生未知异常，请联系管理员查看异常日志"})


@admin_web_api.route('/vulnerability/details/filter/', methods=['GET'], endpoint='show_vulnerability_details')
@check_authentication(role=Role.ADMIN)
def show_vulnerability_details():
    """
    v2.2 修复 越权
    根据task_id获取一次详细的任务结果，此处存在越权，可以查看其他人的漏洞详情
    所有权限判断的地方都需要去
    :return: 
    """
    try:
        task_id = request.args.get("task_id")
        return jsonify(status=200, message="查询成功", vlun=VulnerabilityService.get_vulnerabilitys_nltdr(task_id))
    except Exception as e:
        logger.exception("show_vulnerability_details error")
        if isinstance(e, KeyError):
            return jsonify(status=400, message="查询失败", data={"extra_info": "未传递taskid"})
        return jsonify(status=500, message="未知异常", data={"extra_info": "发生未知异常，请联系管理员查看异常日志"})


@admin_web_api.route('/vulnerabilitys/', methods=['GET'], endpoint='list_vulnerabilitys')
@check_authentication(role=Role.ADMIN)
def list_vulnerabilitys():
    """
    显示所有漏洞
    :return: 
    """
    try:
        vulns = list()
        for vuln in VulnerabilityService.get_fields_by_where():
            vulns.append({'id': vuln.id, 'url_id': vuln.url_id, 'task_id': vuln.task_id, 'info': vuln.info,
                          'type': vuln.chinese_type, 'level': vuln.level})

        vulns.reverse()
        return jsonify(status=200, message="查询成功", data=vulns)
    except Exception as e:
        logger.exception("list_vulnerabilitys raise error")
        if isinstance(e, KeyError):
            return jsonify(status=400, message="查询失败", data={"extra_info": "参数未传递taskid"})
        return jsonify(status=500, message="未知异常", data={"extra_info": "发生未知异常，请联系管理员查看异常日志"})


@admin_web_api.route('/user/<string:openid>', methods=['PUT'], endpoint='update_user_role')
@check_authentication(role=Role.ADMIN)
def update_user_role(openid):
    """
    更改用户权限
    :return: 
    """
    put_data = request.get_json(force=True)
    role = put_data.get("role")
    if role == Role.ADMIN or role == Role.USER:
        UserService.update_role(openid, role)
        return jsonify(status=200, message="更新权限成功", data={})
    else:
        return jsonify(status=400, message="更新权限失败", data={"extra_info": "role不合法"})


@admin_web_api.route('/vulnstatistics/count/', methods=['GET'], endpoint='list_vulnerability_count')
@check_authentication(role=Role.ADMIN)
def list_vulnerability_count():
    """
    获取所有用户所有扫描的记录的漏洞数量集合，按照type和level分类
    :return: 
    """
    try:
        vlun_nums = VulnerabilityService.get_vulnerability_count()
        return jsonify(status=200, message="查询成功", data=vlun_nums)
    except Exception as e:
        return jsonify(status=200, message="查询成功", data=[])


@admin_web_api.route('/tasksurlsvulns/count/filter/', methods=['GET'], endpoint='list_task_url_vulnerability_count')
@check_authentication(role=Role.ADMIN)
def list_task_url_vulnerability_count():
    """
    获取n天内，任务,url,漏洞数量
    :return: 
    """
    try:
        days = int(request.args.get("days"))
        tasks_urls_vulns_num = VulnerabilityService.get_tasks_urls_vulns_num_by_days(day_range=days)
        return jsonify(status=200, message="查询成功", data=tasks_urls_vulns_num)
    except KeyError as e:
        logger.exception("list_task_url_vulnerability_count raise error")
        if isinstance(e, KeyError):
            return jsonify(status=400, message="查询失败", reason="请传递参数days")
        return jsonify(status=500, message="未知异常", data={"extra_info": "发生未知异常，请联系管理员查看异常日志"})


@admin_web_api.route('/tasktime/filter/', methods=['GET'], endpoint='list_task_spent_time')
@check_authentication(role=Role.ADMIN)
def list_task_spent_time():
    """
    列出最近n次任务扫描消耗的时间，用于数据大盘第四个图
    :return: 
    """
    from common.system_util import minutes_
    try:
        count = int(request.args.get("count"))
        response_data = list()
        tasks = TaskService.get_fields_by_where(fields=(Task.id, Task.task_name, Task.created_time, Task.killed_time))[
                -count:]
        for task in tasks:
            created_time = task.created_time.strftime("%Y-%m-%d %H:%M") if task.created_time else ""
            killed_time = task.killed_time.strftime("%Y-%m-%d %H:%M") if task.killed_time else ""
            response_data.append(
                {"id": task.id, "task_name": task.task_name, "created_time": created_time, "killed_time": killed_time,
                 "spend_time": minutes_(task.killed_time, task.created_time)})
        return jsonify(status=200, message="查询成功", data=response_data)
    except Exception as e:
        logger.exception("list_task_spent_time raise error")
        if isinstance(e, KeyError):
            return jsonify(status=400, message="查询失败", data={"extra_info": "请传递参数count"})
        return jsonify(status=500, message="未知异常", data={"extra_info": "发生未知异常，请联系管理员查看异常日志"})


@admin_web_api.route('/user/', methods=['GET'], endpoint='list_users')
@check_authentication(role=Role.ADMIN)
def list_users():
    """
    获取系统中的用户列表
    :return: 
    """
    user_list = []
    try:
        users = UserService.get_fields_by_where()
        user_list.reverse()
        response_data = jsonify(status=200, message="查询成功", data={'users': user_list, 'num': len(users)})
    except UsersDataNotExistException:
        logger.exception("list_users raise error")
        response_data = jsonify(status=200, message="查询成功", data={'users': user_list, 'num': 0})

    return response_data


@admin_web_api.route('/tasks/', methods=['GET'], endpoint='list_tasks_by_num')
@check_authentication(role=Role.ADMIN)
def list_tasks_by_num():
    """
    获取系统中的任务列表，用于数据大盘展示用户使用最新动态，需要跨表连接获取数据
    SELECT * FROM user INNER JOIN usertask ON usertask.user_id = user.id where usertask.task_id = 2333
    :return: 
    """
    try:
        num = int(request.args.get("num"))
        tasks_cursor_wrapper = TaskService.get_fields_by_where(
            fields=(Task.created_time, Task.killed_time, Task.task_name, Task.id))
        tasks_list = OrmModelJsonSerializer.serializer(tasks_cursor_wrapper)
        tasks_list.reverse()
        if len(tasks_list) > num:
            tasks_result = tasks_list[0:num]
        else:
            tasks_result = tasks_list
        result = list()
        for task_result in tasks_result:
            user = UserService.get_users(task_id=task_result["id"])[0]
            task_result["dept_name"] = user.dept_name
            task_result["full_name"] = user.full_name
            task_result["user_name"] = user.user_name
            result.append(task_result)

        response_data = jsonify(status=200, message="查询成功",
                                data={'tasks': result, 'num': len(result)})
    except Exception as e:
        logger.exception("list_tasks raise error")
        return jsonify(status=200, message="查询成功", data={'tasks': [], 'num': 0})

    return response_data


@admin_web_api.route('/setting/base/', methods=['PUT'], endpoint='modify_base_config')
@check_authentication(role=Role.ADMIN)
def modify_base_config():
    """
    修改设置，包含黑白名单，系统通知等
    :return: 
    """
    try:
        put_data = request.get_json(force=True)
        notice_message = put_data.get("notice_message")
        white_ips = put_data.get("white_ips")
        if str(notice_message).strip() == "" or str(white_ips).strip() == "":
            return jsonify(status=400, message="更新失败", data={"extra_info": "请确保notice_message,white_ips三个参数不能为空"})
        else:
            SystemConfigService.update(fields=({SystemConfig.notice_message: notice_message}))
            return jsonify(status=200, message="更新成功", data={})
    except Exception as e:
        logger.exception("modify_base_setting raise error")
        if isinstance(e, KeyError):
            return jsonify(status=400, message="查询失败", data={"extra_info": "请确保notice_message,white_ips三个参数不能为空"})
        return jsonify(status=500, message="未知异常", data={"extra_info": "发生未知异常，请联系管理员查看异常日志"})


@admin_web_api.route('/setting/base/', methods=['GET'], endpoint='list_base_config')
@check_authentication(role=Role.ADMIN)
def list_base_config():
    """
    显示基本设置，包含黑白名单，系统通知等
    :return: 
    
    """
    try:
        system_config = SystemConfigService.get_single_instance()
        return jsonify(status=200, message="查询成功", data={'notice_message': system_config.notice_message,
                                                         "socket_log_host": system_config.hunter_log_socket_host})
    except Exception:
        logger.exception("list_base_setting raise error")
        return jsonify(status=500, message="未知异常", data={"extra_info": "发生未知异常，请联系管理员查看异常日志"})


@admin_web_api.route('/setting/email/', methods=['PUT'], endpoint='modify_email_config')
@check_authentication(role=Role.ADMIN)
def modify_email_config():
    """
    修改发件邮箱基本信息
    :return: 
    """
    try:
        put_data = request.get_json(force=True)
        param_list = ["smtp_host", "smtp_port", "sender_email", "sender_password"]
        if has_dict_value_blank(put_data, param_list):
            return jsonify(status=400, message="更新失败", data={"extra_info": "请保证%s任一参数值不为空" % ','.join(param_list)})

        smtp_host = put_data.get("smtp_host")
        smtp_port = put_data.get("smtp_port")
        sender_email = put_data.get("sender_email")
        sender_password = put_data.get("sender_password")
        email_content_template = put_data.get("content_template")
        SystemConfigService.update(fields=({SystemConfig.smtp_host: smtp_host, SystemConfig.smtp_port: smtp_port,
                                            SystemConfig.sender_email: sender_email,
                                            SystemConfig.sender_password: sender_password,
                                            SystemConfig.email_content_template: email_content_template}))
        return jsonify(status=200, message="更新成功", data={})
    except Exception as e:
        logger.exception("modify_email_setting raise error")
        if isinstance(e, KeyError):
            return jsonify(status=400, message="更新失败", data={
                "extra_info": "请确保传递参数smtp_host,smtp_port,sender_email,sender_password"})
        return jsonify(status=500, message="未知异常", data={"extra_info": "发生未知异常，请联系管理员查看异常日志"})


@admin_web_api.route('/setting/email/', methods=['GET'], endpoint='list_email_config')
@check_authentication(role=Role.ADMIN)
def list_email_config():
    """
    显示邮箱设置信息
    :return: 
    """
    try:
        system_config = SystemConfigService.get_single_instance()
        response_data = {"sender_email": system_config.sender_email, "sender_password": system_config.sender_password,
                         "smtp_host": system_config.smtp_host, "smtp_port": system_config.smtp_port,
                         "content_template": system_config.email_content_template}
        return jsonify(status=200, message="查询成功", data=response_data)
    except Exception:
        logger.exception("list_email_setting raise error")
        return jsonify(status=500, message="未知异常", data={"extra_info": "发生未知异常，请联系管理员查看异常日志"})


@admin_web_api.route('/setting/hunter_log/socket/', methods=['PUT'], endpoint='modify_hunter_socket_log_config')
@check_authentication(role=Role.ADMIN)
def modify_hunter_socket_log_config():
    """
    修改hunter Log Socket模块信息
    :return: 
    
    
    """
    try:
        put_data = request.get_json(force=True)
        param_list = ["hunter_log_socket_host", "hunter_log_socket_port", "hunter_log_socket_switch"]
        if has_dict_value_blank(put_data, param_list):
            return jsonify(status=400, message="更新失败", data={"extra_info": "请保证%s任一参数值不为空" % ','.join(param_list)})
        hunter_log_socket_host = put_data.get("hunter_log_socket_host")
        hunter_log_socket_port = put_data.get("hunter_log_socket_port")
        hunter_log_socket_switch = put_data.get("hunter_log_socket_switch")
        SystemConfigService.update(fields=({SystemConfig.hunter_log_socket_host: hunter_log_socket_host,
                                            SystemConfig.hunter_log_socket_port: hunter_log_socket_port,
                                            SystemConfig.hunter_log_socket_switch: hunter_log_socket_switch}))
        return jsonify(status=200, message="更新成功", data={})
    except Exception as e:
        logger.exception("modify_hunter_log_socket raise error")
        return jsonify(status=500, message="未知异常", data={"extra_info": "发生未知异常，请联系管理员查看异常日志"})


@admin_web_api.route('/setting/hunter_log/socket/', methods=['GET'], endpoint='list_hunter_socket_log_config')
@check_authentication(role=Role.ADMIN)
def list_hunter_socket_log_config():
    """
    显示hunterlog socket模块的基本配置信息
    :return: 
    """
    try:
        system_config = SystemConfigService.get_single_instance()
        response_data = {"hunter_log_socket_host": system_config.hunter_log_socket_host,
                         "hunter_log_socket_port": system_config.hunter_log_socket_port,
                         "hunter_log_socket_switch": system_config.hunter_log_socket_switch}
        return jsonify(status=200, message="查询成功", data=response_data)
    except Exception:
        logger.exception("list_hunter_log_socket raise error")
        return jsonify(status=500, message="未知异常", data={"extra_info": "发生未知异常，请联系管理员查看异常日志"})


@admin_web_api.route('/setting/hunter_log/dns/', methods=['PUT'], endpoint='modify_hunter_dns_log_config')
@check_authentication(role=Role.ADMIN)
def modify_hunter_dns_log_config():
    """
    修改hunter Log Socket模块信息
    :return: 
    """
    try:
        put_data = request.get_json(force=True)
        param_list = ["hunter_log_dns_fake_root_domain", "hunter_log_dns_switch", "hunter_api_url"]
        if has_dict_value_blank(put_data, param_list):
            return jsonify(status=400, message="更新失败", data={"extra_info": "请保证%s任一参数值不为空" % ','.join(param_list)})
        hunter_log_dns_fake_root_domain = put_data.get("hunter_log_dns_fake_root_domain")
        hunter_log_dns_switch = put_data.get("hunter_log_dns_switch")
        hunter_api_url = put_data.get("hunter_api_url")
        SystemConfigService.update(fields=(
        {SystemConfig.hunter_log_dns_fake_root_domain: hunter_log_dns_fake_root_domain,
         SystemConfig.hunter_log_dns_switch: hunter_log_dns_switch, SystemConfig.hunter_api_url: hunter_api_url}))
        return jsonify(status=200, message="更新成功,开启开关之前一定要确认dnslog功能正常使用,否则将会跳过socketlog回显检测逻辑,导致插件漏报", data={})
    except Exception as e:
        logger.exception("modify_hunter_log_dns raise error")
        return jsonify(status=500, message="未知异常", data={"extra_info": "发生未知异常，请联系管理员查看异常日志"})


@admin_web_api.route('/setting/hunter_log/dns/', methods=['GET'], endpoint='list_hunter_dns_log_config')
@check_authentication(role=Role.ADMIN)
def list_hunter_dns_log_config():
    """
    显示hunterlog dns模块和hunter_api_url地址
    :return: 
    """
    try:
        system_config = SystemConfigService.get_single_instance()
        response_data = {"hunter_log_dns_fake_root_domain": system_config.hunter_log_dns_fake_root_domain,
                         "hunter_log_dns_switch": system_config.hunter_log_dns_switch,
                         "hunter_api_url": system_config.hunter_api_url}
        return jsonify(status=200, message="查询成功", data=response_data)
    except Exception:
        logger.exception("list_hunter_log_dns raise error")
        return jsonify(status=500, message="未知异常", data={"extra_info": "发生未知异常，请联系管理员查看异常日志"})


@admin_web_api.route('/setting/ldap/', methods=['PUT'], endpoint='modify_ldap_config')
@check_authentication(role=Role.ADMIN)
def modify_ldap_config():
    """
    修改ldap模块信息
    :return: 
    """
    try:
        put_data = request.get_json(force=True)

        ldap_host = put_data.get("ldap_host")
        bind_dn = put_data.get("ldap_bind_dn")
        bind_dn_password = put_data.get("ldap_bind_dn_password")
        base_dn = put_data.get("ldap_base_dn")
        search_filter = put_data.get("ldap_search_filter")
        user_name_field = put_data.get("ldap_user_name_field")
        full_name_field = put_data.get("ldap_full_name_field")
        email_field = put_data.get("ldap_email_field")
        dept_name_field = put_data.get("ldap_dept_name_field")
        ldap_mobile_field = put_data.get("ldap_mobile_field")
        ldap_switch = put_data.get("ldap_switch")

        if LdapConfigService.count() == 0:
            LdapConfigService.save(ldap_host=ldap_host, bind_dn=bind_dn, bind_dn_password=bind_dn_password,
                                   base_dn=base_dn,
                                   search_filter=search_filter, user_name_field=user_name_field,
                                   full_name_field=full_name_field, email_field=email_field,
                                   dept_name_field=dept_name_field,
                                   ldap_switch=ldap_switch, ldap_mobile_field=ldap_mobile_field)

        LdapConfigService.update(
            fields=({LdapConfig.ldap_host: ldap_host, LdapConfig.bind_dn: bind_dn,
                     LdapConfig.bind_dn_password: bind_dn_password,
                     LdapConfig.base_dn: base_dn, LdapConfig.search_filter: search_filter,
                     LdapConfig.user_name_field: user_name_field, LdapConfig.full_name_field: full_name_field,
                     LdapConfig.email_field: email_field, LdapConfig.dept_name_field: dept_name_field,
                     LdapConfig.ldap_switch: ldap_switch, LdapConfig.mobile_field: ldap_mobile_field}))
        return jsonify(status=200, message="更新成功", data={})
    except Exception as e:
        logger.exception("modify_ldap_setting raise error")
        return jsonify(status=500, message="未知异常", data={"extra_info": "发生未知异常，请联系管理员查看异常日志"})


@admin_web_api.route('/setting/ldap/', methods=['GET'], endpoint='list_ldap_config')
@check_authentication(role=Role.ADMIN)
def list_ldap_config():
    """
    显示ldap配置信息
    :return: 
    """
    try:
        ldap_config = LdapConfigService.get_single_instance()
        response_data = {"ldap_host": ldap_config.ldap_host, "ldap_bind_dn": ldap_config.bind_dn,
                         "ldap_bind_dn_password": ldap_config.bind_dn_password, "ldap_base_dn": ldap_config.base_dn,
                         "ldap_search_filter": ldap_config.search_filter,
                         "ldap_user_name_field": ldap_config.user_name_field,
                         "ldap_full_name_field": ldap_config.full_name_field,
                         "ldap_email_field": ldap_config.email_field,
                         "ldap_dept_name_field": ldap_config.dept_name_field, "ldap_switch": ldap_config.ldap_switch,
                         "ldap_mobile_field": ldap_config.mobile_field}
        return jsonify(status=200, message="查询成功", data=response_data)
    except Exception as e:
        logger.exception("list_ldap_setting raise error")
        if isinstance(e, IndexError):
            return jsonify(status=200, message="查询成功", data={})
        return jsonify(status=500, message="未知异常", data={"extra_info": "发生未知异常，请联系管理员查看异常日志"})


@admin_web_api.route('/setting/proxy/', methods=['GET'], endpoint='list_proxy_config')
@check_authentication(role=Role.ADMIN)
def list_proxy_config():
    """
    显示ldap配置信息
    :return: 
    """
    try:
        proxy_config_single = NetWorkProxyConfigService.get_single_instance()
        response_data = {"ca_country_name": proxy_config_single.ca_country_name,
                         "ca_province": proxy_config_single.ca_province,
                         "ca_locality_name": proxy_config_single.ca_locality_name,
                         "ca_organization_name": proxy_config_single.ca_organization_name,
                         "ca_organizational_unit_name": proxy_config_single.ca_organizational_unit_name,
                         "ca_common_name": proxy_config_single.ca_common_name,
                         "white_host_list": proxy_config_single.white_host_list,
                         "ldap_auth_switch": proxy_config_single.ldap_auth_switch,
                         "account_auth_switch": proxy_config_single.account_auth_switch}
        return jsonify(status=200, message="查询成功", data=response_data)
    except Exception as e:
        logger.exception("list_ldap_setting raise error")
        if isinstance(e, IndexError):
            return jsonify(status=200, message="查询成功", data={})
        return jsonify(status=500, message="未知异常", data={"extra_info": "发生未知异常，请联系管理员查看异常日志"})


@admin_web_api.route('/setting/proxy/', methods=['PUT'], endpoint='modify_proxy_config')
@check_authentication(role=Role.ADMIN)
def modify_proxy_config():
    """
    修改ldap模块信息
    :return: 
    """
    try:
        put_data = request.get_json(force=True)

        ca_country_name = put_data.get("ca_country_name")
        ca_province = put_data.get("ca_province")
        ca_locality_name = put_data.get("ca_locality_name")
        ca_organization_name = put_data.get("ca_organization_name")
        ca_organizational_unit_name = put_data.get("ca_organizational_unit_name")
        ca_common_name = put_data.get("ca_common_name")
        white_host_list = put_data.get("white_host_list")
        ldap_auth_switch = put_data.get("ldap_auth_switch")
        account_auth_switch = put_data.get("account_auth_switch")

        if NetWorkProxyConfigService.count() == 0:
            NetWorkProxyConfigService.save(ca_country_name=ca_country_name, ca_province=ca_province,
                                           ca_locality_name=ca_locality_name, ca_organization_name=ca_organization_name,
                                           ca_organizational_unit_name=ca_organizational_unit_name,
                                           ca_common_name=ca_common_name, white_host_list=white_host_list,
                                           ldap_auth_switch=ldap_auth_switch, account_auth_switch=account_auth_switch)

        NetWorkProxyConfigService.update(
            fields=({NetWorkProxyConfig.ca_country_name: ca_country_name, NetWorkProxyConfig.ca_province: ca_province,
                     NetWorkProxyConfig.ca_locality_name: ca_locality_name,
                     NetWorkProxyConfig.ca_organization_name: ca_organization_name,
                     NetWorkProxyConfig.ca_organizational_unit_name: ca_organizational_unit_name,
                     NetWorkProxyConfig.ca_common_name: ca_common_name,
                     NetWorkProxyConfig.white_host_list: white_host_list,
                     NetWorkProxyConfig.ldap_auth_switch: ldap_auth_switch,
                     NetWorkProxyConfig.account_auth_switch: account_auth_switch}))
        return jsonify(status=200, message="更新成功", data={})
    except Exception as e:
        logger.exception("modify_ldap_setting raise error")
        return jsonify(status=500, message="未知异常", data={"extra_info": "发生未知异常，请联系管理员查看异常日志"})


@admin_web_api.route('/client/', methods=['POST'], endpoint='upload_client')
@check_authentication(role=Role.ADMIN)
def upload_client():
    """
    上传客户端到服务器，暂时只支持chrome浏览器插件，网络代理，火狐浏览器
    """

    def allowed_file(filename):
        """
        检测是否为python文件
        :param filename: 
        :return: 
        """
        return '.' in filename and filename.rsplit('.', 1)[1] in ["zip"]

    try:
        file = request.files['file']
        if file and allowed_file(file.filename):
            chrome_client_path = os.path.join(CLIENT_ROOT_PATH, CHROME_CLIENT_NAME)
            file.save(chrome_client_path)
            return jsonify(status=200, message="上传成功", data={"extra_info": "用户可以刷新网页后在用户下载处下载新客户端"})
        return jsonify(status=500, message="上传失败", data={"extra_info": "您上传的插件不是py文件"})
    except Exception as e:
        logger.exception("create_plugin raise error")
        # 解析插件是否满足格式
        return jsonify(status=500, message="上传失败", data={"extra_info": str(e)})
