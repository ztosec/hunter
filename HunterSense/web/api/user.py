#!/ usr/bin/env
# coding=utf-8
"""
author: b5mali4
Copyright (c) 2018
"""

from flask import Blueprint
from flask import request
from flask import jsonify
from flask import session
from model.base_model import OrmModelJsonSerializer
from model.user import User
from model.user import UserService

user = Blueprint('user', __name__)


@user.route("/api/v1/login", methods=["POST"], endpoint="login")
def login():
    """
    请求如下
    POST /api/v1/user
    
    {"username": "", "password": ""}
    
    登录成功并设置SESSION
    :return: 
    """
    post_data = request.get_json(force=True)
    username = post_data["username"]
    password = post_data["password"]
    count = UserService.count(where=(User.username == username, User.password == password))
    if count > 0:
        session["username"] = username
        session["password"] = password
        session["ok"] = True
        response_data = jsonify(status=200, message="授权成功", data={"extra_info": "跳转到后台", "site": "/"})
    else:
        response_data = jsonify(status=403, message="未能授权成功", data={"extra_info": "跳转到登录页面", "site": "/login"})
    return response_data