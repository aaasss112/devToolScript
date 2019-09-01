#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import argparse
import logging
import re
import sys
import os
# import pdb

LOGGING_FORMAT = '%(asctime)s [%(levelname)s]: %(message)s'
logging.basicConfig(format=LOGGING_FORMAT, level=logging.DEBUG)


def _multi_install(args):
    r"""
    同时在多台已连接的设备上安装apk

    >>> python adb.py -i xx.apk 
    >>> python adb.py --install xx.apk

    """
    if not str(args.apk).endswith(".apk"):
        logging.error("only support *.apk file")
        return

    try:
        _adb_devices = ['adb', 'devices']
        result = subprocess.check_output(_adb_devices).strip()
        reg_result = re.findall(r'(\w+)\t+device', result)
        if reg_result:
            for device_id in reg_result:
                logging.info(
                    "installing apk: %s into device_id: %s ..." % (args.apk, device_id))
                try:
                    subprocess.check_call(
                        ['adb', '-s', device_id, 'install', '-r', '-d', args.apk])
                    logging.info(
                        "install success... apk : %s, device_id = %s" % (args.apk, device_id))
                except:
                    logging.error(
                        "install failure... apk : %s, device_id = %s \n" % (args.apk, device_id))
                    continue
        else:
            logging.error(
                "There are not connected devices. Please check devices connection.")
    except Exception as e:
        logging.error(e)


def _path(args):
    try:
        logging.info("The package name: %s" % args.pkgName)
        pkg_path = subprocess.check_output(
            ['adb', 'shell', 'pm', 'path', args.pkgName])
        print pkg_path
        if args.target_dir:
            try:
                path_reg = re.findall(r'.*:(.*)', pkg_path)
                if path_reg and path_reg[0]:
                    logging.info("Being pull to : %s" % args.target_dir)
                    subprocess.check_call(
                        ['adb', 'pull', path_reg[0], args.target_dir])
                    os.rename(os.path.join(args.target_dir, "base.apk"),
                              os.path.join(args.target_dir, "%s.apk" % args.pkgName))
                    print "\npull to %s success, the apk name is %s.apk" % (
                        args.target_dir, args.pkgName)
            except Exception as e:
                logging.error("\npull failure...error = %s" % e)
    except:
        logging.error("\nno result, please check input package name!")


def _arg_parse():
    parser = argparse.ArgumentParser(
        description='ADB Extensions: install, and so on.')
    parser.add_argument('--install', '-i',  # 命令参数的名称
                        dest="apk",  # 将命令行中，--install 的参数值赋值给变量apk，你可以用args.apk访问。
                        metavar='[apk]',  # 用于更好的展示--help内容，不指定该值，默认使用dest的值
                        # 展示提示信息，主要是该命令的作用
                        help="Install local [apk] file into multi devices at once"
                        )
    parser.add_argument('--path',
                        dest="pkgName",
                        type=str,
                        metavar='[pkgName]',
                        help="Print the installation path of the specified package name")
    parser.add_argument('--pull',
                        dest="target_dir",
                        metavar='[target_dir]',
                        help="using after --path param,it will pull the apk to specified path")
    return parser.parse_args()


def _setup():
    args = _arg_parse()
    # _multi_install(args)
    _path(args)


if __name__ == "__main__":
    _setup()
