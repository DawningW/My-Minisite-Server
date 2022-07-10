#coding= utf-8

import os
import logging
import configparser

parser = configparser.ConfigParser()

if not os.path.exists("./settings.ini"):
    logging.info("Can't find settings. Creating settings.ini.")
    parser.set("DEFAULT", "host", "127.0.0.1")
    parser.set("DEFAULT", "port", "80")
    parser.set("DEFAULT", "website", "http://yourserver.com")
    parser.set("DEFAULT", "silent", "false")
    parser.set("DEFAULT", "allow_webspiders", "false")
    save()

def load():
    logging.info("Loading settings from settings.ini.")
    parser.read("./settings.ini")
    return

def save():
    logging.info("Saving settings to settings.ini.")
    with open("./settings.ini", "w") as configFile:
        parser.write(configFile)
    return
