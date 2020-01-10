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

import os

HUNTER_PATH = os.path.normpath("{}/../".format(os.path.dirname(os.path.abspath(__file__))))

SQLMAP_SCRIPT_PATH = "{}/sqlmap/sqlmap.py".format(HUNTER_PATH)

# 日志文件路径
HUNTER_LOG_PATH = "{}/logs/logger.log".format(HUNTER_PATH)

# 配置文件
HUNTER_CONFIG_PATH = "{}/config/config.ini".format(HUNTER_PATH)

# Fuzz字典
FUZZ_DIC_PATH = "{}/config/payload.dic".format(HUNTER_PATH)

# 插件路径
PLUGIN_PATH = "{}/plugins/".format(HUNTER_PATH)
