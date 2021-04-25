# coding=utf-8

import os
import sys
import copy
import re
import logging
import configparser
import json
import requests
import webbrowser
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from msserver import ThreadingHTTPServer

# 正则表达式
pattern = re.compile(r"(?<=json \= )(.*)(?= \|\| null;)", re.M)
# (?<=json \= )(?:.|\s)*(?= \|\| null;)

# 我的请求头
headers = {"User-Agent": "MyMinisiteServer/1.0"}
session = None

# HTTP服务器
server = None
# 文件监控
observer = None

# 我的新闻数据
originalData = {}
# 热点新闻服务器地址
minisiteHosts = {"kingsoft": "http://hotnews.duba.com"}
# 热点新闻网页模板
minisiteTemplates = {}
# 热点新闻数据
minisiteData = {}
# 生成的热点新闻数据
generatedData = {}
# 生成的热点新闻主页
generatedSites = {}

def run():
    # 读取配置文件 TODO 重写配置文件读取
    config = configparser.ConfigParser()
    if not os.path.exists("./settings.ini"):
        logging.info("Can't find settings. Creating settings.ini.")
        config.set("DEFAULT", "ip", "127.0.0.1")
        config.set("DEFAULT", "port", "80")
        config.set("DEFAULT", "host", "http://yourserver.com")
        config.set("DEFAULT", "silent", "false")
        config.set("DEFAULT", "allow_webspiders", "false")
        with open("./settings.ini", "w") as configFile:
            config.write(configFile)
    else:
        config.read("./settings.ini")
    address = config.get("DEFAULT", "ip")
    port = config.getint("DEFAULT", "port")
    minisiteHosts["localhost"] = config.get("DEFAULT", "host")
    if config.getboolean("DEFAULT", "silent"):
        from systraymgr import onTrayClicked
        onTrayClicked()
    robotstxt = not config.getboolean("DEFAULT", "allow_webspiders")
    # 初始化会话
    global session
    session = requests.Session()
    session.headers.update(headers)
    # 读取本地热点新闻模板和数据
    logging.info("Loading custom templates and news data.")
    readLocalData()
    # 爬取热点新闻网页和数据
    logging.info("Getting minisites' templates and news data.")
    getMinisiteData()
    # 生成新的热点新闻数据
    logging.info("Generating new minisite news data.")
    generateData()
    # 生成新的热点新闻网页
    logging.info("Generating new minisite webpages.")
    generateSites()
    # 启动服务器
    global server
    server = ThreadingHTTPServer(address, port, generatedSites, robotstxt)
    server.start()
    # 自动重载数据
    global observer
    observer = Observer()
    observer.schedule(MyFileEventHandler(), "./data")
    observer.start()
    # 接受用户输入
    while True:
        line = input(">> ").strip()
        strs = line.split()
        if (len(strs) >= 1):
            processCommand(strs[0], strs[1:])
    return

def readLocalData():
    "从本地读取自定义热点新闻网页模板和数据"
    with open("./data/news_template.html", encoding = "utf-8") as f:
        minisiteTemplates["localhost"] = f.read()
    with open("./data/news_data.json", encoding = "utf-8") as f:
        s = f.read()
        s = s.replace("{$localhost}", minisiteHosts["localhost"])
        global originalData
        originalData = json.loads(s)
    with open("./data/detail_template.html", encoding = "utf-8") as f:
        generatedSites["content"] = f.read()
    return

def getMinisiteData():
    "从各热点新闻服务器爬取网页和数据"
    for (key, value) in minisiteHosts.items():
        if key == "kingsoft":
            logging.info("Connecting to kingsoft minisite server to get news webpage.")
            try:
                r = session.get(value + "/minisite/1335/")
                r.encoding = "UTF-8-sig" # 为啥金山的新闻是UTF-8带BOM的呢???
                # m = re.search(pattern, r.text)
                def repl(m):
                    s = m.group(1).replace("\"/uploadImg", "\"" + value + "/uploadImg")
                    minisiteData[key] = json.loads(s)
                    return "{$data}"
                s = re.sub(pattern, repl, r.text)
                s = s.replace("/minisite", value + "/minisite")
                minisiteTemplates[key] = s
            except requests.exceptions.RequestException as e:
                logging.error("An error has occurred when getting webpage: %s", e)
                logging.info("Load alternate data from local.")
                with open("./data/kingsoft_template.html", encoding = "utf-8") as f:
                    minisiteTemplates[key] = json.loads(f.read())
                with open("./data/kingsoft_data.json", encoding = "utf-8") as f:
                    minisiteData[key] = f.read()
    return

def generateData():
    "为各热点新闻重新生成新数据"
    for (key, value) in minisiteData.items():
        if key == "kingsoft":
            generatedData[key] = copy.deepcopy(value)
            # 生成热点词
            hotwords = generatedData[key]["hotWords"]
            hotwords.clear()
            for word in originalData["keywords"]:
                hotwords.append({"id": 1, "type": 7, "title": word})
            # 生成新闻
            news = []

            count = len(originalData["news"])
            for index in range(0, count): # [0, count)
                item = originalData["news"][index]
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
                    elif pos == "videos2":
                        # 当template=11时(video)有3个type=21的条目(右侧3个视频)
                        id = 2010
                        for entry in content:
                            tab["data"].append({"id": id, "type": 21, "from": 0, "fontColor": "0","title": entry["title"], "link": entry["link"], "imgUrl": entry["image"], "spread": 0})
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

            inheritTabs = []
            if key in originalData["inherit"]: 
                inheritTabs = originalData["inherit"][key]
            for item in generatedData[key]["news"]:
                if item["title"] in inheritTabs:
                    count += 1
                    tab = copy.deepcopy(item)
                    tab["tab"] = count
                    tab["sort"] = count
                    news.append(tab)

            generatedData[key]["news"] = news
    return

def generateSites():
    "为各热点新闻重新生成新页面"
    for (key, value) in minisiteTemplates.items():
        s = None
        if key == "localhost":
            s = json.dumps(originalData)
        else:
            s = json.dumps(generatedData[key])
        generatedSites[key] = value.replace("{$data}", s)
    return

def reload(download = False):
    "重载"
    readLocalData()
    if download:
        getMinisiteData()
    generateData()
    generateSites()
    print("Reload successfully!")
    return

def close():
    "关闭"
    session.close()
    observer.stop()
    observer.join()
    server.stop()
    return

def processCommand(name, args):
    "解析命令输入"
    if name == "view":
        print(generatedData["kingsoft"])
    elif name == "open":
        webbrowser.open(minisiteHosts["localhost"] + "/kingsoft/default")
    elif name == "reload":
        reload()
    elif name == "help" or name == "?":
        print("----- Command Help -----")
        print("view - 查看生成的热点新闻数据")
        print("open - 在浏览器中打开我的热点新闻网页")
        print("reload - 重新加载热点新闻数据")
        print("help - 显示此命令帮助")
        print("stop - 退出我的热点新闻服务器")
    elif name == "stop" or name == "exit" or name == "quit" or name == "close":
        sys.exit(0)
    else:
        print("Unknown command. Type \"help\" or \"?\" for more helps.")
    return

class MyFileEventHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()

    def on_moved(self, event):
        if event.is_directory:
            print("directory moved from {0} to {1}".format(event.src_path, event.dest_path))
        else:
            print("file moved from {0} to {1}".format(event.src_path, event.dest_path))

    def on_created(self, event):
        if event.is_directory:
            print("directory created: {0}".format(event.src_path))
        else:
            print("file created: {0}".format(event.src_path))

    def on_deleted(self, event):
        if event.is_directory:
            print("directory deleted: {0}".format(event.src_path))
        else:
            print("file deleted: {0}".format(event.src_path))

    def on_modified(self, event):
        if event.is_directory:
            print("directory modified: {0}".format(event.src_path))
        else:
            print("file modified: {0}".format(event.src_path))
            if "news_data.json" in event.src_path: reload()
