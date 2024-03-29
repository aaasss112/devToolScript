import subprocess
import os
import re


def isEmpty(str):
    if str is None or len(str) == 0:
        return True
    return False


def get_dirs(root_dir, exclude_dir=None):
    """
    获取指定dir下的所有子目录，并且根据exclude_dir排除子目录
    :param root_dir: 指定的根目录
    :param exclude_dir: 要排除的文件夹，type List
    :return: 子目录集合
    """
    if not root_dir:
        print("root_dir is null")
        return None
    os.chdir(root_dir)
    dirs = subprocess.check_output(['ls']).strip().decode()  # type: str
    dirs_arr = dirs.split("\n")  # type: list
    if not exclude_dir:
        return dirs_arr
    for d in exclude_dir:
        if d in dirs_arr:
            dirs_arr.remove(d)  # 排除一些文件夹
    return dirs_arr


def getPidByPkgName(pkgName):
    if isEmpty(pkgName):
        return None
    tempInfo = subprocess.check_output("adb shell ps -o PID,NAME | grep -E '%s$'" % pkgName, shell=True).decode()
    if isEmpty(tempInfo):
        return None
    pids = re.findall("(\\d+).*", tempInfo)
    if not pids:
        return None
    return int(pids[0])
