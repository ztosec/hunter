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
import json
import peewee
from common.mysql_util import MysqlManage


class HunterModel(peewee.Model):
    def __str__(self):
        """
        序列化成json
        :return: 
        """
        result = dict()
        for key in self.__data__.keys():
            try:
                result[key] = str(getattr(self, key))
            except:
                result[key] = json.dumps(getattr(self, key))
        return json.dumps(result)


class HunterModelService(object):
    @staticmethod
    @MysqlManage.close_database
    def save(cls, **kwargs):
        """
        保存数据内容
        :param cls: 
        :param kwargs: 
        :return: 
        """
        if not kwargs:
            return
        return cls.create(**kwargs)

    @staticmethod
    @MysqlManage.close_database
    def count(cls, **kwargs):
        """
        某个查找结果的数量
        :param cls: 
        :param kwargs: 
        :return: 
        """
        if not kwargs:  # 全删除
            return cls.select().count()

        if "where" in kwargs:  # 查询条件
            if isinstance(kwargs["where"], tuple):
                return cls.select().where(*kwargs["where"]).count()
            else:
                return cls.select().where(kwargs["where"]).count()

    @staticmethod
    @MysqlManage.close_database
    def update(cls, **kwargs):
        """
        执行UPDATE操作
        :param cls: 
        :param kwargs: 
        :return: 
        """
        if not kwargs and "fields" not in kwargs:  # 什么都没填或者字段没填
            return
        if "where" not in kwargs and "fields" in kwargs:  # 字段填入，条件没填，默认全更新
            if isinstance(kwargs["fields"], dict):
                return cls.update(kwargs["fields"]).execute()
            return cls.update(*kwargs["fields"]).execute()

        if "where" in kwargs and "fields" in kwargs:  # 两个都填的情况
            if isinstance(kwargs["where"], tuple) and isinstance(kwargs["fields"], dict):
                return cls.update(kwargs["fields"]).where(*kwargs["where"]).execute()

            if isinstance(kwargs["where"], tuple) and not isinstance(kwargs["fields"], dict):
                return cls.update(*kwargs["fields"]).where(*kwargs["where"]).execute()

            if not isinstance(kwargs["where"], tuple) and isinstance(kwargs["fields"], dict):
                return cls.update(kwargs["fields"]).where(tuple([kwargs["where"]])).execute()

            if not isinstance(kwargs["where"], tuple) and not isinstance(kwargs["fields"], dict):
                return cls.select(*kwargs["fields"]).where(tuple([kwargs["where"]])).execute()

    @staticmethod
    @MysqlManage.close_database
    def remove(cls, **kwargs):
        """
        删除
        :return: 
        """
        if not kwargs:  # 全删除
            return cls.delete().execute()

        if "where" in kwargs:  # 查询条件
            if isinstance(kwargs["where"], tuple):
                return cls.delete().where(*kwargs["where"]).execute()
            else:
                return cls.delete().where(kwargs["where"]).execute()

    @staticmethod
    @MysqlManage.close_database
    def get_objects(cls, **kwargs):
        """
        对外暴露接口
        :param kwargs: 
        :return: 
        """
        objects = list()
        for object in HunterModelService.get_fields_by_where(cls, **kwargs):
            objects.append(object)
        return objects

    @staticmethod
    @MysqlManage.close_database
    def get_fields_by_where(cls, **kwargs):
        """
        基础的CURD操作，通用类
        To use:
        >>> tasks = HunterModelService.__get_fields_by_where(fields=(Task.id, Task.hunter_status), where=(Task.id > 1))
        >>> print(tasks)

        :param kwargs: 
        :return: 
        """
        # cls = self.__class__
        if not kwargs:  # 什么都没填
            return cls.select().execute()

        if "fields" not in kwargs and "where" in kwargs:  # 要的结果字段没填
            if isinstance(kwargs["where"], tuple):
                return cls.select().where(*kwargs["where"]).execute()
            return cls.select().where(tuple([kwargs["where"]])).execute()

        if "where" not in kwargs and "fields" in kwargs:  # 要的结果字段没填
            if isinstance(kwargs["fields"], tuple):
                return cls.select(*kwargs["fields"]).execute()
            return cls.select(kwargs["fields"]).execute()

        if "where" in kwargs and "fields" in kwargs:  # 两个都填的情况
            if isinstance(kwargs["where"], tuple) and isinstance(kwargs["fields"], tuple):
                return cls.select(*kwargs["fields"]).where(*kwargs["where"]).execute()

            if isinstance(kwargs["where"], tuple) and not isinstance(kwargs["fields"], tuple):
                return cls.select(kwargs["fields"]).where(*kwargs["where"]).execute()

            if not isinstance(kwargs["where"], tuple) and isinstance(kwargs["fields"], tuple):
                return cls.select(*kwargs["fields"]).where(tuple([kwargs["where"]])).execute()

            if not isinstance(kwargs["where"], tuple) and not isinstance(kwargs["fields"], tuple):
                return cls.select(kwargs["fields"]).where(tuple([kwargs["where"]])).execute()


class OrmModelJsonSerializer:
    @staticmethod
    def serializer(instances):
        """
        序列化工具
        :param self: 
        :return: 
        """
        if not isinstance(instances, list) and isinstance(instances, HunterModel) and hasattr(instances, '__str__'):
            return json.loads(instances.__str__())

        if isinstance(instances, peewee.CursorWrapper):
            results = list()
            for instance in instances:
                result = OrmModelJsonSerializer.serializer(instance)
                results.append(result)
            return results
