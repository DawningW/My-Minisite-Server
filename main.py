#!/usr/bin/env python
# coding=utf-8

import sys
import atexit
import logging

from systray import initTray, removeTray
import app

@atexit.register
def onexit():
    "退出程序"
    removeTray()
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
        # 初始化系统托盘
        initTray()
        # 运行应用
        app.run()
    except KeyboardInterrupt:
        sys.exit(0)
