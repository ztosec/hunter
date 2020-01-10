#!/bin/bash

#Create directory hierarchy.创建目录结构
#touch index.txt serial
#chmod 666 index.txt serial
#echo 01 >  serial
#mkdir -p newcerts private
mkdir crt
#生成RSA密钥对
openssl genrsa -out crt/rootCA.key 4096
#openssl req -x509 -new -nodes -key rootCA.key -sha256 -days 1024 -out rootCA.crt -config req.cnf
#openssl req -x509 -new -nodes -key crt/rootCA.key -sha256 -days 1024 -out crt/rootCA.crt -subj "/C=CN/ST=ZJ/L=HZ/O=Zto, Inc./OU=ZtoSec"
openssl req -x509 -new -nodes -key crt/rootCA.key -sha256 -days 1024 -out crt/rootCA.crt