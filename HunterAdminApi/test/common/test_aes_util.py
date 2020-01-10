#!/ usr/bin/env
# coding=utf-8
"""
author: b5mali4
Copyright (c) 2018
"""

import unittest


class AesUtilTestCase(unittest.TestCase):
    def testCase1(self):
        """
        测试
        :return: 
        """
        import json
        import datetime
        from common.aes_util import prpcrypt
        clear_data = {"task_id": 1, "username": "12", "create_time": "44"}
        print(type(json.dumps(clear_data)))
        print(json.dumps(clear_data))
        print(prpcrypt.get_single_instance("keyskeyskeyskeys", False).encrypt(json.dumps(clear_data)))

        """
        threads = list()
        for i in range(50):
            thread = threading.Thread(target=prpcrypt.get_single_instance, args=("key", False))
            thread.start()
        """
        # threads.append(thread)
        # print(prpcrypt.get_single_instance())
        pc = prpcrypt('keyskeyskeyskeys')  # 初始化密钥
        e = pc.encrypt("hello")  # 加密
        d = pc.decrypt(e)  # 解密
        print("加密:", e)
        print("解密:", d)
        print(datetime.datetime.now())
        print(type(datetime.datetime.now()))
        print(str(datetime.datetime.now()))


if __name__ == "__main__":
    unittest.main()