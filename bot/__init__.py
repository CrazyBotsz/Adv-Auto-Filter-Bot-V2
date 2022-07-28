#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) @AlbertEinsteinTG

import os
import logging
import time

from logging.handlers import RotatingFileHandler

from .translation import Translation

# Change Accordingly While Deploying To A VPS
APP_ID = int(os.environ.get("6766195"))

API_HASH = os.environ.get("95900e1df408a32d044c1939a2ba4fd9")

BOT_TOKEN = os.environ.get("5498939115:AAHT8YDsRcL9SDaOYOjufOOAQLGJ_jX6Kw4")

DB_URI = os.environ.get("mongodb+srv://perera51:perera51@cluster0.xhzyav3.mongodb.net/?retryWrites=true&w=majority")

USER_SESSION = os.environ.get("BQAxplszMOj3yZ3iGdI43K_nZT7ww7LuXvRpOhBjFPU-iNP45lVCd2evQ6CxaaO2HHMRmCBHgxNCDpJjD5qjTMJKzaO80WpH4pMVwdLs6Cdfs3iO1bjQRFwXUz5W14BG0FCvx3nuhqr7R8oRSuh7SEp6x3m-NdFz-kX5aM_oCIXXJtoQlEn2ad6bFAbKBe9cko0FR83hKpG24BDKa7sv7JSQyeS5-PDdnYgpGQYMdf_4Wl8Ue-SAtIFZ_Q6GQ36b-zU46E5rCB76F82Sh2y2_Ik7Q8wlt8Jo1lfAlE9VDkizmqfKFuiUSycQWZFElXrRMrLvoPnKrzCwC8Ract0hCPwYAAAAAG5wiOcA")

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
