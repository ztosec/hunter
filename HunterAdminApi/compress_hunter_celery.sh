#!/usr/bin/env bash

hunterCeleryTemp='HunterCelery/'
initHunterCeleryTempFolder(){
    if [ -d $hunterCeleryTemp ];then
            echo "文件夹"$hunterCeleryTemp"存在,将删除创建新文件夹"
            rm -rf $hunterCeleryTemp
        else
            echo "文件夹"$hunterCeleryTemp"不存在,将直接创建新文件夹"
        fi
        mkdir -p $hunterCeleryTemp
        echo "文件夹"$hunterCeleryTemp"创建成功"
}

#新建临时配置文件
createHunterCeleryTemp(){
    initHunterCeleryTempFolder
    folders=("plugins/" "taskschedule/" "config/" "common/" "exception/" "model/" "parser/" "notice/" "hunter_celery.py" "plugin_requirements.txt" "api/service/")

    for folder in ${folders[*]}; do
        if [[ $(echo $folder | grep "/") != "" ]]; then
            mkdir -p $hunterCeleryTemp""$folder
        fi
        cp -r $folder $hunterCeleryTemp""$folder
    done
    mv $hunterCeleryTemp"plugin_requirements.txt" $hunterCeleryTemp"requirements.txt"
    mkdir -p $hunterCeleryTemp"logs"
    #拷贝
    cp -r "start_consume.sh" $hunterCeleryTemp"start_consume.sh"
    cp -r $hunterCeleryTemp"requirements.txt" ../docker/hunter-consumer/requirements.txt
}

#mac用户安装gnu-sed
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
createHunterCeleryTemp
tar -zcvf HunterCelery.tar.gz --exclude=__pycache__/* --exclude=*.git --exclude=*.DS_Store ${hunterCeleryTemp}