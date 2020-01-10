#!/ usr/bin/env
# coding=utf-8
"""
author: b5mali4
Copyright (c) 2018
"""
import unittest


class LoggerTestCase(unittest.TestCase):
    def testFileAutoCreate(self):
        """
        测试log文件是否自动创建
        :return: 
        """
        from common import log
        logger1 = log.get_default_logger()
        logger1.info("1222")
        logger2 = log.getLogger("334555")
        logger2.info("4555")

    def testColorLog(self):
        """
        测试非windows系统下log颜色是否为正常显示
        :return: 
        """
        from common import log
        logger2 = log.get_default_logger()
        logger2.info("info")
        logger2.error("error")
        logger2.warning("warning")
        logger2.critical("critical")

    def testExceptionLog(self):
        """
        测试是否能够捕获异常
        :return: 
        """
        from common import log
        logger2 = log.get_default_logger()
        try:
            number = 1 / 0
        except ZeroDivisionError as e:
            logger2.exception("11111")
            logger2.info("info")


if __name__ == "__main__":
    unittest.main()
