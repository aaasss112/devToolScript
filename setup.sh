#!/usr/bin/env bash
# 配置当前项目的运行环境
if command -v pip3 > /dev/null 2>&1; then
    (pip3 install -r requirement.txt)
else
    echo 'pip3 命令不存在，请参考网上教程安装pip3和python3'
fi