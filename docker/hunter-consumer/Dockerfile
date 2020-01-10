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


#RUN wget https://www.python.org/ftp/python/3.6.3/Python-3.6.3.tgz -P /tmp/
COPY Python-3.6.3.tgz /tmp/
RUN cd /tmp/ && tar -zxvf Python-3.6.3.tgz &&\
    cd /tmp/Python-3.6.3 && ./configure --with-ssl && make && make install

RUN mkdir -p /home/hunter/HunterCelery &&\
    mkdir -p /home/hunter/SqlmapCelery &&\
    mkdir -p /home/hunter/XssEyeCelery

COPY requirements.txt /tmp/

RUN pip3 install -r /tmp/requirements.txt --timeout 3000

#安装中文支持
RUN yum -y install kde-l10n-Chinese telnet && \
    yum -y reinstall glibc-common &&\
    yum clean all  &&\
    localedef -c -f UTF-8 -i zh_CN zh_CN.utf8

ENV LANG=zh_CN.UTF-8 \
    LANGUAGE=zh_CN:zh \
    LC_ALL=zh_CN.UTF-8

RUN yum -y install epel-release && yum install python-pip -y


COPY SqlmapCelery.tar.gz /tmp/

RUN tar -zxvf /tmp/SqlmapCelery.tar.gz -C /home/hunter/ &&\
    cd /home/hunter/SqlmapCelery/ &&\
    pip2 install -r requirements.txt

COPY XssEyeCelery.tar.gz /tmp/

COPY xsseye_celery_requirements.txt /tmp/

RUN cd /tmp/ && pip3 install -r xsseye_celery_requirements.txt

COPY download_chromium.py /tmp/

RUN yum install libX11-xcb pango libXcomposite libXcursor libXdamage libXext libXi libXtst cups-libs libXScrnSaver libXrandr GConf2 alsa-lib atk gtk3 nss -y
RUN cd /tmp/ && python3 download_chromium.py
#下载chromium

RUN tar -zxvf /tmp/XssEyeCelery.tar.gz -C /home/hunter/

COPY HunterCelery.tar.gz /tmp/
RUN tar -zxvf /tmp/HunterCelery.tar.gz -C /home/hunter/ && cd /home/hunter/HunterCelery

COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
#RUN chmod +x /usr/local/bin/docker-entrypoint.sh

#ENTRYPOINT ["docker-entrypoint.sh"]
WORKDIR /home/hunter/