#!/usr/bin/env bash

#检查服务状态
checkServiceStatus(){
    while true
    do
        status=`netstat -nlt|grep 3306|wc -l`
        if [ $status != 0 ];
            then
                break
        else
            bash docker-entrypoint.sh mysqld &
        fi
        sleep 30s
    done
    echo "MySQL started successfully"
}

# 创建外网用户，创建数据库并开启外链
createAccount(){
    USERNAME='root'
    PASSWORD=$MYSQL_ROOT_PASSWORD
    DB_NAME=$DB_NAME
    mysql -u$USERNAME  -p$PASSWORD <<EOF
    CREATE database IF NOT EXISTS hunter DEFAULT CHARSET utf8;
    use mysql;
    GRANT ALL PRIVILEGES ON *.* TO '$USERNAME'@'%' IDENTIFIED BY '$PASSWORD' WITH GRANT OPTION;
    flush privileges;
EOF
}
# 同步数据库结构
migrateStruct(){
    mysql -u$USERNAME  -p$PASSWORD <<EOF
    USE hunter;
    SOURCE /data.sql
EOF
}

echo "step1:检查mysql-server启动状态"
checkServiceStatus
echo "step2:mysql-server成功启动"
echo "step3:开始新建外链账号"
createAccount
echo "step4:新建外链账号成功"
#migrateStruct
echo "step5:需要运行python init_table.py初始化数据库脚本"

# 防止容器退出
tail -f /dev/null