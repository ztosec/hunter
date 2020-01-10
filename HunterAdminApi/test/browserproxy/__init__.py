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