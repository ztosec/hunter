ARG IMAGE_BASE="centos"
ARG IMAGE_TAG="7"
FROM ${IMAGE_BASE}:${IMAGE_TAG}

RUN yum update -y &&\
    yum install -y gcc curl make unzip gettext git &&\
    yum install vim -y &&\
    yum install wget -y &&\
    yum install net-tools -y &&\
    mkdir -p /home/hunter/ && \
    yum install zlib zlib-devel -y &&\
    yum install openssl-devel -y

RUN cd /etc/yum.repos.d \
    && mv CentOS-Base.repo CentOS-Base.repo.bak \
    && wget http://mirrors.aliyun.com/repo/Centos-7.repo \
    && mv Centos-7.repo CentOS-Base.repo \
    && yum clean all \
    && yum makecache \
    && yum update -y

#安装中文支持
RUN yum -y install kde-l10n-Chinese telnet && \
    yum -y reinstall glibc-common &&\
    yum clean all  &&\
    localedef -c -f UTF-8 -i zh_CN zh_CN.utf8

ENV LANG=zh_CN.UTF-8 \
    LANGUAGE=zh_CN:zh \
    LC_ALL=zh_CN.UTF-8

RUN cd / && wget https://npm.taobao.org/mirrors/node/v10.13.0/node-v10.13.0-linux-x64.tar.xz

RUN cd / && tar -xf node-v10.13.0-linux-x64.tar.xz &&\
    ln -s /node-v10.13.0-linux-x64/bin/node /usr/bin/node &&\
    ln -s /node-v10.13.0-linux-x64/bin/npm /usr/bin/npm

RUN mkdir -p /home/hunter/HunterAdminGui/
COPY package.json /home/hunter/HunterAdminGui/

RUN cd /home/hunter/HunterAdminGui &&\
    npm config set registry http://registry.npm.taobao.org &&\
    npm install

RUN rpm -Uvh http://nginx.org/packages/centos/7/noarch/RPMS/nginx-release-centos-7-0.el7.ngx.noarch.rpm &&\
    yum install nginx -y

COPY HunterAdminGui.tar.gz /home/hunter/
COPY HunterDoc.tar.gz /home/hunter/

COPY nginx.conf /etc/nginx/nginx.conf

RUN tar -zxvf /home/hunter/HunterAdminGui.tar.gz -C /home/hunter/HunterAdminGui/

RUN mkdir -p /home/hunter/HunterDoc/ && tar -zxvf /home/hunter/HunterDoc.tar.gz -C /home/hunter/HunterDoc/

COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

WORKDIR /home/hunter/HunterAdminGui/