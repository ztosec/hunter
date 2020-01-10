#!/ usr/bin/env
# coding=utf-8
"""
author: b5mali4
Copyright (c) 2018
"""
import unittest
from common import log
from exception.request_classification_exception import HeaderParseError


class LoggerTestCase(unittest.TestCase):
    def testHeaderParseError(self):
        """
        测试异常
        :return: 
        """
        pass

    def testExcectpion(self):
        """
        
        :return: 
        """
        logger2 = log.get_default_logger()
        logger2.exception("11111")


if __name__ == "__main__":
    unittest.main()
