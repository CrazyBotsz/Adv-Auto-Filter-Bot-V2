#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) @AlbertEinsteinTG & Dark Angel

import os
import logging
import time

from logging.handlers import RotatingFileHandler

from .translation import Translation

# Custom vars
START_MSG = os.environ.get("START_MSG", "<b>Hey {}!!</b>\n<i>Am Just A Advance Auto Filter Bot....😉\nJust Add Me To Your Group And Channel And Connect Them And See My Pevers 🔥🔥😝\nFor More Details Click Help Button Below..\n@CrazyBotsz</i>")
START_MSG_BUTTON_NAME_1 = os.environ.get("START_MSG_BUTTON_NAME_1", "Developers")
START_MSG_BUTTIN_NAME_2 = os.environ.get("START_MSG_BUTTON_NAME_2", "Source Code 🧾")
START_MSG_BUTTON_NAME_3 = os.environ.get("START_MSG_BUTTON_NAME_3", "Support 🛠")
START_MSG_BUTTON_LINK_1 = os.environ.get("START_MSG_BUTTIN_LINK_1", "https://t.me/CrazyBotsz")
START_MSG_BUTTON_LINK_2 = os.environ.get("START_MSG_BUTTON_LINK_2", "https://github.com/AlbertEinsteinTG/Adv-Auto-Filter-Bot-V2")
START_MSG_BUTTON_LINK_3 = os.environ.get("START_MSG_BUTTON_LINK_3", "https://t.me/CrazyBotszGrp")
FILE_SENT_BUTTON_NAME = os.environ.get("FILE_SENT_BUTTON_NAME", "Developers")
FILE_SENT_BUTTON_LINK = os.environ.get("FILE_SENT_BUTTON_LINK", "https://t.me/CrazyBotsz")
ENABLE_START_MSG_PIC = os.environ.get("ENABLE_START_MSG_PIC", "no").lower()
START_MSG_PHOTO = os.environ.get("START_MSG_PHOTO", "https://telegra.ph/file/ed2aadd877a8b44069180.jpg")


# Change Accordingly While Deploying To A VPS
APP_ID = int(os.environ.get("APP_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
DB_URI = os.environ.get("DB_URI")
USER_SESSION = os.environ.get("USER_SESSION")
VERIFY = {}

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            "autofilterbot.txt",
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

start_uptime = time.time()


def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
