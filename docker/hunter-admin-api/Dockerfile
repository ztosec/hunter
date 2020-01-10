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

#RUN wget https://www.python.org/ftp/python/3.6.3/Python-3.6.3.tgz -P /tmp/  &&\
#    cd /tmp/ && tar -zxvf Python-3.6.3.tgz &&\
#    cd /tmp/Python-3.6.3 && ./configure --with-ssl && make && make install

RUN yum install epel-release -y \
    && yum install https://centos7.iuscommunity.org/ius-release.rpm -y \
    && yum install python36u-devel.x86_64 -y

RUN cd tmp/ \
    && curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py \
    && python3 get-pip.py
#see https://www.jianshu.com/p/a337acb40453
RUN rpm -e --nodeps  `rpm -q curl` &&\
    wget https://curl.haxx.se/download/curl-7.43.0.tar.gz -P /tmp/ &&\
    cd /tmp/ && tar -zxf /tmp/curl-7.43.0.tar.gz && cd /tmp/curl-7.43.0 && ./configure && make && make install &&\
    ln -s /usr/local/bin/curl /usr/bin/curl &&\
    yum install openldap-devel -y

COPY uplibcurl.sh /tmp/

RUN bash /tmp/uplibcurl.sh

RUN pip install --no-cache-dir --compile --ignore-installed --install-option="--with-nss" pycurl

COPY requirements.txt /tmp/

RUN pip3 install -r /tmp/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

#安装nginx和supervisor
#RUN rpm -Uvh http://nginx.org/packages/centos/7/noarch/RPMS/nginx-release-centos-7-0.el7.ngx.noarch.rpm &&\
#    yum install nginx -y &&\
#    pip3 install supervisor &&\
#    pip3 install uwsgi

#安装中文支持
RUN yum -y install kde-l10n-Chinese telnet && \
    yum -y reinstall glibc-common &&\
    yum clean all  &&\
    localedef -c -f UTF-8 -i zh_CN zh_CN.utf8

ENV LANG=zh_CN.UTF-8 \
    LANGUAGE=zh_CN:zh \
    LC_ALL=zh_CN.UTF-8

COPY HunterAdminApi.tar.gz /tmp/

RUN tar -zxvf /tmp/HunterAdminApi.tar.gz -C /home/hunter/ && cd /home/hunter/HunterAdminApi/

COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh
#ENTRYPOINT ["docker-entrypoint.sh"]
WORKDIR /home/hunter/HunterAdminApi/
