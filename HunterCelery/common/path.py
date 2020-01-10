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

__all__ = ["HUNTER_PATH", "HUNTER_CONFIG_PATH", "HUNTER_PASS_DIC_PATH", "PLUGIN_PATH", "HUNTER_SCRIPT_PATH",
           "HUNTER_LOG_PATH"]
HUNTER_PATH = os.path.normpath("{}/../".format(os.path.dirname(os.path.abspath(__file__))))

# hunter配置文件路径
HUNTER_CONFIG_PATH = "{}/config/config.ini".format(HUNTER_PATH)
# 插件检测弱密码字典
HUNTER_PASS_DIC_PATH = "{}/config/password.dic".format(HUNTER_PATH)
# 插件路径
PLUGIN_PATH = "{}/plugins/".format(HUNTER_PATH)

# 插件压缩包路径
PLUGIN_ZIP_PATH = "%s/plugins.zip" % HUNTER_PATH

# 客户端下载路径

CLIENT_ROOT_PATH = "{}/api/resource/client".format(HUNTER_PATH)

CHROME_CLIENT_NAME = "hunter-chrome-client.zip"

# 插件配置文件，标注了插件开关
# PLUGIN_PATH_CONFIG = "{}/plugins/".format(HUNTER_PATH)

HUNTER_SCRIPT_PATH = "{}/hunter.py".format(HUNTER_PATH)

# 日志文件路径
HUNTER_LOG_PATH = "{}/logs/logger.log".format(HUNTER_PATH)
