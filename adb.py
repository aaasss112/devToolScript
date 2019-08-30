#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import argparse
import logging
import re
import sys
# import pdb

LOGGING_FORMAT = '%(asctime)s [%(levelname)s]: %(message)s'
logging.basicConfig(format=LOGGING_FORMAT, level=logging.DEBUG)
apk = sys.argv[1]


def multi_install():
    """
    同时在多台已连接的设备上安装apk
    """
    try:
        _adb_devices = ['adb', 'devices']
        result = subprocess.check_output(_adb_devices).strip()
        reg_result = re.findall(r'(\w+)\t+device', result)
        if reg_result:
            for device_id in reg_result:
                logging.info(
                    "installing apk: %s into device_id: %s ..." % (apk, device_id))
                try:
                    subprocess.check_call(
                        ['adb', '-s', device_id, 'install', '-r', apk])
                    logging.info(
                        "install success... apk : %s, device_id = %s" % (apk, device_id))
                except subprocess.CalledProcessError as e:
                    logging.error(
                        "install failure... apk : %s, device_id = %s \n" % (apk, device_id))
                    continue
        else:
            logging.error(
                "There are not connected devices. Please check devices connection.")
    except Exception as e:
        logging.error(e)


if __name__ == "__main__":
    multi_install()
