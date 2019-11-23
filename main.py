# coding=utf-8

import ctypes
import sys

from app import main

def isadmin():
    "检查管理员权限"
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# 主程序
if __name__ == "__main__":
    # 检查权限
    if isadmin():
        main()
    else:
        if len(sys.argv) >= 2 and sys.argv[1] == "debug":
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__ + " debug", None, 1)
        else:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, "", None, 1)
