#!/usr/bin/env bash
# sqlmap中加入Celery参数和保存结果补丁
until [ $# -eq 0 ]
do
  name=${1:1}; shift;
  if [[ -z "$1" || $1 == -* ]] ; then eval "export $name=true"; else eval "export $name=$1"; shift; fi
done

actionTypes=("install")

checkActionTypes(){
    result=0
    for actionType in ${actionTypes[*]}; do
        if [ "$actionType" == "$action" ]; then
            result=1
        fi
    done
    return $result
}
#删除文件指定行
deleteFile(){
    line_number=$1
    file_name=$2
    os=`uname -a | awk {'print $1'}`
    if [ "$os" == "Darwin" ];then
        gsed -i "${line_number} d" $file_name
    elif [ "$os" == "Linux" ];then
        sed -i "${line_number} d" $file_name
    fi
}
#将指定行替换成空
clearFile(){
    line_number=$1
    file_name=$2
    os=`uname -a | awk {'print $1'}`
    if [ "$os" == "Darwin" ];then
        gsed -i "${line_number}c \ " $file_name
    elif [ "$os" == "Linux" ];then
        sed -i "${line_number}c \ " $file_name
    fi
}
#替换某一行
replaceFile(){
    line_number=$1
    file_name=$2
    new_str=$3
    os=`uname -a | awk {'print $1'}`
    if [ "$os" == "Darwin" ];then
        gsed -i "${line_number}c ${new_str}" $file_name
    elif [ "$os" == "Linux" ];then
        sed -i "${line_number}c ${new_str}" $file_name
    fi
}
#新增某一行之前
insertFile(){
    line_number=$1
    file_name=$2
    new_str=$3
    os=`uname -a | awk {'print $1'}`
    if [ "$os" == "Darwin" ];then
        gsed -i "${line_number}i ${new_str}" $file_name
    elif [ "$os" == "Linux" ];then
        sed -i "${line_number}i ${new_str}" $file_name
    fi
}

#安装补丁文件到 sqlmap/lib/parse/cmdline.py
installPatch2cmdline(){
    filePath="sqlmap/lib/parse/cmdline.py"
    if [ `grep -c "celery" ${filePath}` -eq '0' ]; then
        nextLineNum=`cat ${filePath}| grep 'parser.*("--hh"' -n|awk -F ":" {'print $1'}|head -n 1`
        insertFile $nextLineNum $filePath "\        parser.add_option(\"--celery\", dest=\"celery\", help=\"celery_id\")"
        echo "${filePath}安装过的补丁成功"
    else
        echo "${filePath}已经存在安装过的补丁，将跳过安装"
    fi
}

installPatch2controller(){
    filePath="sqlmap/lib/controller/controller.py"
    if [ `grep -c "# coding=utf-8" ${filePath}` -eq '0' ]; then
        insertFile 2 $filePath "# coding=utf-8"
    fi

    #文件尾部插入save_vulnerability
    if [ `grep -c "def save_vulnerability" ${filePath}` -eq '0' ]; then
        cat >>${filePath}<< EOF


def save_vulnerability(payload, task_id, url):
    """
    save to mysql
    :param payload:
    :param task_id:
    :param url:
    :return:
    """
    import os
    import sys

    try:
        from model.vulnerability import Vulnerability,VulnerabilityService
    except ImportError:
        SQLMAP_CELERY_PATH = os.path.normpath("{}/../../../".format(os.path.dirname(os.path.abspath(__file__))))
        sys.path.insert(0, SQLMAP_CELERY_PATH)
        from model.vulnerability import Vulnerability, VulnerabilityService

    if task_id is None:
        return
    # 保存漏洞到数据库
    sql_type = {'fullname': 'sql_inject', 'fullchinesename': 'sql注入', 'level': 'high'}
    info = "{}存在一个sql注入漏洞".format(url)
    imp_version = "所有版本"
    repair = "过滤掉sql恶意字符"
    type = sql_type["fullname"]
    chinese_type = sql_type["fullchinesename"]
    description = "Sql 注入攻击是通过将恶意的 Sql 查询或添加语句插入到应用的输入参数中，再在后台 Sql 服务器上解析执行进行的攻击，它目前黑客对数据库进行攻击的最常用手段之一。参考连接http://wiki.dev.ztosys.com/pages/viewpage.action?pageId=21741806"
    level = sql_type["level"]
    VulnerabilityService.save(info=info, payload=payload, imp_version=imp_version, repair=repair, type=type, chinese_type=chinese_type, description=description, level=level, task_id=task_id)

EOF

        targetFuncLineNum=`cat ${filePath}| grep 'def _showInjections' -n|awk -F ":" {'print $1'}`
        found=0
        for func_line in `cat sqlmap/lib/controller/controller.py| grep 'def' -n|awk -F ":" {'print $1'}`;do
            if [ $found -eq 1 ];then
                insertFile $func_line $filePath "\    if\ conf.celery:\n\        save_vulnerability(data, conf.celery, conf.url)\n\n"
                found=0
            fi
            if [ "$func_line" -eq "$targetFuncLineNum" ]; then
                found=1
            fi
        done
        echo "${filePath}安装过的补丁成功"
    else
        echo "${filePath}已经存在安装过的补丁，将跳过安装"
    fi


}

checkActionTypes

if [ $? == 1 ];then
    if [ "$action"=="install" ]; then
        installPatch2cmdline
        installPatch2controller
    fi
else
    echo "请选择操作类型,安装SqlmapCelery补丁"
    echo "执行 bash "$0 "-action install 表示在sqlmap中安装SqlmapCelery补丁"
    exit
fi