#!/usr/bin/env bash
until [ $# -eq 0 ]
do
  name=${1:1}; shift;
  if [[ -z "$1" || $1 == -* ]] ; then eval "export $name=true"; else eval "export $name=$1"; shift; fi
done
basePath='/home/hunter/HunterAdminGui/'
#修改rabbitmq配置
modifyBackEndUrl(){
    back_end_url_num=`cat ${basePath}src/utils/request.js | grep "const host" -n|awk -F ':' {'print $1'}`
    os=`uname -a | awk {'print $1'}`
    if [ "$os" == "Darwin" ];then
        gsed -i "${back_end_url_num}c const host = \"${back_end_url}\";" ${basePath}src/utils/request.js
    elif [ "$os" == "Linux" ];then
        sed -i "${back_end_url_num}c const host = \"${back_end_url}\";" ${basePath}src/utils/request.js
    fi
}
#启动nginx
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
modifyBackEndUrl
if [ $build == "true" ]; then
    npm run build
fi
start_nginx
tail -f /dev/null