#!/ usr/bin/env
# coding=utf-8
"""
author: b5mali4
Copyright (c) 2018
License: BSD, see LICENSE for more details.
To use:
>>> sq = Square(3)
>>> sq.area
9
Simple Postgres pool example code:

    # Use the special postgresql extensions.
    from playhouse.pool import PooledPostgresqlExtDatabase

    db = PooledPostgresqlExtDatabase(
        'my_app',
        max_connections=32,
        stale_timeout=300,  # 5 minutes.
        user='postgres')

    class BaseModel(Model):
        class Meta:
            database = db
"""
import unittest
import hashlib
import random
import string


class TaskModelTestCase(unittest.TestCase):
    def testGetTasksUrlNum(self):
        """
        测试执行SQL
        :return: 
        """

    def testGenerateSession(self):
        """
        随机生成SESSION
        :return: 
        """
        random_byte = ''.join(random.sample(string.ascii_letters + string.digits + string.punctuation, 32))
        m = hashlib.md5()
        m.update(random_byte.encode("utf-8"))
        md5 = m.hexdigest()
        print(md5)


if __name__ == "__main__":
    unittest.main()
