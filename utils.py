# coding=utf-8

from enum import Enum, auto
import ctypes
import os
import sys

class System(Enum):
    WINDOWS = auto()
    LINUX = auto()
    MACOS = auto()
    FREEBSD = auto()
    OTHER = auto()

def getSystem():
    if sys.platform.startswith('win32') or sys.platform.startswith('cygwin'):
        return System.WINDOWS
    elif sys.platform.startswith('linux'):
        return System.LINUX
    elif sys.platform.startswith('darwin'):
        return System.MACOS
    elif sys.platform.startswith('freebsd'):
        return System.FREEBSD
    return System.OTHER

def getHostFile():
    if getSystem() == System.WINDOWS:
        return os.getenv("SYSTEMROOT") + "\System32\drivers\etc\hosts"
    else:
        return "/etc/hosts"

def showWindow():
    if getSystem() == System.WINDOWS:
        whnd = ctypes.windll.kernel32.GetConsoleWindow()
        if whnd != 0:
            ctypes.windll.user32.ShowWindow(whnd, 5) # win32con.SW_SHOW
            ctypes.windll.kernel32.CloseHandle(whnd)
    return

def hideWindow():
    if getSystem() == System.WINDOWS:
        whnd = ctypes.windll.kernel32.GetConsoleWindow()
        if whnd != 0:
            ctypes.windll.user32.ShowWindow(whnd, 0) # win32con.SW_HIDE
            ctypes.windll.kernel32.CloseHandle(whnd)
    return
