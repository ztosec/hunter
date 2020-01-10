#!/bin/bash
# 签发服务器证书
mkdir crt
openssl genrsa -out crt/mydomain.com.key 2048
openssl req -new -sha256 -key crt/mydomain.com.key -subj "/C=CN/ST=ZJ/L=HZ/O=Zto, Inc./CN=baidu.com" -out crt/mydomain.com.csr
#openssl req -new -out oats.csr -config oats.conf
#openssl req -new -sha256 -key crt/mydomain.com.key -config req.cnf -out crt/mydomain.com.csr
#openssl x509 -req -in crt/mydomain.com.csr -CA crt/rootCA.crt -CAkey crt/rootCA.key -CAcreateserial -out crt/mydomain.com.crt -days 500 -sha256

openssl x509 -req -in crt/mydomain.com.csr -CA crt/rootCA.crt -CAkey crt/rootCA.key -CAcreateserial -out crt/mydomain.com.crt -days 3650 -sha256 -extfile <(cat /etc/ssl/openssl.cnf <(printf "[SAN]\nsubjectAltName=IP:10.211.55.2,DNS.1:10.211.55.2")) -extensions SAN
#nginx -c /usr/local/openresty/nginx/conf/nginx.confs &
#openssl x509 -req -in mydomain.com.csr -CA rootCA.crt -CAkey rootCA.key -CAcreateserial -out mydomain.com.crt -config req.cnf -days 500 -sha256
#openssl req -x509 -in mydomain.com.csr -CA rootCA.crt -CAkey rootCA.key -out mydomain.com.crt -config req.cnf -extensions 'v3_req'  -days 500 -sha256