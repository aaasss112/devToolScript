#!/usr/bin/env python3


"""
删除无用git分支
- 通过正则指定要删除的分支名，然后遍历每个插件进行删除
"""
import subprocess
import os
import fire
from constants import Constants
from util import CommonUtil


def _delete_local_unused_branch(branch_name = None):
    """
    删除本地无用分支
    :param branch_name: 需要删除的branch，支持正则表达式
    """
    if not branch_name:
        print("Error: 请指定要删除的branchName，支持正则，例如：python3 git.py del '7.22\|earning'")
        return
    dirs_arr = CommonUtil.get_dirs(Constants.YY_ROOT_DIR, Constants.EXCLUDE_DIR)
    print(dirs_arr)
    print()
    err_output = open(os.devnull, 'w')  # 隐藏错误输出
    for d in dirs_arr:
        result = os.path.join(Constants.YY_ROOT_DIR, d)
        os.chdir(result)
        try:
            result = subprocess.check_output('git branch | grep -E -i %s | xargs git branch -d' % branch_name,
                                             shell = True,
                                             stderr = err_output).decode()
            if result:
                print("%s: " % d)
                print(result, end = '')
                print()
        except:
            print(end = '')


if __name__ == '__main__':
    fire.Fire({
        "del": _delete_local_unused_branch
    })
