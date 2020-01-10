#!/usr/bin/env bash
if [$# != 1 ];then
    echo "warnning:请传递一个参数,作为redis密码"
    exit
fi
redisPassword="requirepass "$1
echo "setp1:修改redis配置文件密码"
sed -i "s/# requirepass foobared/$redisPassword/g" /usr/local/redis/redis.conf
echo "setp2:启动redis"
# 启动redis
/usr/local/redis/src/redis-server /usr/local/redis/redis.conf
# 检测是否启动
echo "setp3:检查redis-server启动状态"
while true
do
    status=`netstat -nlt|grep 6379|wc -l`
    if [ $status != 0 ];
        then
            break
    fi
done
echo "setp4:redis-server成功启动"
tail -f /dev/null