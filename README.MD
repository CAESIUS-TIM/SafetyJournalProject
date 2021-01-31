# 华东理工大学信息门户>抗疫服务>返校前健康日报>自动打卡

## 【除python外的其他软件】
需要用到谷歌浏览器, 以及浏览器相应的版本驱动

查看谷歌浏览器版本：谷歌浏览器->设置->关于Chrome
谷歌浏览器镜像下载网站: http://npm.taobao.org/mirrors/chromedriver/

驱动放置：

1. 将驱动放到python安装目录下的Script目录下, 并且复制一份到谷歌浏览器的安装目录下
2. 将驱动放到该脚本同一目录下
; 其实就是python解释器能通过环境变量找到的目录
; 亦可以使用火狐浏览器, 但也要下载相应版本的驱动, 如上

## 【配置文件】
在同一目录下下创建'config.ini'文件，格式如下：

```
[SafetyJournal]
username=用户名
password=密码
province=省
city=市
address=地址
temperature=体温
```
; 学号 密码 为必填项目
; 非必要项填不填或错会填写默认值
; 默认编码 utf8

注意：

1. 若是其他目录，但是请注意路径

## 开机自启

在开机启动文件夹(以下路径等价)创建一个`*.bat`文本文件
```
C:\Users\用户名\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
%USERNAME%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
```
内部填写`python`+`auto.py`的绝对路径, 就可以实现开机自动打卡，一天一次，还有打印错误log。

如
`SafetyJournal.dat`
```
python C:\SafetyJournalProject\auto.py
```