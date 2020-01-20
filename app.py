# coding=utf-8

# 导入
import ctypes
import os
import sys
import copy
import threading
import atexit
import re
import logging
import configparser
import json
import requests
import webbrowser
from watchdog.observers import Observer

from systrayicon import SysTrayIcon
from fileob import FileEventHandler
import msserver

# Hosts文件地址(未使用)
# hostspath = os.getenv("SYSTEMROOT") + "\System32\drivers\etc\hosts"

# 正则表达式
pattern = re.compile("(?<=json \= )(.*)(?= \|\| null;)", re.M)
# (?<=json \= )(?:.|\s)*(?= \|\| null;)

# 我的请求头
headers = {"User-Agent": "MyMinisiteServer/1.0"}
session = None

# 其他线程
traythread = None
serverthread = None

observer = None

# 我的新闻数据
originaldata = {}
# 热点新闻网页模板
minisitetemplates = {}
# 热点新闻服务器地址
minisitehosts = {"kingsoft": "hotnews.duba.com"}
# 热点新闻数据
minisitedata = {}
# 生成的热点新闻数据
generateddata = {}
# 生成的热点新闻主页模板
generatedsites = {}

def main():
    # 设置日志
    logging.basicConfig(filename = "./latest.log", filemode = "w", level = logging.INFO)
    logging.getLogger().addHandler(logging.StreamHandler())
    # 读配置文件
    config = configparser.ConfigParser()
    if not os.path.exists("./settings.ini"):
        config.set("DEFAULT", "ip", "127.0.0.1")
        config.set("DEFAULT", "port", 80)
        with open("./settings.ini", "w") as configfile:
            config.write(configfile)
    else:
        config.read("./settings.ini")
    address = config.get("DEFAULT", "ip")
    port = config.getint("DEFAULT", "port")
    minisitehosts["localhost"] = address + ":" + str(port)
    # 启动系统托盘线程
    global traythread
    traythread = threading.Thread(target = runtray, daemon = False)
    traythread.start()
    logging.info("Welcome to my minisite server. Author: wc")
    # 初始化会话
    global session
    session = requests.Session()
    session.headers.update(headers)
    # 读取本地新闻数据及网页模板
    readlocaldata()
    # 获取热点新闻数据
    logging.info("Getting minisites' news JSON.")
    getminisitedata()
    # 生成热点新闻数据
    logging.info("Generating new minisite news data.")
    generatedata()
    # 生成热点新闻网页
    logging.info("Generating new minisite webpages.")
    generatetemplate()
    # 启动服务器
    global serverthread
    serverthread = threading.Thread(target = msserver.run, daemon = False, args = (address, port, generatedsites, ))
    serverthread.start()
    # 自动重载数据
    global observer
    observer = Observer()
    observer.schedule(FileEventHandler(reload), "./data")
    observer.start()
    # 接受用户输入
    while True:
        line = input(">> ").strip()
        strs = line.split()
        if (len(strs) >= 1):
            processcommand(strs[0], strs[1:])
    return

def readlocaldata():
    # 我的新闻数据
    logging.info("Reading local news JSON.")
    with open("./data/news_data.json", encoding = "utf-8") as f:
        global originaldata
        originaldata = json.load(f)
    # 我的新闻模板
    logging.info("Reading local website templates.")
    with open("./data/news_template.html", encoding = "utf-8") as f:
        generatedsites["local"] = f.read()
    # 热点新闻网页模板
    with open("./data/kingsoft_template.html", encoding = "utf-8") as f:
        minisitetemplates["kingsoft"] = f.read()
    return

def getminisitedata():
    for (key, value) in minisitehosts.items():
        if key == "kingsoft":
            logging.info("Connecting to kingsoft minisite server to get news JSON.")
            r = session.get("http://" + value + "/minisite/1335/")
            r.encoding = "UTF-8"
            s = r.text
            s = re.search(pattern, s).group(1)
            s = s.replace("\"/uploadImg", "\"http://" + value + "/uploadImg")
            minisitedata[key] = json.loads(s)
    return

def generatedata():
    for (key, value) in minisitedata.items():
        if key == "kingsoft":
            generateddata[key] = copy.deepcopy(value)
            # 生成热点词
            hotwords = generateddata[key]["hotWords"]
            hotwords.clear()
            for word in originaldata["keywords"]:
                hotwords.append({"id": 1, "type": 7, "title": word})
            # 生成新闻
            news = []

            count = len(originaldata["news"])
            for index in range(0, count):# [0, count)
                item = originaldata["news"][index]
                style = 1
                if item["type"] == "page": style = 5
                elif item["type"] == "list": style = 17
                elif item["type"] == "video": style = 11
                tab = {"tab": index + 1, "sort": index + 1, "template": style, "title": item["title"], "count": 1, "color": "0", "data": []}
                for (pos, content) in item["content"].items():
                    if pos == "slider":
                        id = 1001
                        for entry in content:
                            tab["data"].append({"id": id, "type": 1, "from": 0, "fontColor": "0","title": entry["title"], "link": entry["link"], "imgUrl": entry["image"], "spread": 0})
                            id += 1
                    elif pos == "videos":
                        id = 2001
                        for entry in content:
                            tab["data"].append({"id": id, "type": 2, "from": 0, "fontColor": "0","title": entry["title"], "link": entry["link"], "imgUrl": entry["image"], "spread": 0})
                            id += 1
                    elif pos == "sidebig":
                        id = 4001
                        for entry in content:
                            tab["data"].append({"id": id, "type": 4, "from": 0, "fontColor": "0","title": entry["title"], "link": entry["link"], "imgUrl": "", "spread": 0})
                            id += 1
                    elif pos == "sidesmall":
                        id = 5001
                        for entry in content:
                            tab["data"].append({"id": id, "type": 5, "from": 0, "fontColor": "0","title": entry["title"], "link": entry["link"], "imgUrl": "", "spread": 0})
                            id += 1
                    elif pos == "images":
                        id = 9001
                        for entry in content:
                            tab["data"].append({"id": id, "type": 9, "from": 0, "fontColor": "0","title": entry["title"], "link": entry["link"], "imgUrl": entry["image"], "spread": 0})
                            id += 1
                    else:
                        pass
                tab["count"] = len(tab["data"])
                news.append(tab)

            inherittabs = []
            if key in originaldata["inherit"]: 
                inherittabs = originaldata["inherit"][key]
            for item in generateddata[key]["news"]:
                if item["title"] in inherittabs:
                    count += 1
                    tab = copy.deepcopy(item)
                    tab["tab"] = count
                    tab["sort"] = count
                    news.append(tab)

            generateddata[key]["news"] = news
    return

def generatetemplate():
    for (key, value) in minisitetemplates.items():
        s = json.dumps(generateddata[key])
        generatedsites[key] = value.replace("{$data}", s)
    return

def getgeneratedsites():
    return generatedsites

def processcommand(name, args):
    "命令输入处理"
    if name == "view":
        print(generateddata["kingsoft"])
    elif name == "open":
        webbrowser.open("http://" + minisitehosts["localhost"] + "/kingsoft/default")
    elif name == "reload":
        reload()
    elif name == "help" or name == "?":
        print("view/open/reload/help/stop")
    elif name == "stop" or name == "exit" or name == "quit" or name == "close":
        sys.exit(0)
    else:
        print("Unknown command. Type \"help\" or \"?\" for more helps.")
    return

def reload():
    readlocaldata()
    generatedata()
    generatetemplate()
    print("Reload successfully!")
    return

def runtray():
    "系统托盘线程"
    logging.info("Start a new thread which manage system tray.")
    global show, tray
    show = True
    tray = SysTrayIcon("./icon.ico", "我的热点新闻服务器", ontrayclicked)
    ontrayclicked()
    tray.loop()
    return

def ontrayclicked():
    "托盘被点击"
    global show
    whnd = ctypes.windll.kernel32.GetConsoleWindow()
    if whnd != 0:
        if show:
            ctypes.windll.user32.ShowWindow(whnd, 0)
        else:
            ctypes.windll.user32.ShowWindow(whnd, 1)
        show = not show
        ctypes.windll.kernel32.CloseHandle(whnd)
    return

@atexit.register
def onexit():
    "退出程序"
    observer.stop()
    observer.join()
    logging.info("Shut down my minisite server. Thanks for your using.")
    return

if __name__ == "__main__":
    main()
