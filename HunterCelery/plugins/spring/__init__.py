#!/ usr/bin/env
# coding=utf-8
"""
author: b5mali4
Copyright (c) 2018
"""
import os
import sys

HUNTER_PATH = "{}/../../../".format(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HUNTER_PATH)
from common.http_util import get_host_port
from common.http_util import get_parent_route
from common.system_util import get_current_time
