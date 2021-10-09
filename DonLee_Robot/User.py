# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) @AlbertEinsteinTG
# (e) @Muhammed_RK, @Mo_Tech_YT , @Mo_Tech_Group, @MT_Botz
# Copyright permission under MIT License
# All rights reserved by PR0FESS0R-99
# License -> https://github.com/PR0FESS0R-99/DonLee_Robot/blob/main/LICENSE

from pyrogram import Client, __version__

from . import API_HASH, APP_ID, LOGGER, \
    USER_SESSION


class User(Client):
    def __init__(self):
        super().__init__(
            USER_SESSION,
            api_hash=API_HASH,
            api_id=APP_ID,
            workers=4
        )
        self.LOGGER = LOGGER

    async def start(self):
        await super().start()
        usr_bot_me = await self.get_me()
        return (self, usr_bot_me.id)

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("Bot stopped. Bye.")
