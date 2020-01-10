#!/ usr/bin/env
# coding=utf-8
"""
author: b5mali4
Copyright (c) 2018
"""

from flask import Blueprint
from flask import request
from flask import jsonify
from model.base_model import OrmModelJsonSerializer
from model.user import User
from model.user import UserService
from .authentication import check_authentication
from model.system_set import SystemSetting
from model.system_set import SystemSettingService
from resolver.socket_server import TcpServer
from resolver.dns_server import DnsServer
from multiprocessing import Process

system_set = Blueprint('system_set', __name__)


@system_set.route("/api/v1/system_set/dns", methods=["GET"], endpoint="show_dns_server_system_set")
@check_authentication
def show_dns_server_system_set():
    """
    显示DNS服务设置
    请求如下
    
    GET /api/v1/system_set/dns
    :return: 
    """
    system_setting = SystemSettingService.get_fields_by_where(fields=(
        SystemSetting.dns_switch, SystemSetting.fake_root_domain, SystemSetting.ns1domain, SystemSetting.ns2domain,
        SystemSetting.server_ip))[0]
    response_data = jsonify(status=200, message="查询成功", data=OrmModelJsonSerializer.serializer(system_setting))
    return response_data


@system_set.route("/api/v1/system_set/dns", methods=["PUT"], endpoint="update_dns_server_system_set")
@check_authentication
def update_dns_server_system_set():
    """
    修改DNS服务设置
    请求如下

    PUT /api/v1/system_set/dns
    
    {"fake_root_domain":"1", "ns1domain":"ns1domain", "ns2domain":"ns2domain", "server_ip":"server_ip", "dns_switch": true}
    :return: 
    """
    post_data = request.get_json(force=True)
    fake_root_domain = post_data["fake_root_domain"]
    ns1domain = post_data["ns1domain"]
    ns2domain = post_data["ns2domain"]
    server_ip = post_data["server_ip"]
    dns_switch = post_data["dns_switch"]

    row_nums = SystemSettingService.update(fields=(
        {SystemSetting.fake_root_domain: fake_root_domain, SystemSetting.ns1domain: ns1domain,
         SystemSetting.ns2domain: ns2domain, SystemSetting.server_ip: server_ip,
         SystemSetting.dns_switch: dns_switch}))
    message = "成功更新{}条数据".format(row_nums)

    if dns_switch:
        process = Process(target=DnsServer.restart_server, args=("0.0.0.0", 53, fake_root_domain, ns1domain, ns2domain, server_ip))
        process.start()

    if dns_switch is not None and dns_switch is False:
        process = Process(target=DnsServer.kill_server, args=("0.0.0.0", 53))
        process.start()
    """
    dns_server = DnsServer()
    dns_server.set_fake_root_domain(fake_root_domain)
    dns_server.set_ns1domain(ns1domain)
    dns_server.set_ns2domain(ns2domain)
    dns_server.serverip(server_ip)
    dns_server.start()
    """

    response_data = jsonify(status=200, message=message, data=[])
    return response_data


@system_set.route("/api/v1/system_set/socket", methods=["GET"], endpoint="show_socket_server_system_set")
@check_authentication
def show_socket_server_system_set():
    """
    显示DNS服务设置
    请求如下

    GET /api/v1/system_set/dns
    :return: 
    """
    system_setting = SystemSettingService.get_fields_by_where(fields=(
        SystemSetting.socket_port, SystemSetting.socket_switch))[0]
    response_data = jsonify(status=200, message="查询成功", data=OrmModelJsonSerializer.serializer(system_setting))
    return response_data


@system_set.route("/api/v1/system_set/socket", methods=["PUT"], endpoint="update_socket_server_system_set")
@check_authentication
def update_socket_server_system_set():
    """
    修改SOCKET服务设置
    请求如下

    PUT /api/v1/system_set/socket

    {"socket_port":8878, "socket_switch": true}
    
    :return: 
    """
    post_data = request.get_json(force=True)
    socket_port = int(post_data["socket_port"])
    socket_switch = post_data["socket_switch"]
    row_nums = SystemSettingService.update(fields=(
        {SystemSetting.socket_port: socket_port, SystemSetting.socket_switch: socket_switch}))
    message = "成功更新{}条数据".format(row_nums)

    if socket_switch:
        process = Process(target=TcpServer.restart_server, args=("0.0.0.0", socket_port))
        process.start()

    if socket_switch is not None and socket_switch is False:
        process = Process(target=TcpServer.kill_server, args=("0.0.0.0", socket_port))
        process.start()

    response_data = jsonify(status=200, message=message, data=[])
    return response_data
