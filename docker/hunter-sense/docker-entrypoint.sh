#!/usr/bin/env bash
if [ $# != 3 ];then
    echo "请传入参数指定初始化账号,密码和token"
    exit
fi

username=$1
password=$2
token=$3


start_nginx(){
    run_nginx=`/usr/sbin/nginx -c /etc/nginx/nginx.conf`
    #/usr/local/nginx/sbin/nginx -c /usr/local/nginx/conf/nginx.conf
    while true
    do
        status=`curl -I -m 10 -o /dev/null -s -w %{http_code} http://127.0.0.1`
        if [ $status == 200 ];
            then
                break
        fi
        sleep 5s
    done
    echo "nginx启动成功"

}

start_supervisord(){
    supervisord -c /home/app/supervisor.conf
    while true
    do
        ps -fe|grep "supervisord" |grep -v grep
        if [ $? -ne 0 ]; then
            echo "supervisord启动中...."
        else
            echo "supervisord启动成功"
            break
        fi
        sleep 5s
    done
}

python3 /home/app/init_db.py $username $password $token
echo "初始化账号密码成功"
start_nginx
start_supervisord
tail -f /dev/null