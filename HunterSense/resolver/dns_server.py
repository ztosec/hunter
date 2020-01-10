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
To use:
"""
import time
import base64, binascii
from log import logger
from common import config
from resolver.base_server import BaseServer
from model.request_log import RequestLog, RequestLogService
from model.request_log_dup import RequestLogDup, RequestLogDupService
from dnslib import RR, QTYPE, RCODE, TXT
from dnslib import textwrap
from dnslib.server import DNSServer, DNSHandler, BaseResolver, DNSLogger, DNSRecord
from dnslib.zoneresolver import ZoneResolver


class DnsLogger(BaseServer):
    """
            The class provides a default set of logging functions for the various
            stages of the request handled by a DNSServer instance which are
            enabled/disabled by flags in the 'log' class variable.

            To customise logging create an object which implements the DNSLogger
            interface and pass instance to DNSServer.

            The methods which the logger instance must implement are:

                log_recv          - Raw packet received
                log_send          - Raw packet sent
                log_request       - DNS Request
                log_reply         - DNS Response
                log_truncated     - Truncated
                log_error         - Decoding error
                log_data          - Dump full request/response
        """

    def __init__(self):
        self.protocol = "udf"
        self.logger = logger.get_default_logger()

    def log_pass(self, *args):
        pass

    def log_prefix(self, handler):
        pass

    def log_recv(self, handler, data):
        """
        保存请求原始报文，暂不处理
        :param handler: 
        :param data: 
        :return: 
        """
        """
        print("%sReceived: [%s:%d] (%s) <%d> : %s" % (
            self.log_prefix(handler),
            handler.client_address[0],
            handler.client_address[1],
            handler.protocol,
            len(data),
            binascii.hexlify(data)))
        """
        self.logger.info("*******client*******")
        try:
            # bin = binascii.hexlify(data).decode()
            # packet = binascii.unhexlify(bin)
            message = DNSRecord.parse(data)
            print(message)
            # self.logger.info("\n" + message)
        except UnicodeDecodeError as e:
            pass
        self.logger.info("*******client*******")
        pass

    def log_send(self, handler, data):
        pass

    def log_request(self, handler, request):
        """
        保存数据
        :param handler: 
        :param request: 
        :return: 
        """
        remote_addr, remote_port, plugin_name, protocol, recv_data = self.parse_request_data(handler, request)
        RequestLogService.save(ip=remote_addr, port=remote_port, plugin=plugin_name, recv_data=recv_data,
                               protocol=protocol)
        RequestLogDupService.save(ip=remote_addr, port=remote_port, plugin=plugin_name, recv_data=recv_data,
                                  protocol=protocol)

    def parse_request_data(self, handler, request):
        """
        解析需要的数据，无需要解析请求数据
        :param handler: 
        :return: 
        """
        remote_addr = handler.client_address[0]
        remote_port = handler.client_address[1]
        protocol = handler.protocol if handler.protocol else self.protocol
        domain = request.q.qname.__str__()
        # 1.hunter.xxxx.xxx.
        plugin_name = domain.replace("." + config.FAKE_ROOT_DOMAIN + ".", "")
        return remote_addr, remote_port, plugin_name, protocol, ""

    def log_reply(self, handler, reply):
        pass

    def log_truncated(self, handler, reply):
        pass

    def log_error(self, handler, e):
        pass

    def log_data(self, dnsobj):
        pass


class DnsServer(BaseServer):
    """
    DNS服务器，用于部署外网环境，支持回显更多详细信息，需要配置域名，推荐使用，具体配置可以参考文档说明
    
    使用如下:
    默认情况下使用 config下的配置
    >>> dns_server = DnsServer('0.0.0.0', 53)
    >>> dns_server.start()
    
    web后台重启:
    
    >>> dns_server = DnsServer('0.0.0.0', 53)
    >>> dns_server.set_fake_root_domain(fake_root_domain)
    >>> dns_server.set_ns1domain(ns1domain)
    >>> dns_server.set_ns2domain(ns2domain)
    >>> dns_server.set_serverip(serverip)
    >>> dns_server.start()

    """

    def __init__(self, host, port=53):
        """
        开启DNS服务，默认端口是53，不要修改
        :param host: 
        :param port: 
        """
        super().__init__(host, port, self.__class__.__name__)
        self.init_zone()
        self.udp_server = None
        self.fake_root_domain = None
        self.ns1domain = None
        self.ns2domain = None
        self.serverip = None

    def set_fake_root_domain(self, fake_root_domain):
        self.fake_root_domain = fake_root_domain

    def set_ns1domain(self, ns1domain):
        self.ns1domain = ns1domain

    def set_ns2domain(self, ns2domain):
        self.ns2domain = ns2domain

    def set_serverip(self, serverip):
        self.serverip = serverip

    def init_zone(self):
        """
        初始化zone，从sqlite数据库中加载配置
        :return: 
        """

        self.zone = '''        
        *.{fake_root_domain}     IN      NS       {ns1domain}
        *.{fake_root_domain}     IN      NS       {ns2domain}
        *.{fake_root_domain}     IN      A       {serverip}
        {fake_root_domain}     IN      A       {serverip}
        '''.format(
            fake_root_domain=config.FAKE_ROOT_DOMAIN,
            ns1domain=config.NS1_DOMAIN,
            ns2domain=config.NS2_DOMAIN,
            serverip=config.SERVER_IP)

    def start_bind(self):
        """
        启动监听，udp监听同一个端口时只有第一个有用
        :return: 
        """
        self.logger.info("\n" + self.zone)
        resolver = ZoneResolver(textwrap.dedent(self.zone), True)
        dns_logger = DnsLogger()
        self.udp_server = DNSServer(resolver, port=self.port, address=self.host, logger=dns_logger)
        return True

    def start_engine(self):
        """
        启动引擎，包含具体逻辑
        :return: 
        """
        if self.udp_server and isinstance(self.udp_server, DNSServer):
            self.udp_server.start()

    def close_server(self):
        """
        关闭UDP服务
        :return: 
        """
        pass

    @staticmethod
    def restart_server(host, port, fake_root_domain, ns1domain, ns2domain, server_ip):
        """
        被子进程调用
        :param host: 
        :param port: 
        :return: 
        """
        dns_server = DnsServer(host, int(port))
        dns_server.set_fake_root_domain(fake_root_domain)
        dns_server.set_ns1domain(ns1domain)
        dns_server.set_ns2domain(ns2domain)
        dns_server.set_serverip(server_ip)
        dns_server.start()

    @staticmethod
    def kill_server(host, port):
        """
        被子进程调用
        :param host: 
        :param port: 
        :return: 
        """
        DnsServer(host, int(port)).stop()
