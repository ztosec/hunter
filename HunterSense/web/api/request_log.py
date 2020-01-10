#!/ usr/bin/env
# coding=utf-8
"""
author: b5mali4
Copyright (c) 2018
"""
from flask import request
from flask import jsonify
from flask import Blueprint
from model.base_model import OrmModelJsonSerializer
from model.request_log import RequestLogService
from model.request_log import RequestLog
from model.system_set import SystemSetting
from model.user import UserService
from model.user import User
from model.system_set import SystemSettingService
from .authentication import check_hunter_token
from .authentication import check_authentication

request_log = Blueprint('requestlog', __name__, url_prefix="/api/v1/")


@request_log.route("requestlogs", methods=['GET'], endpoint='show_requestlogs')
@check_authentication
def show_request_logs():
    """
    请求 GET /api/v1/requestlogs
    显示所有的请求记录
    :return: 
    """
    request_logs = RequestLogService.get_fields_by_where(
        fields=(
            RequestLog.id, RequestLog.ip, RequestLog.port, RequestLog.protocol, RequestLog.time_str, RequestLog.plugin))

    response_data = jsonify(status=200, message="查询成功", data=OrmModelJsonSerializer.serializer(request_logs))
    return response_data


@request_log.route("requestlogs/fieldvalue/", methods=['GET'], endpoint='show_request_logs_field_value')
@check_authentication
def show_request_logs_field_value():
    """
    请求 GET /api/v1/requestlogs/fieldvalue/
    显示所有的记录的类型值去重之后的结果
    :return: 
    """
    """
    plugins = list()
    protocols = list()
    request_log1s = RequestLogService.get_fields_by_where(fields=(RequestLog.plugin.distinct()))
    for request_log in request_log1s:
        plugins.append(request_log.plugin)

    request_log2s = RequestLogService.get_fields_by_where(fields=(RequestLog.protocol.distinct()))
    for request_log in request_log2s:
        protocols.append(request_log.protocol)
    
    response_data = jsonify(status=200, message="查询成功", data={"plugin": plugins, "protocols": protocols})
    """
    response_data = jsonify(status=200, message="查询成功", data=[])
    return response_data


@request_log.route("requestlogs", methods=["DELETE"], endpoint="remove_requestlogs")
@check_authentication
def remove_request_logs():
    """
    请求 DELETE /api/v1/requestlog?id=1
    删除指定的请求记录
    :return: 
    """
    req_json = request.get_json(force=True)
    id_list = [int(idstr) for idstr in req_json.get("id")]
    # IN 语句
    row_nums = RequestLogService.remove(where=(RequestLog.id << id_list))
    message = "成功删除{}条数据".format(row_nums)
    response_data = jsonify(status=200, message=message, data=[])
    return response_data


@request_log.route("hunter/<string:plugin>", methods=["GET"], endpoint="check_hunter_blind")
# @check_hunter_token
def check_hunter_blind(plugin):
    """
    用于给hunter 扫描器调用，探测无回显漏洞，使用token验证身份，plugin由uuid生成
    :return: 
    """
    request_logs = RequestLogService.get_fields_by_where(where=(RequestLog.plugin == plugin))
    if len(request_logs) > 0:
        response_data = jsonify(status=200, message="查找到记录", data=OrmModelJsonSerializer.serializer(request_logs))
    else:
        response_data = jsonify(status=400, message="未查找到记录", data=[])
    RequestLogService.remove(where=(RequestLog.plugin == plugin))
    return response_data
