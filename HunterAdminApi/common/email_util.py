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
import json
import logging
import traceback
import smtplib
from email.header import Header
import email.mime.multipart
import email.mime.text
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from model.system_config import SystemConfigService, SystemConfig
from common import log
from common.config_util import get_system_config

logger = log.get_default_logger()


class EmailUtils(object):
    """
    邮件发送工具类
    """

    def __init__(self):
        """
        初始化配置
        """
        email_config = self.get_email_config()
        self.mail_host = email_config.smtp_host
        self.mail_port = email_config.smtp_port
        self.mail_username = email_config.sender_email
        self.mail_password = email_config.sender_password
        self.mail_sender = email_config.sender_email
        # self.message = email.mime.multipart.MIMEMultipart()

    def get_email_config(self):
        """
        获得邮件配置
        :return: 
        """
        system_config = SystemConfigService.get_single_instance(refresh=True)
        return system_config

    def send_mail_with_out_ssl(self, receivers, subject, content):
        """
        发送邮件
        :param receivers: 
        :param message: 
        :return: 
        """
        # print(content)
        try:
            # logger.setLevel(logging.DEBUG)
            # 邮件正文
            msg = MIMEText(content, 'html', 'utf-8')
            msg['from'] = self.mail_username
            msg['subject'] = subject

            smtpObj = smtplib.SMTP()
            smtpObj.connect(self.mail_host, self.mail_port)  # 25 为 SMTP 端口号
            smtpObj.login(self.mail_username, self.mail_password)
            smtpObj.sendmail(self.mail_sender, receivers, str(msg))
            logger.info("hunter send eamil to {} success".format(receivers))
        except Exception as e:
            logger.exception("send_mail_with_out_ssl raise error")
            logger.error("hunter send eamil to {} fail".format(receivers))

    def __send_mail_with_ssl(self, receiver, subject, content, attach=None):
        """
        发送提醒邮件，ssl加密
        :param receiver: 
        :param message: 
        :return: 
        """

        msg = MIMEText(content, 'html', 'utf-8')
        """
        msg['Subject'] = Header("hunter平台提示", 'utf-8')
        msg['From'] = Header(self.mail_username)
        msg['To'] = Header(receiver, 'utf-8')
        """
        msg['Subject'] = subject
        msg['From'] = self.mail_username
        msg['To'] = receiver

        from_addr = self.mail_username  # 发件邮箱
        password = self.mail_password  # 邮箱密码(或者客户端授权码)
        to_addr = receiver  # 收件邮箱

        try:
            server = smtplib.SMTP_SSL(self.mail_host, self.mail_port)  # 第二个参数为默认端口为25，这里使用ssl，端口为994
            server.login(from_addr, password)  # 登录邮箱
            server.sendmail(from_addr, to_addr, msg.as_string())  # 将msg转化成string发出
            # server.quit()
            logger.info("hunter send eamil to {} success".format(receiver))
        except Exception:
            logger.exception("send_mail_with_ssl raise error")
            logger.error("hunter send eamil to {} fail".format(receiver))

    def send_mail_with_ssl(self, receivers, subject, content, attach=None):
        """
        向多个用户发送邮件
        :param receivers: 
        :param subject: 
        :param content: 
        :param attach: 
        :return: 
        """
        assert isinstance(receivers, str)
        receiver_list = receivers.split(",")
        for receiver in receiver_list:
            self.__send_mail_with_ssl(receiver, subject, content, attach)
