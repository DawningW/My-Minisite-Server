# coding=utf-8

import os
import threading
import logging
import utils

trayThread = None
tray = None
show = True

def initTray():
    "初始化系统托盘线程"
    logging.info("Start a new thread to manage system tray.")
    global trayThread
    trayThread = threading.Thread(target = runTray, daemon = True)
    trayThread.start()
    return

def runTray():
    "添加系统托盘"
    global tray
    if utils.getSystem() == utils.System.WINDOWS:
        from SysTrayIcon import SysTrayIcon
        logging.info("Init system tray for Windows.")
        menuOptions = (("显示/隐藏", None, onOptionClicked), ("退出", None, onOptionClicked))
        tray = SysTrayIcon("./icon.ico", "我的热点新闻服务器", onTrayClicked, menuOptions)
        tray.loop()
    elif utils.getSystem() == utils.System.LINUX:
        logging.info("System tray doesn't support Linux.")
    elif utils.getSystem() == utils.System.MACOS:
        logging.info("System tray doesn't support MacOS.")
    else:
        logging.info("System tray doesn't support this system.")
    return

def removeTray():
    "移除系统托盘"
    global tray
    if tray is not None:
        if utils.getSystem() == utils.System.WINDOWS:
            tray.close()
        tray = None
    return

def onTrayClicked():
    "托盘被点击"
    global show
    if show:
        utils.hideWindow()
    else:
        utils.showWindow()
    show = not show
    return

def onOptionClicked(id):
    "托盘菜单选项被点击"
    if id == 0:
        onTrayClicked()
    elif id == 1:
        # _thread.interrupt_main() # 读取输入时好像无效
        removeTray()
        os._exit(0)
    return
