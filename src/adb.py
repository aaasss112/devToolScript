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
import os
import fire
# import pdb
from constants import code as ErrorCode
import datetime
from util import CommonUtil
from ThreadInfo import ThreadInfo

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

    python adb.py install xx.apk
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

    python adb.py path "com.duowan.mobile"
    python adb.py path "com.duowan.mobile" ~/Desktop/

    :parameter pkg_name apk包名
    :parameter pull 远程路径
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

    python3 adb.py screencap ~/Desktop

    :param path 截图导出的路径
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
                'screen shot was successful, output path is: %s' % os.path.join(path,
                                                                                "screen-shot-%s.png" % device))
        return ErrorCode.CODE_EXEC_SUCCESS
    except NoDevicesConnectionException as e:
        logging.error(e)
        return ErrorCode.CODE_NO_DEVICES_CONNECTION
    except:
        logging.error('screen shot has occur some error, please retry... ')
        return ErrorCode.CODE_EXEC_FAILURE


def _dumpHprof(pkgName=None, dumpPath=None):
    """
    dump Hprof文件，会尝试转换hprof文件格式，dump并导出完成后，会自动删除手机中的Hprof文件缓存

    python3 adb.py dump com.baidu.haokan
    :param pkgName: 要dump的apk包名
    :param dumpPath: Hprof文件导出的路径，只是文件夹路径，不是文件路径，不填默认导出到桌面（mac）
    """
    if not pkgName:
        logging.error("pkgName must not be null")
        return ErrorCode.CODE_EXEC_FAILURE
    if not dumpPath or len(dumpPath) == 0:
        dumpPath = os.path.join(os.path.expanduser("~"), 'Desktop', 'hprof_dump')
        if not os.path.exists(str(dumpPath)):
            os.mkdir(str(dumpPath))
    try:
        devices = _get_connection_devices()
        if len(devices) > 1:
            logging.error('暂不支持多台已连接设备')
            return ErrorCode.CODE_EXEC_FAILURE
        hprof_file_name_tmp = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        hprof_file_name = hprof_file_name_tmp + ".hprof"
        hprofCachePath = "/data/local/tmp/%s" % hprof_file_name
        print('Waiting for [%s] dump to finish... ' % hprofCachePath)
        subprocess.check_output("adb shell am dumpheap %s %s" % (pkgName, hprofCachePath), shell=True)
        subprocess.check_output("adb pull %s %s" % (hprofCachePath, dumpPath), shell=True)
        subprocess.check_output("adb shell rm -rf %s " % hprofCachePath, shell=True)
        try:
            # Library/Android/sdk/platform-tools/hprof-conv
            android_platform_tools = os.path.join("Library", "Android", "sdk", "platform-tools", "hprof-conv")
            hprof_convert_path = os.path.join(os.path.expanduser("~"), android_platform_tools)
            print('convert hprof file...hprof_convert_path = ' + hprof_convert_path)
            origin_file = os.path.join(dumpPath, hprof_file_name)
            converted_file = os.path.join(dumpPath, hprof_file_name_tmp + "-converted.hprof")
            subprocess.call("%s -z %s %s " % (hprof_convert_path, origin_file, converted_file), shell=True)
            print('convert hprof file success, converted file = ' + converted_file)
        except Exception as e:
            print('convert hprof file failure')
            pass
        print('dump success, hprofCachePath: %s' % dumpPath)
    except NoDevicesConnectionException as e:
        logging.error(e)
        return ErrorCode.CODE_NO_DEVICES_CONNECTION
    except:
        logging.error('dumpHprof has occur some error, please retry... ')
        return ErrorCode.CODE_EXEC_FAILURE


def _formatOriginThreadInfoList(originThreadInfoList):
    if not originThreadInfoList:
        return
    infoMap = {}
    for index, item in enumerate(originThreadInfoList):
        temp = item.strip()
        if CommonUtil.isEmpty(temp) or index == 0:
            continue
        value = infoMap.get(temp)
        if not value:
            infoMap[temp] = ThreadInfo(temp, 1)
        else:
            value.plusCount()
    return infoMap


def _formatPrintThread(threadList):
    print("Count    ThreadName")
    for item in threadList:
        print("%s         %s" % (item[1].count, item[1].name))


def _filterThreadMap(map, limit):
    infoMap = {}
    for key, value in map.items():
        if value.count >= limit:
            infoMap[key] = value
    sortedMap = sorted(infoMap.items(), key=lambda item: item[1].count, reverse=True)
    return sortedMap


def _threadInfo(pkgName=None, limit=5):
    """
    python3 adb.py thread com.baidu.haokan

    dump thread 信息
    :param pkgName: app包名
    :param limit: 线程数超过指定的数量才进行统计，默认线程数超过5条的线程才统计
    """
    if not pkgName:
        logging.error("pkgName [%s] invalid" % pkgName)
        return
    pid = CommonUtil.getPidByPkgName(pkgName)
    if not pid:
        logging.error("can not get pid from pkg [%s], please check pkgName first" % pkgName)
        return
    threadInfo = subprocess.check_output("adb shell ps -T -o CMD -p %s" % pid, shell=True).decode()
    originThreadInfoList = re.split('\n', threadInfo)
    print("pkgName = %s, pid = %s, TotalThreadCount = %s" % (pkgName, pid, len(originThreadInfoList) - 2))
    if limit == 0:
        print("=========所有线程及对应数量如下=====================")
    else:
        print("=========线程数大于等于%s的线程如下=====================" % limit)
    threadMap = _formatOriginThreadInfoList(originThreadInfoList)
    sorteList = _filterThreadMap(threadMap, limit)
    _formatPrintThread(sorteList)


def _crashDump(pkgName=None, output=None):
    """
    python3 adb.py bug com.baidu.haokan
    dump崩溃、ANR等相关文件
    1. dump bugreport
    2. dump anrtrace
    :param pkgName: app包名
    :param output: dump的文件输出路径, 只是文件夹路径，不是文件路径，不填默认导出到桌面（mac）
    """
    if not pkgName:
        logging.error("pkgName [%s] invalid" % pkgName)
        return
    pid = CommonUtil.getPidByPkgName(pkgName)
    if not pid:
        logging.error("can not get pid from pkg [%s], please check pkgName first" % pkgName)
        return
    if not output:
        output = os.path.join(os.path.expanduser("~"), 'Desktop')
    print("crash dump start")
    try:
        print("dump bugreport start...")
        subprocess.check_output("adb bugreport %s " % output, shell=True)
        print("dump bugreport success...")
    except:
        print("dump bugreport fail...")

    try:
        print("try to  pull ANRTrace...")
        subprocess.check_output("adb pull /data/anr %s " % output, shell=True)
        print("pull ANRTrace success...")
    except:
        print("pull ANRTrace Fail...")
    try:
        print("dump meminfo start...")
        subprocess.check_output("adb shell dumpsys meminfo %s " % output, shell=True)
        print("dump meminfo success...")
    except:
        print("dump meminfo fail...")

def _cpuDump(pkgName=None):
    """
    python3 adb.py cpu com.baidu.haokan

    :param pkgName: app包名
    """
    if not pkgName:
        logging.error("pkgName [%s] invalid" % pkgName)
        return
    pid = CommonUtil.getPidByPkgName(pkgName)
    if not pid:
        logging.error("can not get pid from pkg [%s], please check pkgName first" % pkgName)
        return
    subprocess.check_call("adb shell top -H -p %s " % pid, shell=True)    

if __name__ == "__main__":
    fire.Fire({
        "install": _multi_install,
        "path": _path,
        'cap': _screen_shot,
        'dump': _dumpHprof,
        'thread': _threadInfo,
        'bug': _crashDump,
        'cpu':_cpuDump
    })
