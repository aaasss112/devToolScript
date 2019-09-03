#!/usr/bin/env python3
r""" A command line tool for ADB

Command Usage:

install:
    install local apk into multi devices at once.
- python adb.py install xx.apk

path:
    Print the installation path of the specified package name, and pull to specified path
- python adb.py path "com.duowan.mobile"
- python adb.py path "com.duowan.mobile" ~/Desktop/

"""
import subprocess
import logging
import re
import sys
import os
import fire
# import pdb
from constants import code as ErrorCode

LOGGING_FORMAT = '%(asctime)s [%(levelname)s]: %(message)s'
logging.basicConfig(format=LOGGING_FORMAT, level=logging.DEBUG)


class NoDevicesConnectionException(Exception):
    def __init__(self, output='当前没有已连接的设备，请确保设备连接后重试'):
        self.output = output

    def __str__(self):
        return self.output


def _get_connection_devices():
    """获取已连接的设备id"""
    devices = []
    try:
        result = subprocess.check_output(['adb', 'devices']).strip().decode()
        devices = re.findall('(\w+)\t+device', result)
    except:
        pass
    if len(devices) > 0:
        return devices

    raise NoDevicesConnectionException()


def _multi_install(apk):
    r""" install local apk into multi devices at once.

    >>> python adb.py install xx.apk
    """
    if not apk.endswith(".apk"):
        logging.error("only support *.apk file")
        return ErrorCode.CODE_EXEC_FAILURE

    try:
        devices = _get_connection_devices()
        for device in devices:
            logging.info(
                "installing apk: %s into device: %s ..." % (apk, device))
            try:
                subprocess.check_output(
                    ['adb', '-s', device, 'install', '-r', '-d', apk])
                logging.info(
                    "install success... apk : %s, device = %s" % (apk, device))
            except:
                print
                logging.error(
                    "install failure... apk : %s, device = %s \n" % (apk, device))
                continue
        return ErrorCode.CODE_EXEC_SUCCESS
    except NoDevicesConnectionException as e:
        logging.error(e)
        return ErrorCode.CODE_NO_DEVICES_CONNECTION
    except Exception as e:
        logging.error(e)
        return ErrorCode.CODE_EXEC_FAILURE


def _path(pkg_name, pull=None):
    """Print the installation path of the specified package name, and pull to specified path.

    >>> python adb.py path "com.duowan.mobile"
    >>> python adb.py path "com.duowan.mobile" ~/Desktop/
    """
    try:
        if len(_get_connection_devices()) > 1:
            logging.error('检测到多台设备连接，请确保只有一台设备连接后重试')
            return ErrorCode.CODE_EXEC_FAILURE
        logging.info("The package name: %s" % pkg_name)
        pkg_path = subprocess.check_output(
            ['adb', 'shell', 'pm', 'path', pkg_name]).decode()
        print(pkg_path)
        if isinstance(pull, str):
            try:
                path_reg = re.findall(r'.*:(.*)', pkg_path)
                if path_reg and path_reg[0]:
                    logging.info("Being pull to : %s" % pull)
                    subprocess.check_output(
                        ['adb', 'pull', path_reg[0], pull])
                    os.rename(os.path.join(pull, "base.apk"),
                              os.path.join(pull, "%s.apk" % pkg_name))
                    print("\npull to %s success, the apk name is %s.apk" % (
                        pull, pkg_name))
                    return ErrorCode.CODE_EXEC_SUCCESS
            except Exception as e:
                logging.error("\npull failure...error = %s" % e)
                return ErrorCode.CODE_EXEC_FAILURE
        return ErrorCode.CODE_EXEC_SUCCESS
    except NoDevicesConnectionException as e:
        logging.error(e)
        return ErrorCode.CODE_NO_DEVICES_CONNECTION
    except:
        logging.error("\nno result, please check input package name!")
        return ErrorCode.CODE_EXEC_FAILURE


def _screen_shot(path):
    """ 获取连接设备的实时截图，多台设备连接时，会分别获取每台设备的截图

    >>> python3 adb.py screencap ~/Desktop
    """
    if not path:
        logging.error('path invalid, please check the path.')
        return ErrorCode.CODE_EXEC_FAILURE
    try:
        devices = _get_connection_devices()
        if len(devices) > 1:
            logging.info('当前有多台已连接设备，会分别获取每台设备的实时屏幕截图，并以设备id命名')
        for device in devices:
            logging.info('start %s screen shot...' % device)
            _screen_shot_name = '/sdcard/screen-shot-%s.png' % device
            subprocess.check_call(
                ['adb', '-s', device, 'shell', 'screencap', '-p', _screen_shot_name])
            subprocess.check_output(
                ['adb', '-s', device, 'pull', _screen_shot_name, path])
            subprocess.check_call(
                ['adb', '-s', device, 'shell', 'rm', _screen_shot_name])
            logging.info(
                'screen shot was successful, output path is: %s' % os.path.join(path, "screen-shot-%s.png" % device))
        return ErrorCode.CODE_EXEC_SUCCESS
    except NoDevicesConnectionException as e:
        logging.error(e)
        return ErrorCode.CODE_NO_DEVICES_CONNECTION
    except:
        logging.error('screen shot has occur some error, please retry... ')
        return ErrorCode.CODE_EXEC_FAILURE


if __name__ == "__main__":
    fire.Fire({
        "install": _multi_install,
        "path": _path,
        'screencap': _screen_shot
    })
