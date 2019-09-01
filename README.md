# devToolScript
日常开发脚本
### [adb.py](./adb.py)
- `python adb.py install xx.apk`：同时在多台已连接的设备上安装apk
- `python adb.py path "com.duowan.mobile""`：根据指定包名查询并显示apk的安装路径
- `python adb.py path "com.duowan.mobile" ~/Desktop/`：同时把apk pull 到指定路径

### [adbTop.sh](./adbTop.sh)
- `./adbTop.sh "com.duowan.mobile"`：查看指定包名的Activity堆栈(若遇到`permission denied: adbTop.sh`，请先运行`chmod +x adbTop.sh`)
