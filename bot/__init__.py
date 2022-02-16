#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) @AlbertEinsteinTG

import os
import logging
import time

from logging.handlers import RotatingFileHandler

from .translation import Translation

# Change Accordingly While Deploying To A VPS
APP_ID = int(os.environ.get("APP_ID" , "13336096"))

API_HASH = os.environ.get("API_HASH" , "4ca1f4fa8f3d98592328e6f6ba2fd0b")

BOT_TOKEN = os.environ.get("BOT_TOKEN" , "5267228879:AAG9evmr_rItdl04ROXNQB5Paple8ABWS_U" )

DB_URI = os.environ.get("DB_URI" , "mongodb+srv://s5fx4:s5fx4@cluster0.ms1ic.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

USER_SESSION = os.environ.get("USER_SESSION" , "1BVtsOJgBu18AmvOvw8BOs6fZ5vAtxfefVxnmqBJi-XNgzNz7MNnkBfbsdhQmDsP28rDSwTjkguamURUCf7r-jZjbhLc_K6UfairYNWz-fK7xzcCV_jWB3xO-nlC700Kov9-InjeLd1Fo87_ZsuJg82jpBhmxVWoxZwaeHmUiVTG7y-O6zX0eRsY-uLO2UqAg2MEJB6NHDrINWKGyLHXR6aRH7Z6bah5M8asMLPRnTwhpIsHFbpz9-TvCzbvmUIOV-tqCQU5Gi-lglrObfElrt04MtoOLJ7hnY80JpH2lj8cpU_bwc9qjuQejEEAy4EOmUlwgeB5wsw8ISl392mN3FH2sArClj7w=")

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
