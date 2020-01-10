#!/usr/bin/env bash
#修改rabbitmq配置
basePath='/home/hunter/HunterAdminApi/'
configInI=$basePath'config/config.ini'
celeryConfig=$basePath'config/celery_config.py'
modifyRabbitMqConfig(){
    number=`cat $celeryConfig | grep "^broker_url" -n | awk -F ":" {'print $1'}` #行号
    sed -i "${number} d" $celeryConfig
    echo "broker_url=\"amqp://$RABBITMQ_USER:$RABBITMQ_PASSWORD@hunter_rabbitmq_host:$RABBITMQ_PORT\"" >> ${celeryConfig} #插入
}
#删除文件指定行
deleteFile(){
    line_number=$1
    file_name=$2
    sed -i "${line_number} d" $file_name
}
#修改mysql配置
modifyMySqlConfig(){
    mysql_config_line_number=`cat $configInI | grep "mysql" -n|awk -F ':' {'print $1'}`
    deleteFile $mysql_config_line_number $configInI
    echo "mysql = {\"host\":\"hunter_mysql_host\", \"user\":\"root\", \"password\":\"$MYSQL_ROOT_PASSWORD\", \"port\":"3306", \"database\":\"hunter\", \"max_connections\": 8, \"stale_timeout\":300}" >> ${configInI} #插入
}

modifyRedisConfig(){
    mysql_config_line_number=`cat $configInI | grep "redis" -n|awk -F ':' {'print $1'}`
    deleteFile $mysql_config_line_number $configInI
    echo "redis = {\"host\": \"hunter_redis_host\", \"port\": \"6379\", \"password\": \"$REDIS_PASSWORD\", \"max_connections\": 20}" >> ${configInI} #插入
}

modifyFrontEndConfig(){
    mysql_config_line_number=`cat $configInI | grep "front_end" -n|awk -F ':' {'print $1'}`
    deleteFile $mysql_config_line_number $configInI
    echo "front_end = {\"index\": \"$INDEX_URL\", \"vuln_route\": \"$VULN_ROUTE\"}" >> ${configInI} #插入
}
#初始化数据
initializeData(){
    while true
    do
        if [ `python3 $basePath/init_tables.py |grep "success"|wc -l` == 1 ]; then
            echo "初始化数据库成功"
            break
        fi
        echo "初始化数据库失败,5秒后自动重试"
        sleep 5
    done
}
echo "setp1:修改rabbitmq配置文件"
modifyRabbitMqConfig
echo "setp2:修改mysql配置文件"
modifyMySqlConfig
echo "setp3:修改redis配置文件"
modifyRedisConfig
modifyFrontEndConfig
echo "setp4:初始化数据库中数据"
initializeData
echo "setp5:启动restful api服务"
nohup python3 $basePath/web_app.py >> $basePath/web_app.log 2>&1 &
echo "setp6:启动网络代理服务"
nohup python3 $basePath/networkproxy/proxy_server.py  >> $basePath/networkproxy/proxy_server.log 2>&1 &
tail -f /dev/null