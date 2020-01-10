#!/usr/bin/env bash

#修改rabbitmq配置
HunterCeleryBasePath='/home/hunter/HunterCelery/'
HunterConfigInI=$HunterCeleryBasePath'config/config.ini'
HunterCeleryConfig=$HunterCeleryBasePath'config/celery_config.py'

SqlmapCeleryBasePath='/home/hunter/SqlmapCelery/'
SqlmapConfigInI=$SqlmapCeleryBasePath'config/config.ini'
SqlmapCeleryConfig=$SqlmapCeleryBasePath'config/celery_config.py'

XssEyeCeleryBasePath='/home/hunter/XssEyeCelery/'
XssEyeConfigInI=$XssEyeCeleryBasePath'config/config.ini'
XssEyeCeleryConfig=$XssEyeCeleryBasePath'config/celery_config.py'


modifyRabbitMqConfig(){
    celeryConfig=$1
    number=`cat $celeryConfig | grep "^broker_url" -n | awk -F ":" {'print $1'}` #行号
    sed -i "${number} d" $celeryConfig
    echo "broker_url=\"amqp://$RABBITMQ_USER:$RABBITMQ_PASSWORD@hunter_rabbitmq_host:$RABBITMQ_PORT\"" >> ${celeryConfig} #插入
}
#删除文件指定行
deleteFile(){
    line_number=$1
    file_name=$2
    if [ ! -z $line_number ]; then
        sed -i "${line_number} d" $file_name
    fi
}
#修改mysql配置
modifyMySqlConfig(){
    configInI=$1
    mysql_config_line_number=`cat $configInI | grep "mysql" -n|awk -F ':' {'print $1'}`
    deleteFile $mysql_config_line_number $configInI
    echo "mysql = {\"host\":\"hunter_mysql_host\", \"user\":\"root\", \"password\":\"$MYSQL_ROOT_PASSWORD\", \"port\":"3306", \"database\":\"hunter\", \"max_connections\": 8, \"stale_timeout\":300}" >> ${configInI} #插入
}

modifyRedisConfig(){
    configInI=$1
    redis_config_line_number=`cat $configInI | grep "redis" -n|awk -F ':' {'print $1'}`
    deleteFile $redis_config_line_number $configInI
    echo "redis = {\"host\": \"hunter_redis_host\", \"port\": \"6379\", \"password\": \"$REDIS_PASSWORD\", \"max_connections\": 20}" >> ${configInI}
}
#修改hunter_celery的front_end配置文件
modifyFrontEnd(){
    configInI=$1
    front_end_config_line_number=`cat $configInI | grep "front_end" -n|awk -F ':' {'print $1'}`
    deleteFile $front_end_config_line_number $configInI
    echo "front_end = {\"index\": \"http://$FRONT_END_HOST/taskmanagement\", \"vuln_route\": \"http://$FRONT_END_HOST/scanrecord/\", \"master_checkers_url\": \"http://hunter_admin_api_host:8888/api/v1/admin/checkers/\"}" >> ${configInI} #插入
}


#检查mq账号是否新建成功
checkRabbitMqAuthenticationStatus(){
    while true
    do
        resstatus=`curl -i -u $RABBITMQ_USER:$RABBITMQ_PASSWORD -I -s -w "%{http_code}\n" -o /dev/null http://hunter_rabbitmq_host:$RABBITMQ_API_PORT/api/queues`
        if [ ${resstatus} == 200 ];
            then
                break
        fi
        sleep 5s
    done

}

modifyRabbitMqConfig $HunterCeleryConfig

modifyMySqlConfig $HunterConfigInI
modifyRedisConfig $HunterConfigInI
modifyFrontEnd $HunterConfigInI

modifyRabbitMqConfig $SqlmapCeleryConfig
modifyRedisConfig $SqlmapConfigInI
modifyMySqlConfig $SqlmapConfigInI

modifyRabbitMqConfig $XssEyeCeleryConfig
modifyRedisConfig $XssEyeConfigInI
modifyMySqlConfig $XssEyeConfigInI

checkRabbitMqAuthenticationStatus

#下载

#nohup bash start_consume.sh hunter >> /home/hunter/hunter_celery/nohup.log 2>&1 &
cd ${HunterCeleryBasePath} && nohup bash start_consume.sh hunter >> ${HunterCeleryBasePath}nohup.log 2>&1 &
cd ${SqlmapCeleryBasePath} && nohup bash start_consume.sh sqlmap >> ${SqlmapCeleryBasePath}nohup.log 2>&1 &
cd ${XssEyeCeleryBasePath} && nohup bash start_consume.sh xsseye > ${XssEyeCeleryBasePath}nohup.log 2>&1 &

tail -f /dev/null