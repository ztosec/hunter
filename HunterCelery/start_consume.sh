#!/usr/bin/env bash
#opensource
#brew install gnu-sed
consumerQueue=$1
taskQueues=("hunter" "sqlmap" "xsseye")
osType=`uname -a | awk {'print $1'}`
if [ $# != 1 ];then
    echo "请传入参数指定要消费的队列，例如bash start_consume.sh hunter,sqlmap,xsseye"
    echo "消费的队列主要分为hunter,sqlmap,xsseye"
    exit
fi

checkConsumerQueue(){
    result=0
    for taskQueue in ${taskQueues[*]}; do
        if [ "$taskQueue" == "$consumerQueue" ]; then
            result=1
        fi
    done
    return $result
}

modifyCeleryConfig(){
    task_queues_line_number=`cat config/celery_config.py | grep "task_queues" -n|awk -F ':' {'print $1'}`
    queue_line_number=$[task_queues_line_number+1]
    queue_name=`sed -n "${queue_line_number}p" config/celery_config.py`

    if [ "$osType" == "Darwin" ];then
        gsedOrset=gsed
    elif [ "$osType" == "Linux" ];then
        gsedOrset=sed
    fi

    is_exist=$(echo $queue_name | grep "Queue")
    if [[ "$is_exist" != "" ]]; then
        echo "存在队列名，将修改原有队列名"
        $gsedOrset -i "${queue_line_number}c Queue('${consumerQueue}', Exchange('hunter_raw_traffic', type='fanout'), routing_key='hunter')," config/celery_config.py
    else
        echo "不存在队列名,将自动增加队列名"
        $gsedOrset -i "${task_queues_line_number}a Queue('${consumerQueue}', Exchange('hunter_raw_traffic', type='fanout'), routing_key='hunter')," config/celery_config.py
    fi
}

installSed(){
    if [ "$osType" == "Darwin" ];then
        gsed > /dev/null 2>&1
        if [  $? == 0 ]; then
            echo "Darwin need install gnu-sed"
            brew install gnu-sed
        fi
    fi
}

installSed
checkConsumerQueue

if [ $? == 1 ];then
    modifyCeleryConfig
else
    echo "指定非法队列名称,只能指定${taskQueues[*]}中任意一种"
    exit
fi

python3 hunter_celery.py -A hunter_celery worker -l info -c 1