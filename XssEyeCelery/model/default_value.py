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

DEFAULT_TASK_ID = 999999999

DEFAULT_CREATE_USER = "None"

DEFAULT_IS_ADMINISTRATOR = 0


class TaskStatus(object):
    """
    WAITING 表示正在排列等待
    WORKING 表示开始消费MQ
    DONE 表示已经将MQ中的数据消费完成，表示系统检测完成
    KILLED 插件点击了停止,表示不再接收任何HOOK到的数据，表示用户停止
    NONE 无任何实际意义
    """
    WAITING = 0
    WORKING = 1
    DONE = 2
    KILLED = 3
    NONE = -1


class Role(object):
    """
    用户角色
    USER为普通用户权限，即只能操作自己的
    保留权限为部门经理，开发角色，总监，CTO，CEO 暂时可能用不上

    """
    USER = 0
    ADMIN = 4
