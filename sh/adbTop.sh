#!/usr/bin/env bash

# activity 'com.duowan.mobile' 查看指定包名的Activity堆栈，顶级Activity
# pid 'com.duowan.mobile'查看指定包名的pid

PKG_NAME="com.duowan.mobile"
COMMAND=('install' ' pid')

result=`adb devices`
if [ $? != 0 ]; then
    echo '请检查设备连接'
    exit 1
fi

case $1 in
    'activity' | 'ac') 
        if [ -z "$2" ]; then
            pkg=$PKG_NAME
        else
            pkg=$2
        fi
        (adb shell dumpsys activity activities "$pkg" |  sed -En -e '/Running activities/,/Run #0/p'| grep --color -i "$pkg")
        if [ $? != 0 ]; then
            echo  '对应包名的APP没在运行中，请打开指定包名的应用后重试'
        fi
    ;;
    'pid')
        if [ -z "$2" ]; then
            pkg=$PKG_NAME
        else
            pkg=$2
        fi
        (adb shell ps | head -n 1 ; adb shell ps | grep --color -i "$pkg")
    ;;
    *) echo "unsupport command: [$1], only support :" $(IFS=, ; echo "[${COMMAND[*]}]") 
    ;;
esac