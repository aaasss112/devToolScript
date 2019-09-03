#!/usr/bin/env python3

"""
- cd 进入src目录后，执行`python3 -m tests.test_adb`
测试 adb.py的：
- 语法是否正常
- 功能是否正常
"""

import unittest
import constants.code as ErrorCode
import os
import adb

APK_NAME = os.path.join('..', 'testres', 'test.apk')
REMOTE_PAHT = os.path.join('..', 'testres')


class ADBTestCase(unittest.TestCase):

    def test_install01(self):
        unittest.TestCase.assertEqual(
            self, ErrorCode.CODE_EXEC_SUCCESS, adb._multi_install(APK_NAME))

    def test02(self):
        unittest.TestCase.assertEqual(
            self, ErrorCode.CODE_EXEC_FAILURE, adb._multi_install('xx.ap'))

    def test_path01(self):
        unittest.TestCase.assertEqual(self,
                                      adb._path('python.test'), ErrorCode.CODE_EXEC_SUCCESS)

    def test_path02(self):
        unittest.TestCase.assertEqual(self,
                                      adb._path('python.test', REMOTE_PAHT), ErrorCode.CODE_EXEC_SUCCESS)

    def test_screen_cap(self):
        unittest.TestCase.assertEqual(self, adb._screen_shot(
            REMOTE_PAHT), ErrorCode.CODE_EXEC_SUCCESS)


if __name__ == '__main__':
    unittest.main()
