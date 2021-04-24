# My-Minisite-Server
伪(金山毒霸)热点新闻服务端

你可以通过本项目搭建你的热点新闻服务器并在学校来一番恶作剧

本项目包含一个服务端和一个简陋的pyqt客户端,同时也提供了一个mitmproxy脚本,你可利用它来重定向原来的热点新闻客户端

目前仅支持金山系列的热点新闻(hotnews.duba.com/kminisite/default),欢迎二次开发或提交Pull request

并没有支持其它热点新闻的计划,但我看搜狗和flash的新闻很不爽

## 使用的库
- requests
- filetype
- Markdown
- pywin32
- watchdog
- PyInstaller(如果构建则需要安装)
- mitmproxy4(脚本)
- PyQt5(客户端)

## 如何构建
> pyinstaller -F -i .\icon.ico .\app.py
(Tips: 用32位的Python编译会得到32位的可执行文件)

## 如何使用
先修改settings.ini

再确保data和static文件夹内的东西完整

编写好您的热点新闻(全是magic number, 具体如何编写还请查看源码, 有时间会写文档的)

运行mitmproxy脚本
> mitmdump.exe -s .\mitmaddon.py

运行程序
> app.exe

设置系统全局代理
> 127.0.0.1:端口号

测试
> 访问127.0.0.1/kingsoft

## 展示
![1](/docs/1.png)

## TODO/Bugs
- 托盘图标单击可显示/隐藏(已完成,仅Windows)
- 日志输出(已完成)
- 自定义新闻(已完成)
- mitmproxy脚本(已完成)
- 控制台命令(已完成)
- 可在自定义新闻中引用原新闻(已完成)
- 用markdown或html编写新闻(已完成)
- 自动重载(已完成)
- 配置文件(已完成)
- 跨平台支持(已完成)
- 支持多级目录
- 定时刷新
- 重写命令解析器
- 提供原生代理
- 将爬取热点新闻的代码抽象出来
- 文档
- 添加robots.txt禁止搜索引擎抓取(已完成)
- 多线程服务器(已完成)
