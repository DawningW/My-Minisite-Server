#!/usr/bin/env python3
# coding=utf-8

import sys
import atexit
import logging

import config
import systraymgr
import app

@atexit.register
def onexit():
    "退出程序"
    systraymgr.removeTray()
    app.close()
    logging.info("Shut down my minisite server. Thanks for your using.")
    return

# 程序入口
if __name__ == "__main__":
    try:
        # 配置日志
        logging.basicConfig(filename = "./latest.log", filemode = "w", level = logging.INFO)
        logging.getLogger().addHandler(logging.StreamHandler())
        logging.info("Welcome to my minisite server. Author: wc.")
        # 加载配置文件
        config.load()
        if config.parser.getboolean("DEFAULT", "silent"):
            systraymgr.onTrayClicked()
        # 初始化系统托盘
        systraymgr.initTray()
        # 运行应用
        app.run()
    except KeyboardInterrupt:
        sys.exit(0)
