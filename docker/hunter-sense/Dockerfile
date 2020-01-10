ARG RESTY_IMAGE_BASE="centos"
ARG RESTY_IMAGE_TAG="7"
FROM ${RESTY_IMAGE_BASE}:${RESTY_IMAGE_TAG}
LABEL maintainer="b5mali4 <root@codersec.net>"

# 安装python3和pip
# RUN yum install update -y
RUN yum install wget -y \
    && yum install gcc -y \
    && mkdir -p /home/app
# 更换成阿里源
RUN cd /etc/yum.repos.d \
    && mv CentOS-Base.repo CentOS-Base.repo.bak \
    && wget http://mirrors.aliyun.com/repo/Centos-7.repo \
    && mv Centos-7.repo CentOS-Base.repo \
    && yum clean all \
    && yum makecache \
    && yum update -y
# 安装支持中文
ENV LANG=zh_CN.UTF-8 \
    LANGUAGE=zh_CN:zh \
    LC_ALL=zh_CN.UTF-8
RUN yum update -y && \
    yum reinstall -y glibc-common && \
    yum install -y telnet net-tools && \
    yum clean all && \
    rm -rf /tmp/* rm -rf /var/cache/yum/* && \
    localedef -c -f UTF-8 -i zh_CN zh_CN.UTF-8 && \
    ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

#RUN wget -P tmp/ https://www.python.org/ftp/python/3.6.9/Python-3.6.9.tgz \
#    && cd tmp/ \
#    && tar -zxvf Python-3.6.9.tgz \
#    && cd Python-3.6.9 \
#    && ./configure --with-ssl \
#    && make \
#    && make install

RUN yum install epel-release -y \
    && yum install https://centos7.iuscommunity.org/ius-release.rpm -y \
    && yum install python36u-devel.x86_64 -y

RUN cd tmp/ \
    && curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py \
    && python3 get-pip.py
# 安装uwsgi
RUN pip3 install uwsgi --timeout 600
# 安装nginx
RUN yum install nginx -y
# 安装supervisor
RUN pip3 install supervisor
RUN yum install net-tools -y && yum install vim -y
# 复制源码
COPY ./HunterSense.tar.gz /home/app/
RUN cd /home/app/ && tar -xvf HunterSense.tar.gz && mkdir -p /usr/share/nginx/logs/
RUN cd /home/app/ && pip3 install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple --timeout 3000
COPY ./uwsgi.ini /home/app/uwsgi.ini
COPY ./supervisor.conf /home/app/supervisor.conf
COPY ./nginx.conf /etc/nginx/nginx.conf
# 复制entrypoint
COPY ./docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

COPY ./20-nproc.conf /etc/security/limits.d/
ENTRYPOINT ["docker-entrypoint.sh"]
WORKDIR /home/app
EXPOSE 80 80
#CMD ["admin", "admin", "token"]
# 执行NGINX
#RUN nginx -c /etc/nginx/nginx.conf
# uwsgi --ini /home/app/uwsgi.ini
# docker run --rm -p 8843:80 --name hunter-log -it hunter-log:v2.5.1 bin/bash
# docker run -d -p 8843:80 --name hunter-log hunter-log:v2.5.1
# supervisord -c /home/app/supervisord.conf