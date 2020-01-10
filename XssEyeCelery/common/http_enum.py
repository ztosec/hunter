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


class HttpEnum():
    # Default POST data content-type
    DEFAULT_CONTENT_TYPE = "application/x-www-form-urlencoded"

    # Raw text POST data content-type
    PLAIN_TEXT_CONTENT_TYPE = "text/plain"

    # json text POST data content-type
    JSON_TEXT_CONTENT_TYPE = "application/json"

    # form text POST data content-type
    FORM_DATA_CONTENT_TYPE = "multipart/form-data"
