#!/ usr/bin/env
# coding=utf-8
"""
author: b5mali4
Copyright (c) 2018
"""
from flask import Blueprint
from flask import jsonify
from .authentication import check_authentication
from model.base_model import OrmModelJsonSerializer
from model.request_log_dup import RequestLogDup
from model.request_log_dup import RequestLogDupService

request_log_dup = Blueprint('requestlogdup', __name__)


@request_log_dup.route("/api/v1/requestlogdups", methods=['GET'], endpoint='show_request_log_dups')
@check_authentication
def show_request_log_dups():
    """
    请求 GET /api/v1/requestlogdups
    显示所有的请求记录
    :return: 
    """
    request_logs = RequestLogDupService.get_fields_by_where(
        fields=(RequestLogDup.id, RequestLogDup.port, RequestLogDup.ip, RequestLogDup.protocol, RequestLogDup.time_str,
                RequestLogDup.plugin))

    response_data = jsonify(status=200, message="查询成功", data=OrmModelJsonSerializer.serializer(request_logs))
    return response_data
