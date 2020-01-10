#!/usr/bin/env bash
if [ $# != 2 ];then
    echo "warnning:请传递两个参数,分别为账号和密码"
    exit
fi
username=$1
password=$2

# 启动rabbitmq
rabbitmq-server --detached & ps aux |grep rabbitmq

checkRabbitmqStatus(){
    while true
    do
        resstatus=`curl -I -s -w "%{http_code}\n" -o /dev/null http://127.0.0.1:15672`
        if [ ${resstatus} == 200 ];
            then
                break
        fi
        sleep 5s
    done
}

# 创建exchange
createExchange(){
    exchangeName=$1
    curl -i -u $username:$password -H "content-type:application/json" -XPUT -d'{"vhost":"/","name":"$exchangeName","type":"fanout","durable":"true","auto_delete":"false","internal":"false","arguments":{}}' http://localhost:15672/api/exchanges/%2F/$exchangeName
}

# 创建queue
createQueue(){
    queueName=$1
    data='{"vhost":"/","name":"hunter","durable":"true","auto_delete":"false","arguments":{}}'
    curl -i -u $username:$password -H "content-type:application/json" -XPUT -d$data http://localhost:15672/api/queues/%2F/$queueName
}
# 绑定queue
bindExchange2Queue(){
    exchangeName=$1
    queueName=$2
    routingKey=$3
    data='{"vhost":"/","destination":"$queueName","destination_type":"q","source":"$exchangeName","routing_key":"$routingKey","arguments":{}}'
    curl -i -u $username:$password -H "content-type:application/json" -XPOST -d$data http://localhost:15672/api/bindings/%2F/e/$exchangeName/q/$queueName
}

echo "step1:检查rabbitmq-server启动状态"
checkRabbitmqStatus
echo "step2:rabbitmq-server成功启动"

echo "step3:rabbitmq-server添加管理员账号"
# 添加管理员账号
rabbitmqctl add_user $username $password
rabbitmqctl set_user_tags admin administrator monitoring policymaker management
echo "step4:rabbitmq-server设置用户权限"
# 设置用户权限
rabbitmqctl  set_permissions  -p  /  admin  '.*'  '.*'  '.*'
# 开启stomp插件
# rabbitmq-plugins enable rabbitmq_web_stomp
# rabbitmq-plugins enable rabbitmq_web_stomp_examples
echo "step5:rabbitmq-server启动stomp插件"
# 进入容器之后启动stomp协议
rabbitmq-plugins enable rabbitmq_web_stomp rabbitmq_stomp rabbitmq_web_stomp_examples
# 开启remove消息插件
rabbitmq-plugins enable rabbitmq_shovel rabbitmq_shovel_management

checkRabbitmqStatus
echo "step6:创建exchange"
#createExchange 'hunter_broadcast_tasks'
createExchange 'hunter_task_notice'
createExchange 'hunter_raw_traffic'
#新建立exchange和queue,并绑定 see rabbitmqctl
#curl -i -u admin:admin -H "content-type:application/json" -XPUT -d'{"vhost":"/","name":"hunter_broadcast_tasks","type":"fanout","durable":"true","auto_delete":"false","internal":"false","arguments":{}}' http://localhost:15672/api/exchanges/%2F/hunter_broadcast_tasks
#echo "创建queue"
# 创建queue
echo "step7:创建QUEUE"
createQueue 'hunter'
createQueue 'xsseye'
createQueue 'sqlmap'
createQueue 'task'
echo "step8:绑定QUEUE"
bindExchange2Queue 'hunter_raw_traffic' 'hunter' 'hunter'
bindExchange2Queue 'hunter_raw_traffic' 'xsseye' 'hunter'
bindExchange2Queue 'hunter_raw_traffic' 'sqlmap' 'hunter'
bindExchange2Queue 'hunter_task_notice' 'task' 'task'
#curl -i -u admin:admin -H "content-type:application/json" -XPUT -d'{"vhost":"/","name":"hunter","durable":"true","auto_delete":"false","arguments":{}}' http://localhost:15672/api/queues/%2F/hunter
#curl -i -u admin:admin -H "content-type:application/json" -XPUT -d'{"vhost":"/","name":"hunter","durable":"true","auto_delete":"false","arguments":{}}' http://localhost:15672/api/queues/%2F/xssfork
#curl -i -u admin:admin -H "content-type:application/json" -XPUT -d'{"vhost":"/","name":"hunter","durable":"true","auto_delete":"false","arguments":{}}' http://localhost:15672/api/queues/%2F/sqlmap
# 绑定queue
#curl -i -u admin:admin -H "content-type:application/json" -XPOST -d'{"vhost":"/","destination":"hunter","destination_type":"q","source":"hunter_broadcast_tasks","routing_key":"hunter_broadcast_tasks","arguments":{}}' http://localhost:15672/api/bindings/%2F/e/hunter_broadcast_tasks/q/hunter
#curl -i -u admin:admin -H "content-type:application/json" -XPOST -d'{"vhost":"/","destination":"xssfork","destination_type":"q","source":"hunter_broadcast_tasks","routing_key":"hunter_broadcast_tasks","arguments":{}}' http://localhost:15672/api/bindings/%2F/e/hunter_broadcast_tasks/q/xssfork
#curl -i -u admin:admin -H "content-type:application/json" -XPOST -d'{"vhost":"/","destination":"sqlmap","destination_type":"q","source":"hunter_broadcast_tasks","routing_key":"hunter_broadcast_tasks","arguments":{}}' http://localhost:15672/api/bindings/%2F/e/hunter_broadcast_tasks/q/sqlmap

# 防止容器退出
tail -f /dev/null