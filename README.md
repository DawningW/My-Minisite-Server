# My-Minisite-Server
伪(金山毒霸)热点新闻服务端

你可以通过本项目搭建你的热点新闻服务器并在学校来一番恶作剧

本项目包含一个服务端和一个简陋的qt客户端, 同时也提供了一个mitmproxy脚本, 你可利用它来重定向原来的热点新闻客户端

目前仅支持金山系列的热点新闻(hotnews.duba.com/kminisite/default), 欢迎二次开发或提交Pull Request

目前并没有支持其它热点新闻的计划, 但我看搜狗和Flash的新闻很不爽

**2022/7/8 由于毒霸热点已停止服务, 本项目进入暂停维护阶段**

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
> pyinstaller -F -i .\icon.ico .\main.py

(Tips: 用32位的Python编译会得到32位的可执行文件)

## 如何使用
先修改settings.ini

再确保data和assets文件夹内的东西完整

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

## 特性
- 可自定义新闻
- 可在自定义新闻中引用原新闻
- 可用Markdown或HTML编写新闻
- 自动重载
- 配置文件
- 日志和控制台命令
- 跨平台支持
- 允许浏览器缓存静态资源
- 可启用robots.txt, 禁止搜索引擎抓取
- 可从反向代理获取客户真实IP地址(通过X-Forwarded-For)
- 托盘图标单击可显示/隐藏(仅Windows)
- 提供mitmproxy脚本修改毒霸热点新闻客户端的请求

## TODO/Bugs
- 定时刷新原新闻
- 提供原生代理
- 将爬取新闻的代码抽象为库
- 文档
- 加入China Daily新闻源, 图一乐的同时还能学学英语
- http://newsminisite.duba.com/
