#!/usr/bin/env bash
#删除正在运行的其他容器，redis,rabbitmq,mysql容器不动，因为里面保存了数据
#是否包含
contains(){
    str=$1
    array=$2
    result=0
    for item in $array; do
        if [ $str == "$item" ]; then #判断字符串是否相等，注意前后要有空格，否则变为赋值语句
            result=1
            break
        fi
    done
    return $result
}
#停止容器
removeContainers(){
    dataContainers=("/hunter-mysql" "/hunter-rabbitmq" "/hunter-redis")
    containers=`docker inspect -f '{{.Name}}' $(docker ps -aq)|grep "hunter"`
    for container in $containers;do
        contains $container "${dataContainers[*]}"
        if [ $? == 0 ];then
            docker stop $container > /dev/null 2>&1
            docker rm $container > /dev/null 2>&1
            echo "删除容器"$container"成功"
        fi
    done
}
#删除镜像
removeImages(){
    dataImages=("bsmali4/hunter-mysql:2.0" "bsmali4/hunter-rabbitmq:2.0" "bsmali4/hunter-redis:2.0")
    images=`docker images|grep "hunter"|awk {'print $1":"$2'}`
    for image in $images;do
        contains $image "${dataImages[*]}"
        if [ $? == 0 ];then
            docker rmi $image > /dev/null 2>&1
            echo "删除镜像"$image"成功"
        fi
    done
}
removeContainers
removeImages