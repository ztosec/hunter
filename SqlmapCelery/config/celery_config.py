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
Copyright (c) 2018

将抓取到的流量分发到sqlmap,xssfork,hunter 三个队列中，采用多个worker消费同一个队列的模式-分布式模式
将系统通知消息放到 Exchange('system_notice', type='fanout')，worker收到通知执行对于的动作，下载，删除，禁用插件
"""
from kombu import Exchange, Queue
from kombu.common import Broadcast

#
#
#
#

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'Europe/Oslo'
enable_utc = True
task_acks_late = True
worker_prefetch_multiplier = 1
worker_max_tasks_per_child = 200

# 不要和修改删除本文件中的东西

# Queue('sqlmap', Exchange('hunter_raw_traffic', type='fanout'), routing_key='hunter'),
# Queue('xssfork', Exchange('hunter_raw_traffic', type='fanout'), routing_key='hunter'),
# Queue('hunter', Exchange('hunter_raw_traffic', type='fanout'), routing_key='hunter'),
# Broadcast(exchange=Exchange('hunter_system_notice', type='fanout'), routing_key='system'),

task_queues = {
Queue('sqlmap', Exchange('hunter_raw_traffic', type='fanout'), routing_key='hunter'),
    Queue('task', Exchange('hunter_task_notice', type='fanout'), routing_key='task'),
    Broadcast(exchange=Exchange('hunter_system_notice', type='fanout'), routing_key='system'),
}


class MyRouter(object):
    def route_for_task(self, task, args=None, kwargs=None):
        if task.startswith('hunter_celery.scan_celery'):
            return {
                'exchange': 'hunter_raw_traffic', "routing_key": "hunter"
            }
        elif task.startswith('hunter_celery.system_notice_celery'):
            return {
                'exchange': 'hunter_system_notice', "routing_key": "system"
            }
        elif task.startswith('hunter_celery.task_notice_celery'):
            return {
                'exchange': 'hunter_task_notice', "routing_key": "task"
            }
        else:
            return None


# 将不同的任务放到不同的队列
# task_routes = {'hunter_celery.scan_celery': {'exchange': 'broadcast_tasks'}}
# 声明队列和exchange
task_routes = (MyRouter(),)
#
broker_url="amqp://admin:rabbitmq123456@127.0.0.1:5672"
