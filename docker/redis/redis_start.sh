#!/usr/bin/env bash
# 存放session，hookRule等
docker run --name redis -it -e ALLOW_EMPTY_PASSWORD=yes -p 6379:6379 centos/redis-32-centos7 bin/bash
#修改 /etc/redis.conf 中的bind 127.0.0.1为 bind 0.0.0.0