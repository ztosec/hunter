#!/ usr/bin/env
# coding=utf-8
"""
author: b5mali4
Copyright (c) 2018
"""

import unittest


class EmailUtilTestCase(unittest.TestCase):
    def testSendBaseEmail(self):
        """
        测试发送邮件
        :return: 
        """
        from common.email_util import EmailUtils
        EmailUtils().send_mail_with_ssl("chenming@zto.cn", "Hunter扫描完成提醒",
                                        "Hi,0:\n你好，欢迎使用Hunter，本次扫描结束，扫描到你有{}个漏洞。详情请查看附件", )

    def testSendHunterTaskEmail(self):
        """
        测试发送hunter扫描结果邮件
        :return: 
        """
        from common.email_util import EmailUtils

        def generate_report(task_id):
            """
            生成邮件发送报告
            :param cls: 
            :param task_id: 
            :return: 
            """
            from common.config_util import get_system_config
            from model.vulnerability import Vulnerability, VulnerabilityService
            vulns_info = VulnerabilityService.get_fields_by_where(where=(Vulnerability.task_id == task_id))
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
                        get_system_config()['front_end']['vuln_route'] + str(task_id), vuln_info.info)
                    content += """
                            <tr>
                                <td style="border-right: 1px solid #bfbfbf;">{}</td>
                                <td style="border-right: 1px solid #bfbfbf;">{}</td>
                                <td style="border-right: 1px solid #bfbfbf;">{}</td>
                                <td style="border-right: 1px solid #bfbfbf;">{}</td>
                            </tr>

                    """.format(index, vuln_info.level, vuln_info.chinese_type, vuln_detail_url)
                content += """</table>"""

                return content

        email_content = generate_report(task_id=308)
        print(email_content)
        EmailUtils().send_mail_with_ssl("root@codersec.net", "Hunter扫描完成提醒", email_content)


if __name__ == "__main__":
    unittest.main()
