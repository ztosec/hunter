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
from notice.base_observer import BaseObserver
from common.email_util import EmailUtils
from common.config_util import get_system_config

from model.task import Task, TaskService
from model.vulnerability import Vulnerability, VulnerabilityService
from model.user import User, UserService
from common import log

logger = log.get_default_logger()


class EmailObserver(BaseObserver):
    def notify(self, task_id):
        """
        发送邮件通知
        :return: 
        """
        email_content, receivers_email = self.generate_report(task_id=task_id)
        logger.info("task task_id:{} has been checked out, hunter will send result to email:{}".format(task_id,
                                                                                                       receivers_email))
        if receivers_email is not None and receivers_email.strip() != "":
            EmailUtils().send_mail_with_ssl(receivers_email, "Hunter扫描完成提醒", email_content)

    def generate_report(self, task_id):
        """
        生成邮件发送报告
        :param cls: 
        :param task_id: 
        :return: 
        """
        current_task = TaskService.get_fields_by_where(where=(Task.id == task_id))[0]
        vulns_info = VulnerabilityService.get_fields_by_where(where=(Vulnerability.task_id == task_id))
        users = UserService.get_users(task_id=task_id)
        if len(vulns_info) <= 0:
            content = """<br>你好，欢迎使用Hunter，本次扫描结束，扫描到你有0个漏洞。详情请可登录{}查看<br>""".format(
                get_system_config()['front_end']['index'])
        else:
            content = """<br>你好，欢迎使用Hunter，本次扫描结束，扫描到你有{}个漏洞。任务预览如下,详情请登录{}查看<br>""".format(len(vulns_info),
                                                                                            get_system_config()[
                                                                                                'front_end'][
                                                                                                'index'])

            content += """
                        <table frame='border' cellpadding='15' cellspacing='0' align='center' style='border: 1px solid #d6d3d3;'>
                            <tr style='background: #e6e6e6;'>
                                <th style="border-right: 1px solid #bfbfbf;">序号</th>
                                <th style="border-right: 1px solid #bfbfbf;">漏洞等级</th>
                                <th style="border-right: 1px solid #bfbfbf;">漏洞类型</th>
                                <th style="border-right: 1px solid #bfbfbf;">漏洞详情</th>
                            </tr>
                        """
            index = 0
            for vuln_info in vulns_info:
                index += 1
                vuln_detail_url = '<a href="{}">{}</a>'.format(
                    get_system_config()['front_end']['vuln_route'] + str(task_id),
                    vuln_info.info)
                content += """
                                    <tr>
                                        <td style="border-right: 1px solid #bfbfbf;">{}</td>
                                        <td style="border-right: 1px solid #bfbfbf;">{}</td>
                                        <td style="border-right: 1px solid #bfbfbf;">{}</td>
                                        <td style="border-right: 1px solid #bfbfbf;">{}</td>
                                    </tr>

                            """.format(index, vuln_info.level, vuln_info.chinese_type, vuln_detail_url)
            content += """</table>"""

        return content, ",".join([user.email for user in users if user.email])
