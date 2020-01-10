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
import json
import threading
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex


def synchronized(func):
    func.__lock__ = threading.Lock()

    def synced_func(*args, **kwargs):
        with func.__lock__:
            return func(*args, **kwargs)

    return synced_func


class prpcrypt():
    """
    加密类
    """
    __single_instance = None

    @synchronized
    def get_single_instance(key, refresh=False):
        """
        获得单例
        :return: 
        """
        if refresh or prpcrypt.__single_instance is None or prpcrypt.__single_instance.key != key:
            prpcrypt.__single_instance = prpcrypt(key)

        return prpcrypt.__single_instance

    def __init__(self, key):
        self.key = key
        self.mode = AES.MODE_CBC
        self.cipher_text = None

    def encrypt(self, text):
        """
        加密函数，如果text不足16位就用空格补足为16位，
        如果大于16当时不是16的倍数，那就补足为16的倍数。
        :param text: 
        :return: 
        """
        cryptor = AES.new(self.key, self.mode, b'0000000000000000')
        length = 16
        count = len(text)
        if count < length:
            add = (length - count)
            text = text + ('\0' * add)
        elif count > length:
            add = (length - (count % length))
            text = text + ('\0' * add)
        self.cipher_text = cryptor.encrypt(text)
        return b2a_hex(self.cipher_text)

    def decrypt(self, text):
        """
        解密函数，去掉补足的空格用strip() 去掉
        :param text: 
        :return: 
        """
        cryptor = AES.new(self.key, self.mode, b'0000000000000000')
        plain_text = cryptor.decrypt(a2b_hex(text))
        return plain_text.decode("utf-8").rstrip('\0')


def generate_access_key(task_id, username):
    """
    将 其他三个参数组合成 {"task_id":"1", "username":"lilie", "create_time":"2018-12992"} 后用ase加密
    :param private_key: 
    :param task_id: 
    :param username: 
    :param create_time: 
    :return: 
    """
    import datetime
    from model.system_config import SystemConfigService

    create_time = str(datetime.datetime.now())
    private_key = SystemConfigService.get_single_instance().task_access_private_key
    clear_data = {"task_id": task_id, "username": username, "create_time": create_time}
    return prpcrypt.get_single_instance(private_key, False).encrypt(json.dumps(clear_data))
