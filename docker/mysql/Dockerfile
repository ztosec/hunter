#see https://github.com/docker-library/mysql/blob/696fc899126ae00771b5d87bdadae836e704ae7d/5.7/docker-entrypoint.sh
ARG IMAGE_BASE="mysql"
ARG IMAGE_TAG="5.7.28"
FROM ${IMAGE_BASE}:${IMAGE_TAG}
LABEL maintainer="b5mali4 <root@codersec.net>"

COPY init-mysql.sh /usr/local/bin/
#更换源
RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list
# 安装基本的工具
RUN apt-get update -y && apt-get install procps -y && apt-get install vim -y && apt-get install net-tools -y && apt-get install curl -y && apt-get install wget -y && chmod +x /usr/local/bin/init-mysql.sh
EXPOSE 3306 3306