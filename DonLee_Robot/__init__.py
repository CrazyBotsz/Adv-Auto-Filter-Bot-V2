#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) @AlbertEinsteinTG & MRK_YT

import os
import logging
import time

from logging.handlers import RotatingFileHandler

from .Translation import Translation
from .Simple_Config import Mo_Tech_YT

# Change Accordingly While Deploying To A VPS
APP_ID = Mo_Tech_YT.MO_TECH_YT_10
API_HASH = Mo_Tech_YT.MO_TECH_YT_11
BOT_TOKEN = Mo_Tech_YT.MO_TECH_YT_12
USER_SESSION = Mo_Tech_YT.MO_TECH_YT_16

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
