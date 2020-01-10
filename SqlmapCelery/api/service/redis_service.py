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
To use:
redis服务，保存任务基本信息
"""
import json
import hashlib
from common import log
from common.redis_util import RedisManage
from model.default_value import TaskStatus
from common import http_util
from common.json_utils import dict_to_object
from plugins.base.vuln_enum import PluginSwith
from plugins.base.base_checker import BaseChecker
from exception.hunter_web_exception import RedisError
from exception.hunter_web_exception import UserNotFoundInRedisException


class RedisService:
    logger = log.get_default_logger()
    HUNTER_TASK_KEYS = "hunter-task:"
    HUNTER_URLCLASSIFICATIONS_KEYS = "simplify_request"
    HUNTER_USER = "hunter-user:"
    HUNTER_PLUGIN = "hunter-plugin:"
    HUNTER_PLUGIN_SWITCH = "hunter-plugin-switch"

    @staticmethod
    def get_user(user_name):
        """
        根据用户名称获取用户
        :param user_name: 
        :return: 
        """
        user = dict()
        try:
            user = RedisManage.get_redis_client().hgetall("{}{}".format(RedisService.HUNTER_USER, user_name))
        except Exception as e:
            RedisService.logger.exception("RedisService get_user error")
            raise e
        finally:
            if not user:
                raise UserNotFoundInRedisException("未从redis中找到用户信息")
            user_object = dict_to_object(user)
            return user_object

    @staticmethod
    def remove_user(user_name):
        """
        根据用户名删除用户
        :param user_name: 
        :return: 
        """
        try:
            hashkey = "{}{}".format(RedisService.HUNTER_USER, user_name)
            if RedisManage.get_redis_client().exists(hashkey):
                hashkey_all = RedisManage.get_redis_client().hkeys(hashkey)
                for i in range(len(hashkey_all)):
                    RedisManage.get_redis_client().hdel(hashkey, hashkey_all[i])
        except Exception as e:
            RedisService.logger.exception("RedisService remove_user error")

    @staticmethod
    def update_user(user_name, user_info):
        """
        保存用户信息到redis中，在用户退出登录之后同步，记得设置session，过期时间为两小时
        user_info包含字段如下 role
        warning: 需要注意的是不能出现为None的情况
        :param user_name: 
        :param user_info: 
        :return: 
        """
        try:
            for (key, value) in user_info.items():
                if value is None:
                    user_info[key] = ""
            RedisManage.get_redis_client().hmset(RedisService.HUNTER_USER + user_name, user_info)
        except Exception:
            RedisService.logger.exception("RedisService update_user error")

    @staticmethod
    def update_user_field(user_name, field_name, field_value):
        """
        修改用户某个字段的值
        :param user_name: 
        :param field_name: 
        :param field_value: 
        :return: 
        """
        try:
            RedisManage.get_redis_client().hset(RedisService.HUNTER_USER + user_name, field_name, field_value)
        except Exception:
            RedisService.logger.exception("RedisService update_user_field error")

    @staticmethod
    def create_task(task_id, hook_rule, openid, status):
        """
        创建任务，即向redis中存入hook_rule,openid,status,access_token
        :return: 
        """
        try:
            RedisManage.get_redis_client().hset("{}{}".format(RedisService.HUNTER_TASK_KEYS, task_id), "hook_rule",
                                                hook_rule)
            RedisManage.get_redis_client().hset("{}{}".format(RedisService.HUNTER_TASK_KEYS, task_id), "user_name",
                                                openid)
            RedisManage.get_redis_client().hset("{}{}".format(RedisService.HUNTER_TASK_KEYS, task_id), "status", status)
        except Exception:
            RedisService.logger.exception("RedisService create_task error")

    @staticmethod
    def stop_task(task_id):
        """
        停止任务
        :param task_id: 
        :return: 
        """
        try:
            RedisManage.get_redis_client().hset("{}{}".format(RedisService.HUNTER_TASK_KEYS, task_id), "status",
                                                TaskStatus.KILLED)
        except Exception:
            RedisService.logger.exception("RedisService stop_task error")

    @staticmethod
    def update_task_hook_rule(task_id, hook_rule):
        """
        更新HookRule
        :param task_id: 
        :param hook_rule: 
        :return: 
        """
        try:
            RedisManage.get_redis_client().hset("{}{}".format(RedisService.HUNTER_TASK_KEYS, task_id), "hook_rule",
                                                hook_rule)
        except Exception:
            RedisService.logger.exception("RedisService update_task_hook_rule error")

    @staticmethod
    def get_task(task_id):
        """
        获取任务详情
        :param task_id: 
        :return: 
        """
        task = dict()
        # result = {"access_token": "", "status": TaskStatus.NONE, "hook_rule": "*", "openid": ""}
        try:
            task = RedisManage.get_redis_client().hgetall("{}{}".format(RedisService.HUNTER_TASK_KEYS, task_id))
        except Exception:
            RedisService.logger.exception("RedisService get_task error")
            task = {"status": TaskStatus.NONE, "hook_rule": "*", "user_name": ""}
        finally:
            if "status" not in task:
                task["status"] = TaskStatus.NONE
            if "hook_rule" not in task:
                task["hook_rule"] = "*"
            if "user_name" not in task:
                task["user_name"] = ""
            user_object = dict_to_object(task)
        return user_object

    @staticmethod
    def save_temp_urlsets(urlclassifications_md5, post_data):
        """
        这个百分之百能成功，因为每次的requestid必定是不同的
        temp_urlsets key为md5(urlclassifications) value为set
        sismember 
        :return: 
        """
        result = False
        try:
            is_exist = RedisManage.get_redis_client().sismember(
                "{}{}".format(RedisService.HUNTER_TEMP_URLSETS_KEYS, urlclassifications_md5), post_data)
            if not is_exist:
                RedisManage.get_redis_client().sadd(
                    "{}{}".format(RedisService.HUNTER_TEMP_URLSETS_KEYS, urlclassifications_md5), post_data)
                result = True
        except Exception:
            RedisService.logger.exception("RedisService save_temp_urlsets error")
            result = False
        return result

    @staticmethod
    def create_urlclassifications(task_id, post_data):
        """
        用于对抓取到的url进行分类，类型为hash，md5:str()，第一次存入返回true表示为新链接
        :return: 
        """
        try:
            post_data["data"].pop('requestid')
            request_raw = post_data["data"]

            http_method = str(request_raw["method"]).lower()
            url = str(request_raw["url"]).strip()
            headers = http_util.header_to_lowercase(json.loads(request_raw['headers']))
            content_type = headers[
                "content-type"] if headers is not None and http_util.ContentType.NAME.lower() in headers else None
            data = request_raw['data'] if "data" in request_raw else None
            simplify_request = BaseChecker.get_parser_class(request_raw).simplify_request(url=url, data=data,
                                                                                          http_method=http_method,
                                                                                          content_type=content_type)
            simplify_request_str = json.dumps(simplify_request)
            # 请求解析归类之后的MD5
            simplify_request_md5 = hashlib.new('md5', simplify_request_str.encode("utf-8")).hexdigest()

            if not RedisManage.get_redis_client().hexists(
                    "{}{}".format(RedisService.HUNTER_URLCLASSIFICATIONS_KEYS, str(task_id)), simplify_request_md5):
                RedisManage.get_redis_client().hset(RedisService.HUNTER_URLCLASSIFICATIONS_KEYS + str(task_id),
                                                    simplify_request_md5, simplify_request_str)
                return True
            return False
        except Exception:
            RedisService.logger.exception("create_urlclassifications error")
            return False

    @staticmethod
    def clean_urlclassifications(task_id):
        """
        清空 simplify_request:taskid
        :param task_id: 
        :return: 
        """
        try:
            RedisManage.get_redis_client().delete("{}{}".format(RedisService.HUNTER_URLCLASSIFICATIONS_KEYS, task_id))
        except Exception:
            RedisService.logger.exception("clean_urlclassifications error")

    @staticmethod
    def get_unuseable_plugin_names():
        """
        获取开关为OFF的插件，从扫描插件实体中去除
        :return: 
        """
        unuseable_plugin_name_list = list()
        try:
            plugin_switch = RedisManage.get_redis_client().hgetall(RedisService.HUNTER_PLUGIN_SWITCH)
            for plugin_name, plugin_swith in plugin_switch.items():
                if plugin_swith == PluginSwith.OFF:
                    unuseable_plugin_name_list.append(plugin_name)
        except Exception:
            RedisService.logger.exception("RedisService get_unuseable_plugin_names error")
        return unuseable_plugin_name_list

    @staticmethod
    def init_plugin_config():
        """
        初始化插件开关
        :return: 
        """
        from common.plugins_util import load_default_checkers
        try:
            checker_dict = load_default_checkers(True)
            for (plugin_name, checker_instance) in checker_dict.items():
                plugin_config_info = json.dumps(
                    {"tag": checker_instance.info["tag"], "useable": PluginSwith.ON, "removed": False})
                RedisManage.get_redis_client().hset(RedisService.HUNTER_PLUGIN_SWITCH, plugin_name, plugin_config_info)
        except Exception:
            RedisService.logger.exception("RedisService update_plugin error")

    @staticmethod
    def modify_plugin_config(plugin_name, plugin_config):
        """
        example {"tag": checker_instance.info["tag"], "useable": PluginSwith.ON, "removed": False}
        :param checker_instance: 
        :param kwargs: 
        :return: 
        """
        assert isinstance(plugin_config, dict)
        RedisManage.get_redis_client().hset(RedisService.HUNTER_PLUGIN_SWITCH, plugin_name, json.dumps(plugin_config))

    @staticmethod
    def modify_plugin_switch(checker_instance, plugin_swith=PluginSwith.OFF):
        """
        服务端更新插件开关，打开或者关闭插件开关，Redis出问题默认降级使用本地配置文件
        :param plugin_swith: 
        :return: 
        """
        try:
            plugin_tag = checker_instance.info["tag"]
            plugin_name = checker_instance.info["name"]
            plugin_config = {"tag": plugin_tag, "useable": plugin_swith, "removed": False}
            if RedisManage.get_redis_client().hexists(RedisService.HUNTER_PLUGIN_SWITCH, plugin_name):
                pre_plugin_config = RedisManage.get_redis_client().hget(RedisService.HUNTER_PLUGIN_SWITCH, plugin_name)
                plugin_config = json.loads(pre_plugin_config)
                plugin_config["useable"] = plugin_swith

            RedisService.modify_plugin_config(plugin_name, plugin_config)
        except Exception:
            RedisService.logger.exception("RedisService modify_plugin_switch error")
