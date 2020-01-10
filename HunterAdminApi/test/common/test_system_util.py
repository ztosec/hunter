#!/ usr/bin/env
# coding=utf-8
"""
author: b5mali4
Copyright (c) 2018
"""
import unittest
from common.plugins_util import get_module, get_plugin, print_module, print_plugin, load_pyfiles, load_checkers


class SystemUtilTestCase(unittest.TestCase):
    """
    时间工具
    """

    def testGetFrontData(self):
        """
        获取前几天
        :return: 
        """
        import logging
        logger = logging.getLogger('peewee')
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.DEBUG)

        from common.system_util import get_front_date
        from model.task import Task, TaskService
        front_date = get_front_date(100)
        tasks = TaskService.get_fields_by_where(where=(Task.created_time >= front_date))
        for task in tasks:
            print(task)

    def testZipFile(self):
        from common.system_util import zip_file
        from common.path import PLUGIN_PATH
        target_file = "%stmp/plugin.zip" % PLUGIN_PATH
        origin_file = "%s/spring/cve_2018_1273.py" % PLUGIN_PATH
        print(target_file)
        zip_file(target_file=target_file, origin_file=origin_file)

    def testZipFolder(self):
        from common.system_util import zip_folder
        from common.path import PLUGIN_PATH
        target_file = "%stmp/plugin.zip" % PLUGIN_PATH
        origin_folder = PLUGIN_PATH
        zip_folder(target_file=target_file, origin_folder=origin_folder)

    def testCase1ZipFloderSkip(self):
        from common.system_util import zip_floder_skip
        from common.path import PLUGIN_PATH
        target_file = "%stmp/plugin.zip" % PLUGIN_PATH
        origin_folder = PLUGIN_PATH
        # zip_floder_skip(target_file=target_file, origin_folder=origin_folder, is_regular=True, skip_list=["1*"])

        zip_floder_skip(target_file=target_file, origin_folder=origin_folder, is_regular=True,
                        skip_list=["*DS_Store", "*__pycache__*", "tmp/*"])

    def testCase2ZipFloderSkip(self):
        from common.system_util import zip_floder_skip
        from common.path import PLUGIN_PATH
        target_file = "%stmp/plugin.zip" % PLUGIN_PATH
        origin_folder = PLUGIN_PATH

        zip_floder_skip(target_file=target_file, origin_folder=origin_folder, is_regular=False,
                        skip_list=["tmp/test.py", "tmp/plugin.zip"])

    def testCaseUnZipFile(self):
        from common.system_util import unzip_file
        from common.path import HUNTER_PATH
        origin_file = "%s/HunterCelery/plugins.zip" % HUNTER_PATH
        target_folder = "%s/HunterCelery/plugins/" % HUNTER_PATH
        unzip_file(origin_file=origin_file, target_folder=target_folder)


if __name__ == "__main__":
    unittest.main()
