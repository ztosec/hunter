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
import time
import signal
import socket
import psutil
from log import logger
from model.request_log import RequestLog
from model.request_log_dup import RequestLogDup
from abc import ABCMeta, abstractmethod


class BaseServer(metaclass=ABCMeta):
    """
    服务抽象类
    >>> tcpServer = TcpServer('0.0.0.0', 7799)
    >>> tcpServer.start()
    """

    def __init__(self, host, port, module_name):
        """
        
        :param host: 
        :param port: 
        """
        self.host = host
        self.port = port
        self.logger = logger.get_default_logger()
        self.module_name = module_name

    def start(self):
        """
        启动函数
        :return: 
        """
        self.logger.info(
            "DnsSocketLog启动{name}模块即将监听地址为{host}:{port}".format(name=self.module_name, host=self.host, port=self.port))
        self.check_address_used(True)
        status = self.start_bind()
        if status:
            self.logger.info(
                "DnsSocketLog启动{name}模块并监听地址为{host}:{port}成功".format(name=self.module_name, host=self.host,
                                                                     port=self.port))
            self.start_engine()
        else:
            self.logger.error(
                "DnsSocketLog启动{name}模块并监听地址为{host}:{port}失败".format(name=self.module_name, host=self.host,
                                                                     port=self.port))

    def stop(self):
        """
        终止函数
        :return: 
        """
        self.logger.info(
            "DnsSocketLog即将关闭端口{}所在的进程服务".format(self.port))
        self.check_address_used(True)

    @abstractmethod
    def start_bind(self):
        """
        启动监听
        :return: 
        """
        return False

    @abstractmethod
    def start_engine(self):
        """
        启动引擎，包含具体逻辑
        :return: 
        """

    def check_address_used(self, kill=False):
        """
        检测端口是否被占用，并决定是否关闭
        :param kill: 是否关闭进程
        :return: 
        """
        conns = None
        try:
            conns = psutil.net_connections(kind='inet')
        except psutil.AccessDenied as e:
            self.logger.exception("kill_server出现异常，请以root权限运行")
            exit()
        else:
            if conns is None:
                return
            for conn in conns:
                if conn.laddr[1] == self.port and conn.status == 'LISTEN':
                    # os.kill(conns.pid, signal.SIGKILL) 会把父进程杀掉
                    # exit()
                    if kill:
                        self.logger.warn("DnsSocketLog检测到端口{}被应用进程为{}正在占用，即将自动关闭该进程".format(self.port, conn.pid))
                        os.kill(conn.pid, signal.SIGKILL)  # 自动KILL进程杀掉
                        self.logger.info("DnsSocketLog检测到端口{}被应用进程为{}正在占用，关闭成功".format(self.port, conn.pid))
                    else:
                        self.logger.warn(
                            "DnsSocketLog检测到端口{}被应用进程为{}正在占用，你可以手动关闭它或者设置kill=True".format(self.port, conn.pid))
            time.sleep(2)

    @abstractmethod
    def close_server(self):
        """
        关闭socket服务
        :return: 
        """
        pass
