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
import os
import sys
import time
import math
import datetime
from multiprocessing import cpu_count


def get_cpu_num():
    """
    获取操作系统的核数
    :return: 
    """
    return cpu_count()


def get_current_time(type='str'):
    if type == "float":
        return time.time()
    if type == 'str':
        return time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime())


def get_current_date():
    return time.strftime("%Y-%m-%d", time.localtime())


def get_front_date(day_range):
    """
    获取前day_range天的时间
    :param day_range: 时间范围，天数
    :return: 
    """
    today = datetime.datetime.now()
    # 计算偏移量
    offset = datetime.timedelta(days=-day_range)
    # 获取想要的日期的时间
    re_date = (today + offset).strftime('%Y-%m-%d')
    return re_date


def days(str1, str2):
    """
    获取相差天数
    :param str1: 
    :param str2: 
    :return: 
    """
    from datetime import datetime

    date1 = datetime.strptime(str1[0:10], "%Y-%m-%d")
    date2 = datetime.strptime(str2[0:10], "%Y-%m-%d")
    num = (date1 - date2).days
    return num


def minutes(str1, str2):
    """
    获取相差的分钟
    2018-08-02-15:07:31
    :param str1: 
    :param str2: 
    :return: 
    """
    from datetime import datetime
    year1 = datetime.strptime(str1[0:10], "%Y-%m-%d").year
    year2 = datetime.strptime(str2[0:10], "%Y-%m-%d").year
    month1 = datetime.strptime(str1[0:10], "%Y-%m-%d").month
    month2 = datetime.strptime(str2[0:10], "%Y-%m-%d").month
    day1 = datetime.strptime(str1[0:10], "%Y-%m-%d").day
    day2 = datetime.strptime(str2[0:10], "%Y-%m-%d").day
    hour1 = datetime.strptime(str1[0:19], "%Y-%m-%d-%H:%M:%S").hour
    hour2 = datetime.strptime(str2[0:19], "%Y-%m-%d-%H:%M:%S").hour
    minute1 = datetime.strptime(str1[0:19], "%Y-%m-%d-%H:%M:%S").minute
    minute2 = datetime.strptime(str2[0:19], "%Y-%m-%d-%H:%M:%S").minute
    num = (year1 - year2) * 12 * 30 * 24 * 60 + (month1 - month2) * 30 * 24 * 60 + (day1 - day2) * 24 * 60 + (
                                                                                                                 hour1 - hour2) * 60 + (
              minute1 - minute2)
    return num


def minutes_(datetime1, datetime2):
    """
    获取相差的分钟
    2018-08-02-15:07:31
    :param str1: 
    :param str2: 
    :return: 
    """

    if datetime1 and datetime2:
        year1 = datetime1.year
        year2 = datetime2.year
        month1 = datetime1.month
        month2 = datetime2.month
        day1 = datetime1.day
        day2 = datetime2.day
        hour1 = datetime1.hour
        hour2 = datetime2.hour
        minute1 = datetime1.minute
        minute2 = datetime2.minute
        num = (year1 - year2) * 12 * 30 * 24 * 60 + (month1 - month2) * 30 * 24 * 60 + (day1 - day2) * 24 * 60 + (
                                                                                                                     hour1 - hour2) * 60 + (
                  minute1 - minute2)
    else:
        num = 0
    return num


def months(str1, str2):
    """
    获取相差月数
    :param str1: 
    :param str2: 
    :return: 
    """
    from datetime import datetime

    year1 = datetime.strptime(str1[0:10], "%Y-%m-%d").year
    year2 = datetime.strptime(str2[0:10], "%Y-%m-%d").year
    month1 = datetime.strptime(str1[0:10], "%Y-%m-%d").month
    month2 = datetime.strptime(str2[0:10], "%Y-%m-%d").month
    num = (year1 - year2) * 12 + (month1 - month2)
    return num


def mkdir(path):
    """
    新建文件夹
    :param path: 
    :return: 
    """
    path = path.strip().rstrip("\\")
    is_exist = os.path.exists(path)
    if not is_exist:
        os.makedirs(path)


def get_python_version():
    return sys.version_info


def is_python3():
    """
    判断是否大于3.6，大于3.6才有ModuleNotFoundError
    :return: 
    """
    return get_python_version() >= (3, 6)


def encode_b64(number, filter=True):
    """
    :param number: 
    :param filter:  保留原文带000还是去除0000
    :return: 
    """
    number = int(number)
    table = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-_'
    result = []
    temp = number
    if 0 == temp:
        result.append('0')
    else:
        while 0 < temp:
            result.append(table[int(temp % 64)])
            temp /= 64

    b64 = ''.join([x for x in reversed(result)])
    if filter:
        for i in range(0, len(result)):
            if b64[i] != '0':
                break
        b64 = b64[i:]
    return b64


def split_array(array, num):
    """
    均匀分割数组
    :param array: 
    :return: 
    """
    assert isinstance(array, list)
    array_length = len(array)
    result = list()
    for i in range(num):
        result.append(array[math.floor((i / num) * array_length): math.floor((i + 1) / num * array_length)])
    return result
