#!/usr/bin/env python3
"""
清理多个文件夹中git中未跟踪的文件和文件夹
"""
import subprocess
import os

exclude_dirs = ['']

os.chdir("/Users/renqiangqiang/AndroidWorkSpace/YY")
dirs = subprocess.check_output(['ls']).strip().decode()  # type: str
dirs_arr = dirs.split("\n")  # type: list
for d in exclude_dirs:
    if d in dirs_arr:
        dirs_arr.remove(d)  # 排除一些文件夹
for d in dirs_arr:
    result = os.path.join('/Users/renqiangqiang/AndroidWorkSpace/YY', d)
    os.chdir(result)
    subprocess.call(['git', 'clean', '-fd']) # 删除git中未跟踪的文件和文件夹
    # print(subprocess.check_output(['git', 'status']).strip().decode())