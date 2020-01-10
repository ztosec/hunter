#!/ usr/bin/env
# coding=utf-8
#
# Copyright 2019 ztosec & https://sec.zto.com/
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
import os

HUNTER_PATH = "{}/../".format(os.path.dirname(os.path.abspath(__file__)))

CAKEY_FILE = '%s/networkproxy/ca.key' % HUNTER_PATH
CACERT_FILE = '%s/networkproxy/ca.crt' % HUNTER_PATH
CERTKEY_FILE = '%s/networkproxy/cert.key' % HUNTER_PATH
CERT_DIR = '%s/networkproxy/certs/' % HUNTER_PATH

HTTPServerSingle = None


def get_http_server():
    return HTTPServerSingle


def set_http_server(http_server):
    global HTTPServerSingle
    if http_server:
        HTTPServerSingle = http_server


__all__ = ["CAKEY_FILE", "CACERT_FILE", "CERT_DIR", "get_http_server"]
