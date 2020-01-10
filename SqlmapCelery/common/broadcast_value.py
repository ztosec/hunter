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
celery worker 收到系统广播消息常量枚举
一个完成的 boradcast消息格式如下 
{"type": "plugin", "action": "modify", "data": {"name": checker_name, "switch": PluginSwith.ON}}
"""


class BroadCastType(object):
    PLUGIN = "plugin"
    TASK = "task"


class BroadCastAction(object):
    """
    插件通知类
        修改，禁用插件
    任务通知类
        任务结束，可选择消息提醒方式，邮件,钉钉等
    """
    MODIFY_PLUGIN = "modify"
    DELETE_PLUGIN = "delete"
    INSERT_PLUGIN = "insert"
    COMPLETE_TASK_NOTIFICATION = "complete_task_notification"
