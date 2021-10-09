# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) @AlbertEinsteinTG
# (e) @Muhammed_RK, @Mo_Tech_YT , @Mo_Tech_Group, @MT_Botz
# Copyright permission under MIT License
# All rights reserved by PR0FESS0R-99
# License -> https://github.com/PR0FESS0R-99/DonLee_Robot/blob/main/LICENSE

import os
import logging
import time

from logging.handlers import RotatingFileHandler

from .Translation import Translation

# Change Accordingly While Deploying To A VPS
# API_ID From https://youtu.be/5eEsvLAKVc0
APP_ID = int(os.environ.get("APP_ID"))
# API_HASH From https://youtu.be/5eEsvLAKVc0
API_HASH = os.environ.get("API_HASH")
# BOT_TOKEN From https://youtu.be/cB4UduCcNWs
BOT_TOKEN = os.environ.get("BOT_TOKEN")
# DD_URI From https://youtu.be/cB4UduCcNWs
DB_URI = os.environ.get("DB_URI")
# USER_SESSION From https://youtu.be/WUN_12-dYOM
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
