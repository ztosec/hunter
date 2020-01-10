#!/ usr/bin/env
# coding=utf-8
"""
author: b5mali4
Copyright (c) 2018
"""
import unittest
from peewee import *
from common import log
from exception.request_classification_exception import HeaderParseError


class UserModelTestCase(unittest.TestCase):
    def testGetCreateUser(self):
        """
        测试执行SQL
        :return: 
        """
        from model.user import UserService
        import logging
        logger = logging.getLogger('peewee')
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.DEBUG)

        UserService.get_create_user(task_id=1)

    def testGetFieldsByWhere(self):
        """
        
        :return: 
        """
        import logging
        from model.user import UserService
        from model.user import User
        from model.user_task import UserTask
        from model.hunter_model import OrmModelJsonSerializer

        logger = logging.getLogger('peewee')
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.DEBUG)

        user_services = UserService.get_fields_by_where(
            fields=(UserTask.select(fn.COUNT(UserTask.id)).alias('scan_count').where(UserTask.user_id == User.id),
                    User.full_name))

        # print(OrmModelJsonSerializer.serializer(user_service))

    def testGetFieldsByWhere1(self):
        import logging
        from model.user import UserService
        from model.user import User
        from model.user_task import UserTask
        from model.hunter_model import OrmModelJsonSerializer

        logger = logging.getLogger('peewee')
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.DEBUG)

        User.select(User.full_name, UserTask.select(fn.COUNT(UserTask.id)).alias('scan_count').where(
            UserTask.user_id == User.id)).execute()

    def testGetUsersScanCount(self):
        from model.user import UserService
        import logging
        logger = logging.getLogger('peewee')
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.DEBUG)
        UserService.get_users_scan_count()


if __name__ == "__main__":
    unittest.main()
