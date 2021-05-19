#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) @AlbertEinsteinTG & Dark Angel

import os
import logging
import time

from logging.handlers import RotatingFileHandler

from .translation import Translation

# Custom vars
START_MSG = os.environ.get("START_MSG", """<b>Hey {}!!</b>
<i>Am Just A Advance Auto Filter Bot....😉
Just Add Me To Your Group And Channel And Connect Them And See My Pevers 🔥🔥😝
For More Details Click Help Button Below..
@CrazyBotsz
</i>""")
START_MSG_BUTTON_NAME_1 = os.environ.get("START_MSG_BUTTON_NAME_1", "Developers")
START_MSG_BUTTIN_NAME_2 = os.environ.get("START_MSG_BUTTON_NAME_2", "Source Code 🧾")
START_MSG_BUTTON_LINK_1 = os.environ.get("START_MSG_BUTTIN_LINK_1", "https://t.me/CrazyBotsz")
START_MSG_BUTTON_LINK_2 = os.environ.get("START_MSG_BUTTON_LINK_2", "https://github.com/AlbertEinsteinTG/Adv-Auto-Filter-Bot-V2")

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
