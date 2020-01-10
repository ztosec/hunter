#!/ usr/bin/env
# coding=utf-8
"""
author: b5mali4
Copyright (c) 2018

"""

from peewee import *
from .base_model import BaseModel
from .base_model import BaseModelService
from common.sqllite_util import SqliteManage


class User(BaseModel):
    """
    To Create Table:
    >>> if __name__ == "__main__":
    >>>     User.create_table()
    
    ip : 目标IP
    port: 目标端口
    time: 时间
    plugin: 插件名称
    recv_data: 原始请求数据
    time_stamp: 时间戳
    """
    username = TextField(null=True)
    password = TextField(null=True)
    token = TextField(null=True)

    class Meta:
        database = SqliteManage.get_database()


class UserService:
    @staticmethod
    def get_fields_by_where(**kwargs):
        """
        To use:
        >>> users = UserService.get_fields_by_where(fields=(User.username, User.password), where=(User.username == '1222'))
        >>> print(users)
        :param kwargs: 
        :return: 
        """
        return BaseModelService.get_fields_by_where(User, **kwargs)

    @staticmethod
    def remove(**kwargs):
        """
        数据库删除操作
        To use:
        >>> UserService.remove(where=(User.username == "admin"))
        :param kwargs: 
        :return: 
        """
        return BaseModelService.remove(User, **kwargs)

    @staticmethod
    def count(**kwargs):
        """
        数据数量
        To use:
        >>> UserService.count(where=(RequestLog.id == 26))
        :param kwargs: 
        :return: 
        """
        return BaseModelService.count(User, **kwargs)

    @staticmethod
    def save(**kwargs):
        """
        更新操作
        To use:
        >>> UserService.save(username="admin")
        :param kwargs: 
        :return: 
        """
        return BaseModelService.save(User, **kwargs)
