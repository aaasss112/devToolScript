#!/usr/bin/env bash
# 查看指定包名的Activity堆栈
(adb shell dumpsys activity activities "$1" |  sed -En -e '/Running activities/,/Run #0/p'| grep --color "$1")
