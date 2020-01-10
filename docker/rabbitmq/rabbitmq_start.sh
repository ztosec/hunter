#!/usr/bin/env bash
docker run -it -p 5671:5671 -p 5672:5672 -p 4369:4369 -p 25672:25672 -p 15674:15674 -p 15670:15670 -p 15671:15671 -p 15672:15672 -p 61613:61613 rabbitmq:management bin/bash
# 进入容器之后执行
# rabbitmq-plugins enable rabbitmq_stomp
# ./docker-entrypoint.sh rabbitmq-server
# 添加管理员账号
# rabbitmqctl add_user admin admin
# rabbitmqctl set_user_tags admin administrator monitoring policymaker management
# 设置用户权限
# rabbitmqctl  set_permissions  -p  /  admin  '.*'  '.*'  '.*'
# 开启stomp插件
# rabbitmq-plugins enable rabbitmq_web_stomp
# rabbitmq-plugins enable rabbitmq_web_stomp_examples