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

>>> from notice.subject import Subject
>>> Subject.get_default().notify_all_observers(task_id)
"""
import threading
from notice.base_observer import BaseObserver
from notice.email_observer import EmailObserver
 
 


class Subject:
    _instance_lock = threading.Lock()

    @staticmethod
    def get_default():
        """
        默认注册邮件，同安，星云通知
        :return: 
        """
        if not Subject.initialized():
            subject_instance = Subject.instance()
            email_observer = EmailObserver()
 
 
            subject_instance.attach(email_observer)
 
 

        return Subject.instance()

    def __init__(self):
        self._subscribers = list()

    @staticmethod
    def instance():
        """
        获取单例
        :return: 
        """
        if not hasattr(Subject, "_instance"):
            with Subject._instance_lock:
                if not hasattr(Subject, "_instance"):
                    Subject._instance = Subject()
        return Subject._instance

    @staticmethod
    def initialized():
        return hasattr(Subject, "_instance")

    def install(self):
        assert not Subject.initialized()
        Subject._instance = self

    @staticmethod
    def clear_instance():
        if hasattr(Subject, "_instance"):
            del Subject._instance

    def attach(self, observer):
        """
        添加订阅
        :param observer: 
        :return: 
        """
        assert isinstance(observer, BaseObserver)
        if observer not in self._subscribers:
            self._subscribers.append(observer)

    def detach(self, observer):
        """
        取消订阅
        :param observer: 
        :return: 
        """
        assert isinstance(observer, BaseObserver)
        if observer in self._subscribers:
            self._subscribers.remove(observer)

    def notify_all_observers(self, task_id):
        """
        将消息通知到所有的订阅者
        :return: 
        """
        for observer in self._subscribers:
            observer.notify(task_id)
