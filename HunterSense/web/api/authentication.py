#!/ usr/bin/env
# coding=utf-8
"""
author: b5mali4
Copyright (c) 2018
"""
from flask import session, request, jsonify
from model.user import User
from model.user import UserService
from common.system_util import get_tokens


def check_authentication(func):
    """
    检测是否登录成功过，不成功则跳转到登录页面
    :param flask_app: 
    :return: 
    """

    def __check_authentication(*args, **kwargs):
        if "ok" in session and session["ok"]:
            return func(*args, **kwargs)
        else:
            return jsonify(status=403, message="未能授权成功", data={"extra_info": "跳转到登录页面", "site": "/login"})

    return __check_authentication


def check_hunter_token(func):
    """
    检测token
    :param func: 
    :return: 
    """
    def __check_hunter_token(*args, **kwargs):
        header_token = request.headers["token"] if "token" in request.headers else None
        if not header_token:
            return jsonify(status=400, message="请在请求头放入token", data=[])

        for user_token in get_tokens():
            if user_token == header_token:
                return func(*args, **kwargs)
        return jsonify(status=403, message="token错误", data=[])

    return __check_hunter_token
