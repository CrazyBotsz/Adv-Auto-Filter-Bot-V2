#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) @AlbertEinsteinTG

import re
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot import verify # pylint: disable=import-error

@Client.on_message(filters.command(["settings"]) & filters.group, group=1)
async def settings(bot, update):
    
    chat_id = update.chat.id
<<<<<<< Updated upstream
    chat_name = (remove_emoji(update.chat.title)).encode('ascii', 'ignore').decode('ascii')[:38]
=======
    user_id = update.from_user.id or None
    chat_name = remove_emoji(update.chat.title)
    chat_name = chat_name.encode('ascii', 'ignore')
    chat_name = chat_name.decode('ascii')[:38]
>>>>>>> Stashed changes

    if not verify[str(chat_id)]: # Admin List
        admin_list = []
        
<<<<<<< Updated upstream
        verify[str(update.message_id)] = user_id
        
=======
        await bot.get_chat_members(chat_id)
                
        verify[str(chat_id)] = user_id
    else:
        if not user_id in verify.get(str(chat_id)):
            return
    
>>>>>>> Stashed changes
    bot_status = await bot.get_me()
    bot_fname= bot_status.first_name
    
    text =f"<i>{bot_fname}'s</i> Settings Pannel.....\n"
    text+=f"\n<i>You Can Use This Menu To Change Connectivity And Know Status Of Your Every Connected Channel, Change Filter Types, Configure Filter Results And To Know Status Of Your Group...</i>"
    
    buttons = [
        [
            InlineKeyboardButton
                (
                    "Channels", callback_data=f"channel_list({chat_id}|{chat_name})"
                ), 
            
            InlineKeyboardButton
                (
                    "Filter Types", callback_data=f"types({chat_id}|{chat_name})"
                )
        ],
        [
            InlineKeyboardButton
                (
                    "Configure 🛠", callback_data=f"config({chat_id}|{chat_name})"
                )
        ], 
        [
            InlineKeyboardButton
                (
                    "Status", callback_data=f"status({chat_id}|{chat_name})"
                ),
            
            InlineKeyboardButton
                (
                    "About", callback_data=f"about({chat_id})"
                )
        ],
        [
            InlineKeyboardButton
                (
                    "Close 🔐", callback_data="close"
                )
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(buttons)
    
    await bot.send_message (
        
        chat_id=chat_id, 
        text=text, 
        reply_markup=reply_markup, 
        parse_mode="html",
        reply_to_message_id=update.message_id
        
        )


def remove_emoji(string):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F" 
                               u"\U0001F300-\U0001F5FF"
                               u"\U0001F680-\U0001F6FF" 
                               u"\U0001F1E0-\U0001F1FF" 
                               u"\U00002500-\U00002BEF" 
                               u"\U00002702-\U000027B0"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\ufe0f"
                               u"\u3030"
    "]+", flags=re.UNICODE)
    
    return emoji_pattern.sub(r' ', string)