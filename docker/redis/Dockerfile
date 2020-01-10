ARG IMAGE_BASE="centos"
ARG IMAGE_TAG="7"
FROM ${IMAGE_BASE}:${IMAGE_TAG}
#切换到阿里源
#RUN mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.backup
COPY ./CentOS-Base.repo /etc/yum.repos.d/

RUN yum update -y &&\
    yum install -y gcc curl make unzip gettext git &&\
    yum install vim -y &&\
    yum install wget -y &&\
    yum install net-tools -y

COPY ./redis-4.0.6.tar.gz /usr/local/
RUN cd /usr/local/ \
    && tar -zxvf redis-4.0.6.tar.gz \
    && mv redis-4.0.6 redis \
    && cd redis \
    && make MALLOC=libc \
    && cd src \
    && make install
# 覆盖redis.conf
COPY redis.conf /usr/local/redis/
COPY init-redis.sh /bin/
RUN chmod +x /bin/init-redis.sh
EXPOSE 6379 6379
ENTRYPOINT ["init-redis.sh"]
#CMD [ "redis-server", "/usr/local/redis/redis.conf" ]