#!/usr/bin/env bash
# 更换成阿里源
cd /etc/yum.repos.d && mv CentOS-Base.repo CentOS-Base.repo.bak \
&& wget http://mirrors.aliyun.com/repo/Centos-7.repo \
&& mv Centos-7.repo CentOS-Base.repo \
&& yum clean all \
&& yum makecache \
&& yum update -y

# 安装python3和pip
# RUN yum install update -y
yum install wget -y && yum install gcc -y && mkdir -p /home/app

yum update -y && yum reinstall -y glibc-common
yum install -y telnet net-tools
yum -y install zlib*
yum install zlib-devel bzip2-devel pcre-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel -y

yum install epel-release -y
yum install https://centos7.iuscommunity.org/ius-release.rpm -y
wget -P tmp/ https://www.python.org/ftp/python/3.6.9/Python-3.6.9.tgz \
cd tmp/
tar -zxvf Python-3.6.9.tgz
cd Python-3.6.9
./configure --with-ssl
make && make install

# 安装uwsgi
pip3 install uwsgi --timeout 600
# 安装nginx
mkdir -p /var/log/nginx/
cd tmp/
wget http://nginx.org/download/nginx-1.11.6.tar.gz
tar -zxvf nginx-1.11.6.tar.gz
cd nginx-1.11.6
./configure
make && make install
#/usr/local/nginx/sbin/nginx -c /usr/local/nginx/conf/nginx.conf
#rpm -ivh http://nginx.org/packages/centos/7/noarch/RPMS/nginx-release-centos-7-0.el7.ngx.noarch.rpm
#http://nginx.org/packages/rhel/7/x86_64/RPMS/nginx-1.16.0-1.el7.ngx.x86_64.rpm
#yum install nginx -y
# 安装supervisor
pip3 install supervisor
yum install net-tools -y && yum install vim -y
# 复制源码
cp ./DnsSocketLog.tar.gz /home/app/
cp ./uwsgi.ini /home/app/uwsgi.ini
cp ./supervisor.conf /home/app/supervisor.conf
cp ./nginx.conf /usr/local/nginx/conf/nginx.conf
cp ./docker-entrypoint.sh /usr/local/bin/
cp ./20-nproc.conf /etc/security/limits.d/
cd /home/app/ && tar -xvf DnsSocketLog.tar.gz && mkdir -p /usr/share/nginx/logs/
cd /home/app/ && pip3 install -r requirements.txt --timeout 3000
# 复制entrypoint
chmod +x /usr/local/bin/docker-entrypoint.sh

cd /home/app/ && docker-entrypoint.sh admin admin888 hunter-log-token