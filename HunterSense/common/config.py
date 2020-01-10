#!/ usr/bin/env
# coding=utf-8
#
# Copyright 2019 ztosec & https://www.zto.com/
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
"""
author: b5mali4
"""
# 日志存储路径
LOG_PATH = "app.log"

# socket服务器默认的响应，伪装nginx服务器，不调用则不使用
SOCKET_RESPONSE_CONTENT = '<html><head><title>502 Bad Gateway</title></head><body bgcolor="white"><center><h1>' \
                          '502 BadGateway</h1></center><hr><center>nginx</center></body></html>'

ENCODE_TYPE = "utf-8"

# ～～～保存数据库详情～～～

# 数据库路径
DB_PATH = "app.sqlite3"

# 连接池最大连接数
MAX_CONNECTIONS = 30

STALE_TIMEOUT = 300

# ～～～SOCKET相关配置 ～～～

# 监听端口
SERVER_SOCKET_PORT = 7799

# ～～～DNSLOG相关配置 ～～～

# 表示访问任何以其结尾的域名都将会被记录
FAKE_ROOT_DOMAIN = 'xxx.com'

# 一个域名，配置A记录指向一个DNS服务器，该DNS服务器记录所有访问FAKE_ROOT_DOMAIN结尾的域名记录
NS1_DOMAIN = 'ns1.xxx.com'
# 同上
NS2_DOMAIN = 'ns1.xxx.com'

# DNS服务器ip，NS1_DOMAIN和NS2_DOMAIN配置A记录指向的IP
SERVER_IP = 'xx.xx.xx.xx'
