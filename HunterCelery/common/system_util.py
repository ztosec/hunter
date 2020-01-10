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
import re
import sys
import time
import zipfile
import datetime
from common.path import PLUGIN_PATH
from common.json_utils import list_is_blank


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


def zip_file(target_file, origin_file):
    """
    :param target_file: 
    :param origin_file: 
    :return: 
    """
    with zipfile.ZipFile(target_file, 'w', zipfile.ZIP_DEFLATED) as temp_file:
        temp_file.write(origin_file, str(origin_file).replace(PLUGIN_PATH, ""))


def zip_folder(target_file, origin_folder):
    """
    压缩文件夹，默认不跳过任何目录
    :param target_file: 
    :param origin_folder: 
    :return: 
    """
    zip_floder_skip(target_file=target_file, origin_folder=origin_folder)


def __get_zip_abre_floder(origin_folder):
    """
    获取要压缩的文件的相对路径和绝对路径 call by zip_floder_skip
    
    :param origin_folder: 
    :return: 
    """
    ab_absolute_relative_file_paths = []
    for dir_path, dir_names, file_names in os.walk(origin_folder):
        file_path = dir_path.replace(origin_folder, '')
        file_path = file_path and file_path + os.sep or ''
        for filename in file_names:
            absolute_filepath = os.path.join(dir_path, filename)
            relative_filepath = file_path + filename
            ab_absolute_relative_file_paths.append({"absolute_fp": absolute_filepath, "relative_fp": relative_filepath})
    return ab_absolute_relative_file_paths


def __filter_zip_abre_floder_regular(origin_folder, skip_list):
    """
    正则模式下跳过
    :param skip_list: 
    :param relative_filepath: 
    :return: 
    """

    def match(regulars, str):
        for regular in regulars:
            if re.match(r'%s' % regular, str):
                return True
        return False

    result = []
    ab_re_dict_file_paths = __get_zip_abre_floder(origin_folder)
    for ab_re_dict_file_path in ab_re_dict_file_paths:
        absolute_file_path = ab_re_dict_file_path["absolute_fp"]
        relative_file_path = ab_re_dict_file_path["relative_fp"]
        final_skip_list = [skip_str.replace("*", "(.*?)") if "*" in skip_str else skip_str for skip_str in skip_list]
        if not match(final_skip_list, relative_file_path):
            result.append({"absolute_fp": absolute_file_path, "relative_fp": relative_file_path})
    return result


def __filter_zip_abre_floder_default(origin_folder, skip_list):
    """
    默认模式下
    :param origin_folder: 
    :param skip_list: 
    :return: 
    """

    def match(list, str):
        return str in list

    result = []
    ab_re_dict_file_paths = __get_zip_abre_floder(origin_folder)
    for ab_re_dict_file_path in ab_re_dict_file_paths:
        absolute_file_path = ab_re_dict_file_path["absolute_fp"]
        relative_file_path = ab_re_dict_file_path["relative_fp"]
        if not match(skip_list, relative_file_path):
            result.append({"absolute_fp": absolute_file_path, "relative_fp": relative_file_path})
    return result


def zip_floder_skip(target_file, origin_folder, is_regular=False, skip_list=None):
    """
     压缩并且跳过某个文件夹，支持正则模式
    :param target_file: 
    :param origin_folder: 
    :param skip: 
        is_regular: False
        skip_list: []
    :return: 
    """
    ab_re_dict_file_paths = list()
    if not skip_list:
        ab_re_dict_file_paths = __get_zip_abre_floder(origin_folder)
    # 正则模式
    if is_regular and not list_is_blank(skip_list):
        ab_re_dict_file_paths = __filter_zip_abre_floder_regular(origin_folder, skip_list)
    # 默认匹配模式
    if not is_regular and not list_is_blank(skip_list):
        ab_re_dict_file_paths = __filter_zip_abre_floder_default(origin_folder, skip_list)

    with zipfile.ZipFile(target_file, 'w', zipfile.ZIP_DEFLATED) as temp_zip_file:
        for ab_re_dict_file_path in ab_re_dict_file_paths:
            temp_zip_file.write(ab_re_dict_file_path["absolute_fp"], ab_re_dict_file_path["relative_fp"])


def unzip_file(origin_file, target_folder):
    with zipfile.ZipFile(origin_file, 'r') as zip_temp_file:
        zip_temp_file.extractall(path=r"%s" % target_folder)
