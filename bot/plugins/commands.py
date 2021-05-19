#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) @AlbertEinsteinTG

from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from bot import Translation # pylint: disable=import-error
from bot.database import Database # pylint: disable=import-error
from bot import START_MSG_BUTTON_NAME_1, START_MSG_BUTTIN_NAME_2, START_MSG_BUTTON_LINK_1, START_MSG_BUTTON_LINK_2, FILE_SENT_BUTTON_LINK, FILE_SENT_BUTTON_NAME, START_MSG_BUTTON_LINK_3, START_MSG_BUTTON_NAME_3, ENABLE_START_MSG_PIC, START_MSG_PHOTO

db = Database()
btn_name1 = START_MSG_BUTTON_NAME_1
btn_name2 = START_MSG_BUTTIN_NAME_2
btn_name3 = START_MSG_BUTTON_NAME_3
btn_link1 = START_MSG_BUTTON_LINK_1
btn_link2 = START_MSG_BUTTON_LINK_2
btn_link3 = START_MSG_BUTTON_LINK_3
file_btn_name = FILE_SENT_BUTTON_NAME
file_btn_link = FILE_SENT_BUTTON_LINK

@Client.on_message(filters.command(["start"]) & filters.private, group=1)
async def start(bot, update):
    
    try:
        file_uid = update.command[1]
    except IndexError:
        file_uid = False
    
    if file_uid:
        file_id, file_name, file_caption, file_type = await db.get_file(file_uid)
        
        if (file_id or file_type) == None:
            return
        
        caption = file_caption if file_caption != ("" or None) else ("<code>" + file_name + "</code>")
        
        if file_type == "document":
        
            await bot.send_document(
                chat_id=update.chat.id,
                document = file_id,
                caption = caption,
                parse_mode="html",
                reply_to_message_id=update.message_id,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton
                                (
                                    f"{file_btn_name}", url=f"{file_btn_link}"
                                )
                        ]
                    ]
                )
            )

        elif file_type == "video":
        
            await bot.send_video(
                chat_id=update.chat.id,
                video = file_id,
                caption = caption,
                parse_mode="html",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton
                                (
                                    f"{file_btn_name}", url=f"{file_btn_link}"
                                )
                        ]
                    ]
                )
            )
            
        elif file_type == "audio":
        
            await bot.send_audio(
                chat_id=update.chat.id,
                audio = file_id,
                caption = caption,
                parse_mode="html",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton
                                (
                                    f"{file_btn_name}", url=f"{file_btn_link}"
                                )
                        ]
                    ]
                )
            )

        else:
            print(file_type)
        
    if ENABLE_START_MSG_PIC == "yes":
        try:
            buttons = [[
                InlineKeyboardButton(f"{btn_name1}", url=f"{btn_link1}"),
                InlineKeyboardButton(f"{btn_name2}", url=f"{btn_link2}")
            ],[
                InlineKeyboardButton(f"{btn_name3}", url=f"{btn_link3}")
            ],[
                InlineKeyboardButton('Help ⚙', callback_data="help")
            ]]  
            reply_markup = InlineKeyboardMarkup(buttons)
            await bot.send_photo(
                chat_id=update.chat.id,
                photo=START_MSG_PHOTO,
                caption=Translation.START_TEXT.format(
                           update.from_user.first_name),
                reply_markup=reply_markup,
                parse_mode="html",
                reply_to_message_id=update.message_id
            )
        except:
            pass
        return
    buttons = [[
        InlineKeyboardButton(f"{btn_name1}", url=f"{btn_link1}"),
        InlineKeyboardButton(f"{btn_name2}", url=f"{btn_link2}")
    ],[
        InlineKeyboardButton(f"{btn_name3}", url=f"{btn_link3}")
    ],[
        InlineKeyboardButton('Help ⚙', callback_data="help")
    ]]
    
    reply_markup = InlineKeyboardMarkup(buttons)
    
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.START_TEXT.format(
                update.from_user.first_name),
        reply_markup=reply_markup,
        parse_mode="html",
        reply_to_message_id=update.message_id
    )


@Client.on_message(filters.command(["help"]) & filters.private, group=1)
async def help(bot, update):
    buttons = [[
        InlineKeyboardButton('Home ⚡', callback_data='start'),
        InlineKeyboardButton('About 🚩', callback_data='about')
    ],[
        InlineKeyboardButton('Close 🔐', callback_data='close')
    ]]
    
    reply_markup = InlineKeyboardMarkup(buttons)
    
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.HELP_TEXT,
        reply_markup=reply_markup,
        parse_mode="html",
        reply_to_message_id=update.message_id
    )


@Client.on_message(filters.command(["about"]) & filters.private, group=1)
async def about(bot, update):
    
    buttons = [[
        InlineKeyboardButton('Home ⚡', callback_data='start'),
        InlineKeyboardButton('Close 🔐', callback_data='close')
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.ABOUT_TEXT,
        reply_markup=reply_markup,
        disable_web_page_preview=True,
        parse_mode="html",
        reply_to_message_id=update.message_id
    )
