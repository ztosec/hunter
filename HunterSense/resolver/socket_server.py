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
import sys
import socket
import psutil
import selectors
from log import logger
from functools import partial
from common import config

from resolver.base_server import BaseServer
from model.request_log import RequestLog, RequestLogService
from model.request_log_dup import RequestLogDup, RequestLogDupService


class TcpServer(BaseServer):
    """
    作用于内网环境，而又不想配置域名以及DNS记录，直接使用ServerSocket记录信息即可
    linux下使用epoll，unix下使用kqueue，root权限调用，开启子进程
    使用如下:
    >>> tcpServer = TcpServer('0.0.0.0', 7799)
    >>> tcpServer.start()
    """

    def __init__(self, host, port=config.SERVER_SOCKET_PORT):
        """
        初始化日志和NIO相关信息
        :param host: 
        :param port: 
        """
        super().__init__(host, port, self.__class__.__name__)
        self.selector = selectors.DefaultSelector()
        self.fd_handlers = {}  # 文件描述符和处理函数(主要是读写)
        self.server_socket = None
        self.protocol = "tcp"

    def start_bind(self):
        """
        NIO调用核心调用逻辑
        :return : 是否启动端口成功
        """
        try:
            self.bind_server()
            self.server_socket.listen()
            return True
        except OSError:
            # 未知IO异常
            self.logger.exception("start_bind出错")
            self.close_server()
            return False

    def close_server(self):
        """
        关闭服务
        :return: 
        """
        if self.server_socket:
            try:
                self.server_socket.shutdown(socket.SHUT_RDWR)
                self.server_socket.close()
            except OSError as e:
                print(e)

    def start_engine(self):
        """
        start_bind 返回True之后调用
        :return: 
        """
        server_socket_fd = self.server_socket.fileno()
        self.selector.register(self.server_socket, selectors.EVENT_READ, self.accept)
        self.fd_handlers[server_socket_fd] = partial(self.accept, self.server_socket)
        while True:
            events = self.selector.select()
            for key, mask in events:
                handler = self.fd_handlers.get(key.fd)
                if handler:
                    handler()

    def bind_server(self):
        """
        绑定端口
        :return: 
        """
        self.server_socket = socket.socket()
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.setblocking(False)  # 设置非堵塞
        self.server_address = (self.host, self.port)
        try:
            self.server_socket.bind(self.server_address)
        except OSError as e:
            raise e

    def accept(self, server_socket):
        """
        接收
        :return: 
        """
        try:
            conn, address = server_socket.accept()
        except OSError:
            self.logger.exception("accept出现问题")
        else:
            self.logger.warn("接收来自{}的新连接".format(address))
            conn.setblocking(False)
            self.selector.register(conn, selectors.EVENT_READ, self.read)  # 注册读事件
            self.fd_handlers[conn.fileno()] = partial(self.read, conn, address)

    def read(self, conn, address):
        """
        读函数，读取并解析客户端发出的请求数据，一般情况下是http
        :param conn: 
        :param address: 
        :return: 
        """
        self.selector.unregister(conn)
        self.fd_handlers.pop(conn.fileno(), None)
        try:
            data = conn.recv(1024)
        except socket.error as e:
            self.logger.exception("recv出现问题")
        else:
            if data:
                self.show_req_data(data)
                # 解析并保存数据
                self.save_request_log(data, address)
                self.selector.register(conn, selectors.EVENT_WRITE, self.write)
                self.fd_handlers[conn.fileno()] = partial(self.write, conn, address)
            else:
                conn.close()
                self.logger.warn("无数据，来自{}的连接关闭".format(address))

    def show_req_data(self, data):
        """
        展示请求中的数据
        :param data: 
        :return: 
        """
        self.logger.info("*******client*******")
        try:
            self.logger.info("\n" + data.decode("utf-8"))
        except UnicodeDecodeError as e:
            pass
        self.logger.info("*******client*******")

    def write(self, conn, address):
        """
        响应
        :param conn: 
        :param mask: 
        :return: 
        """
        self.selector.unregister(conn)
        self.fd_handlers.pop(conn.fileno(), None)
        try:
            conn.sendall(bytes("HTTP/1.1 201 OK\r\n\r\n", "utf-8"))  # 响应头
            conn.send(bytes(config.SOCKET_RESPONSE_CONTENT, config.ENCODE_TYPE))
        except OSError as e:
            self.logger.exception("write 出错")
        finally:
            conn.close()
            self.logger.warn("关闭来自{}的连接".format(address))

    def parse_request_data(self, recv_data, addr):
        """
        解析http请求的数据，该请求为检测owasp_xxe的POC ，把owasp_xxe存入当作plugin_name
         >>> curl http://127.0.0.1:7799/owasp_xxe
        :param data: 
        :param addr: 
        :return: 
        """
        remote_addr = addr[0]
        remote_port = addr[1]
        plugin_name = ""
        data_line = list()
        try:
            data_list = recv_data.decode("utf-8").split("\r\n")
        except UnicodeDecodeError as e:
            pass
        else:
            for data_line in data_list:
                if "".join(data_line.split()).startswith('GET'):
                    data_line = "".join(data_line.split()).replace("GET/", "").replace("HTTP/1.1", "").replace(
                        "HTTP/1.0", "")
                    plugin_name = data_line
        return remote_addr, remote_port, plugin_name, self.protocol, recv_data.decode("utf-8")

    def save_request_log(self, recv_data, addr):
        """
        记录保存请求日志，调用位置为 
        :param recv_data: 
        :param addr: 
        :return: 
        """
        remote_addr, remote_port, plugin_name, protocol, recv_data = self.parse_request_data(recv_data, addr)

        RequestLogService.save(ip=remote_addr, port=remote_port, plugin=plugin_name, recv_data=recv_data,
                               protocol=protocol)
        RequestLogDupService.save(ip=remote_addr, port=remote_port, plugin=plugin_name, recv_data=recv_data,
                                  protocol=protocol)

    @staticmethod
    def restart_server(host, port):
        """
        被子进程调用
        :param host: 
        :param port: 
        :return: 
        """
        TcpServer(host, int(port)).start()

    @staticmethod
    def kill_server(host, port):
        """
        被子进程调用
        :param host: 
        :param port: 
        :return: 
        """
        TcpServer(host, int(port)).stop()
