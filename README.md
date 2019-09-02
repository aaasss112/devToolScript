# devToolScript
日常开发脚本
## before of all
1. 所有Python脚本基于`Python3`,且只支持`Python3`
2. `./setup.sh`:项目根目录运行该命令，配置项目，安装相关依赖

### [adb.py](./adb.py)
- `python3 adb.py install xx.apk`：同时在多台已连接的设备上安装apk
- `python3 adb.py path "com.duowan.mobile""`：根据指定包名查询并显示apk的安装路径
- `python3 adb.py path "com.duowan.mobile" ~/Desktop/`：同时把apk pull 到指定路径
- `python3 adb.py screencap ~/Desktop`：获取连接设备的实时截图，多台设备连接时，会分别获取每台设备的截图

### [adbTop.sh](./adbTop.sh)
- `./adbTop.sh "com.duowan.mobile"`：查看指定包名的Activity堆栈，可用于查看当前显示的Activity(若遇到`permission denied: adbTop.sh`，请先运行`chmod +x adbTop.sh`)
