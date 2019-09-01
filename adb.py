#!/usr/bin/env python
# -*- coding: utf-8 -*-
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

LOGGING_FORMAT = '%(asctime)s [%(levelname)s]: %(message)s'
logging.basicConfig(format=LOGGING_FORMAT, level=logging.DEBUG)


def _multi_install(apk):
    r""" install local apk into multi devices at once.  

    >>> python adb.py install xx.apk
    """

    if not str(apk).endswith(".apk"):
        logging.error("only support *.apk file")
        return

    try:
        result = subprocess.check_output(['adb', 'devices']).strip()
        reg_result = re.findall(r'(\w+)\t+device', result)
        if reg_result:
            for device_id in reg_result:
                logging.info(
                    "installing apk: %s into device_id: %s ..." % (apk, device_id))
                try:
                    subprocess.check_call(
                        ['adb', '-s', device_id, 'install', '-r', '-d', apk])
                    logging.info(
                        "install success... apk : %s, device_id = %s" % (apk, device_id))
                except:
                    print
                    logging.error(
                        "install failure... apk : %s, device_id = %s \n" % (apk, device_id))
                    continue
        else:
            logging.error(
                "There are not connected devices. Please check devices connection.")
    except Exception as e:
        logging.error(e)


def _path(pkg_name, pull=None):
    """Print the installation path of the specified package name, and pull to specified path.
    
    >>> python adb.py path "com.duowan.mobile"  
    >>> python adb.py path "com.duowan.mobile" ~/Desktop/    
    """
    try:
        logging.info("The package name: %s" % pkg_name)
        pkg_path = subprocess.check_output(
            ['adb', 'shell', 'pm', 'path', pkg_name])
        print pkg_path
        if isinstance(pull, str):
            try:
                path_reg = re.findall(r'.*:(.*)', pkg_path)
                if path_reg and path_reg[0]:
                    logging.info("Being pull to : %s" % pull)
                    subprocess.check_call(
                        ['adb', 'pull', path_reg[0], pull])
                    os.rename(os.path.join(pull, "base.apk"),
                              os.path.join(pull, "%s.apk" % pkg_name))
                    print "\npull to %s success, the apk name is %s.apk" % (
                        pull, pkg_name)
            except Exception as e:
                logging.error("\npull failure...error = %s" % e)
    except:
        logging.error("\nno result, please check input package name!")


if __name__ == "__main__":
    fire.Fire({
        "install": _multi_install,
        "path": _path
    })
