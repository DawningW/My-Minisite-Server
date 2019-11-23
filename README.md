# My-Minisite-Server
 伪(金山毒霸)热点新闻软件服务器

学校恶作剧专用

## 如何构建
> pyinstaller -F -i .\icon.ico .\app.py

## 如何使用
确保data文件夹内的东西完整

编写好您的热点新闻

运行mitmproxy脚本
> mitmdump.exe -s .\mitmaddon.py

运行程序
> app.exe

设置系统全局代理
> 127.0.0.1:端口号

测试
> 访问127.0.0.1/minisite