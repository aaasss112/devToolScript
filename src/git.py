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


def _delete_local_unused_branch(branch_name=None):
    """
    批量删除本地无用分支
    :param branch_name: 需要删除的branch，支持正则表达式
    """
    if not branch_name:
        print("Error: 请指定要删除的branchName，支持正则，例如：python3 git.py del '7.22|earning|feature'")
        return
    dirs_arr = CommonUtil.get_dirs(Constants.YY_ROOT_DIR, Constants.EXCLUDE_DIR)
    print(dirs_arr)
    print()
    err_output = open(os.devnull, 'w')  # 隐藏错误输出
    for d in dirs_arr:
        result = os.path.join(Constants.YY_ROOT_DIR, d)
        os.chdir(result)
        try:
            result = subprocess.Popen("git branch | grep -E -i '%s' | xargs git branch -D" % branch_name,
                                      shell=True, stdout=subprocess.PIPE, stderr=err_output)
            print("%s: " % d)
            while result.poll() is None:
                line = result.stdout.readline().strip().decode("utf-8")
                if line:
                    print(line, end='')
                    print()
            print()
        except Exception as e:
            print("del exception = %s" % e, end='')
            print()


def _checkout_branch(branch_name=None):
    """
    批量检出指定分支，支持正则表达式
    :param branch_name 分支名，不可为空
    """
    if not branch_name:
        print("请输入要切换的分支名称，支持正则")
        return
    dirs_arr = CommonUtil.get_dirs(Constants.YY_ROOT_DIR, Constants.EXCLUDE_DIR)
    # dirs_arr = ['pluginlivebasemedia', 'ycloud', 'entmobile', 'entlive', 'livebasebiz']
    for d in dirs_arr:
        result = os.path.join(Constants.YY_ROOT_DIR, d)
        os.chdir(result)
        try:
            print("%s: " % d)
            # 先检查本地分支
            try:
                local_branch = subprocess.check_output('git branch | grep %s' % branch_name, shell=True).decode()
                local_branch_arr = list(filter(None, local_branch.split("\n")))  # type: list
                if len(local_branch_arr) == 1:
                    if '*' not in local_branch_arr[0]:
                        subprocess.call('git checkout %s' % local_branch_arr[0], shell=True)  # 检出匹配到的本地分支
                    else:
                        print("当前分支 %s 已经是目标分支，无需切换" % local_branch_arr[0])
                    continue
                elif len(local_branch_arr) > 1:
                    print("匹配到多个本地分支，请细化正则表达式后重试")
                    continue
            except:
                # 再检查远程分支
                subprocess.check_output(['git', 'fetch'])
                try:
                    remote_branch = subprocess.check_output('git branch -r | grep %s' % branch_name,
                                                            shell=True).decode()
                    remote_branch_arr = list(filter(None, remote_branch.split("\n")))  # type: list
                    if len(remote_branch_arr) == 1:
                        first_remote_branch = remote_branch_arr[0]
                        format_remote_branch = first_remote_branch.split("/")[-1]
                        subprocess.call('git checkout -b %s %s' % (format_remote_branch, first_remote_branch),
                                        shell=True)  # 检出匹配到的远程分支
                        continue
                    elif len(remote_branch_arr) > 1:
                        print("匹配到多个远程分支，请细化正则表达式后重试")
                        continue
                except:
                    print("未匹配到任何分支，请检查正则表达式是否正确")

        except Exception as e:
            print(e, end='')


def _list_branch():
    dirs_arr = CommonUtil.get_dirs(Constants.YY_ROOT_DIR, Constants.EXCLUDE_DIR)
    print(dirs_arr)
    print()
    for d in dirs_arr:
        path = os.path.join(Constants.YY_ROOT_DIR, d)
        print(path)
        os.chdir(path)
        try:
            result = subprocess.check_output('git branch', shell=True).decode()
            if result:
                print("%s: " % d)
                print(result, end='')
                print()
        except Exception as e:
            print(e, end='')


def _pull():
    dirs_arr = CommonUtil.get_dirs(Constants.YY_ROOT_DIR, Constants.EXCLUDE_DIR)
    print(dirs_arr)
    print()
    for d in dirs_arr:
        path = os.path.join(Constants.YY_ROOT_DIR, d)
        print(path)
        os.chdir(path)
        try:
            result = subprocess.check_output('git fetch', shell=True).decode()
            if result:
                print("%s: " % d)
                print(result, end='')
                print()
        except Exception as e:
            print(e, end='')


if __name__ == '__main__':
    fire.Fire({
        "del": _delete_local_unused_branch,
        "co": _checkout_branch,
        "br": _list_branch,
        "fe": _pull
    })
