#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) @AlbertEinsteinTG

import re
import time
import asyncio
import pyrogram

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.errors import UserAlreadyParticipant, FloodWait
from pyrogram import Client, filters

from bot.bot import Bot
from bot.translation import Translation
from bot.plugins.database import Database

db = Database () 
result = []

@Client.on_message(filters.command("connect") & filters.group)
async def connect(bot: Bot, update):

    group_id = update.chat.id
    text = update.text.split(None, 1)
    
    x = await bot.get_chat_member(group_id, update.from_user.id)
    
    if x.status == "member":
        return
    
    if len(text) != 2:
        return
    
    channel_id = int(text[1])
    
    conn_hist = await db.find_connections(group_id)
    
    if conn_hist: #TODO: Better Way!? 

        channel1 = int(conn_hist["channel_ids"]["channel1"]) if conn_hist["channel_ids"]["channel1"] else None
        channel2 = int(conn_hist["channel_ids"]["channel2"]) if conn_hist["channel_ids"]["channel2"] else None
        channel3 = int(conn_hist["channel_ids"]["channel3"]) if conn_hist["channel_ids"]["channel3"] else None
    
    else:
        channel1 = None
        channel2 = None
        channel3 = None
    
    if channel_id in (channel1, channel2, channel3):
        await bot.send_message(
            chat_id=group_id,
            text="Group Is Aldready Connected With This Channel",
            reply_to_message_id=update.message_id
        )
        return
    
    if None not in (channel1, channel2, channel3):
        await bot.send_message(
            chat_id=group_id,
            text="Group Reached Its Connection Limit...\nDisconnect From Any Channel To Continue",
            reply_to_message_id=update.message_id
        )
        return

    if channel1 is None:
        channel1 = channel_id
    
    elif channel2 is None:
        channel2 = channel_id
    
    elif channel3 is None:
        channel3 = channel_id

    # Export Invite Link For Userbot
    try:
        join_link = await bot.export_chat_invite_link(channel_id)
    except Exception as e:
        print(e) 
        await bot.send_message(
            chat_id=group_id,
            text=f"Make Sure I'm Admin In <code>{channel_id}</code> And Have Permission - `Invite Users via Link`",
            parse_mode="html",
            reply_to_message_id=update.message_id
        )
        return
    
    user = await bot.USER.get_me()
    user_id = user.id
    
    # Tries To Unban The UserBot
    try:
        await bot.unban_chat_member(
            chat_id=channel_id,
            user_id=user_id
        )
    except Exception as e:
        pass
    
    # Userbot Joins The Channel
    try:
        await bot.USER.join_chat(join_link)
    except UserAlreadyParticipant:
        pass
    except Exception as e:
        print (e)
        
        await bot.send_message(
            chat_id=group_id,
            text=f"My Userbot `@{user.username}` Cant join Your Channel Make Sure He Is Not Banned There..",
            reply_to_message_id=update.message_id
        )
        return
    
    chat_name = await bot.get_chat(channel_id) 
    responce = await db.add_connections(group_id, channel1, channel2, channel3)

    if responce:
        await bot.send_message(
            chat_id=group_id,
            text=f"Sucessfully Connected To <code>{chat_name.title}</code>",
            parse_mode="html",
            reply_to_message_id=update.message_id
        )
        return
    
    else:
        await bot.send_message(
            chat_id=group_id,
            text=f"Having Problem While Connecting...Report @CrazyBotsz",
            reply_to_message_id=update.message_id
        )
        return


@Client.on_message(filters.command("disconnect") & filters.group)
async def disconnect(bot, update):
    group_id = update.chat.id
    text = update.text.split(None, 1)
    
    x = await bot.get_chat_member(group_id, update.from_user.id)
    
    if x.status == "member":
        return
    
    if len(text) != 2:
        return
    
    channel_id = int(text[1])
    
    conn_hist = await db.find_connections(group_id)
    
    if conn_hist:
        channel1 = int(conn_hist["channel_ids"]["channel1"]) if conn_hist["channel_ids"]["channel1"] else None
        channel2 = int(conn_hist["channel_ids"]["channel2"]) if conn_hist["channel_ids"]["channel2"] else None
        channel3 = int(conn_hist["channel_ids"]["channel3"]) if conn_hist["channel_ids"]["channel3"] else None
    
    else:
        await bot.send_message(
            chat_id=group_id,
            text="Group Is Not Connected With Any Channel",
            reply_to_message_id=update.message_id
        )
        return
    
    if channel_id not in (channel1, channel2, channel3):
        await bot.send_message(
            chat_id=group_id,
            text=f"Group Is Not Connected With This Chat : <code>{channel_id}</code>",
            parse_mode="html", 
            reply_to_message_id=update.message_id
        )
        return
    
    if channel1 == channel_id:
        channel1 = None
    
    elif channel2 == channel_id:
        channel2 = None
    
    elif channel3 == channel_id:
        channel3 = None

    try:
        await bot.USER.leave_chat(channel_id)
    except:
        pass
    
    chat_name = await bot.get_chat(channel_id)
    
    try:
        await bot.leave_chat(channel_id)
    except:
        pass
    
    responce = await db.add_connections(group_id, channel1, channel2, channel3)

    if responce:
        await bot.send_message(
            chat_id=group_id,
            text=f"Sucessfully Disconnected From <code>{chat_name.title}</code>",
            parse_mode="html", 
            reply_to_message_id=update.message_id
        )
        return
    
    else:
        await bot.send_message(
            chat_id=group_id,
            text=f"Having Problem While Disconnecting...Report @CrazyBotsz",
            reply_to_message_id=update.message_id
        )
        return


@Client.on_message(filters.command("delall") & filters.group)
async def delall(bot, update):
    group_id = update.chat.id

    x = await bot.get_chat_member(group_id, update.from_user.id)
    
    if x.status == "creator":
        pass
    else:
        print(x.status) 
        return
    print("Ok") 
    conn_hist = await db.find_connections(group_id)
    print(conn_hist) 
    if conn_hist:
        channel1 = int(conn_hist["channel_ids"]["channel1"]) if conn_hist["channel_ids"]["channel1"] else None
        channel2 = int(conn_hist["channel_ids"]["channel2"]) if conn_hist["channel_ids"]["channel2"] else None
        channel3 = int(conn_hist["channel_ids"]["channel3"]) if conn_hist["channel_ids"]["channel3"] else None
        channels = [channel1, channel2, channel3]
    else:
        return
    
    for channel in channels:
        if channel == None:
            continue
        try:
            await bot.USER.leave_chat(channel)
        except:
            pass
        try:
            await bot.leave_chat(channel)
        except:
            pass
    
    responce = await db.delete_connections(group_id)
    
    if responce:
        await bot.send_message(
            chat_id=group_id,
            text=f"Sucessfully Disconnected From All Chats",
            reply_to_message_id=update.message_id
        )
        return


@Client.on_message(filters.text & filters.group)
async def auto_filter (bot, update):
    
    group_id = update.chat.id
    
    if re.findall("((^\/|^,|^\.|^[\U0001F600-\U000E007F]).*)", update.text):
        return
    
    query = update.text

    if len(query) < 3:
        return
    
    results = []

    conn_hist = await db.find_connections(group_id)
    
    if conn_hist: # TODO: Better Way!? 😕
        channel1 = int(conn_hist["channel_ids"]["channel1"]) if conn_hist["channel_ids"]["channel1"] else None
        channel2 = int(conn_hist["channel_ids"]["channel2"]) if conn_hist["channel_ids"]["channel2"] else None
        channel3 = int(conn_hist["channel_ids"]["channel3"]) if conn_hist["channel_ids"]["channel3"] else None
        channels = [channel1, channel2, channel3]
    else:
        return
    
    for channel in channels:
        if channel == None:
            continue
        
        async for msgs in bot.USER.search_messages(chat_id=channel, query=query, filter="document", limit=150):

            if msgs.video:
                name = msgs.video.file_name
            elif msgs.document:
                name = msgs.document.file_name
            elif msgs.audio:
                name = msgs.audio.file_name
            else:
                name = None

            link = msgs.link
            
            if name is not None:
                results.append([InlineKeyboardButton(name, url=link)])


        async for msgs in bot.USER.search_messages(chat_id=channel, query=query, filter="video", limit=150):

            if msgs.video:
                name = msgs.video.file_name
            elif msgs.document:
                name = msgs.document.file_name
            elif msgs.audio:
                name = msgs.audio.file_name
            else:
                name = None

            link = msgs.link
            
            if name is not None:
                results.append([InlineKeyboardButton(name, url=link)])

    if len(results) == 0:
        # await bot.send_message(
        #     chat_id = update.chat.id,
        #     text=f"Couldn't Find A Matching Result",
        #     reply_to_message_id=update.message_id
        # )
        return
    
    else:
        global result
        result = []
        result += [results[i * 30 :(i + 1) * 30 ] for i in range((len(results) + 30 - 1) // 30 )]
        
        if len(results) >30:
            result[0].append([InlineKeyboardButton("Next ⏩", callback_data=f"0 | {update.from_user.id} | next_btn")])

        reply_markup = InlineKeyboardMarkup(result[0])

        await bot.send_message(
            chat_id = update.chat.id,
            text=f"Found {(len(results))} Results For Query: <code>{query}</code>",
            reply_markup=reply_markup,
            parse_mode="html",
            reply_to_message_id=update.message_id
        )

@Client.on_callback_query()
async def cb_handler(bot, query:CallbackQuery, group=1):
    cb_data = query.data
    
    if cb_data == "start":
        buttons = [[
            InlineKeyboardButton('My Dev 👨‍🔬', url='https://t.me/AlbertEinstein_TG'),
            InlineKeyboardButton('Source Code 🧾', url ='https://github.com/AlbertEinsteinTG/Adv-Auto-Filter-Bot')
        ],[
            InlineKeyboardButton('Support 🛠', url='https://t.me/CrazyBotszGrp')
        ],[
            InlineKeyboardButton('Help ⚙', callback_data="help")
        ]]
    
        reply_markup = InlineKeyboardMarkup(buttons)
        
        await query.message.edit_text(
            Translation.START_TEXT.format(query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode="html",
            disable_web_page_preview=True
        )
    
    elif cb_data == "help":
        buttons = [[
            InlineKeyboardButton('Home ⚡', callback_data='start'),
            InlineKeyboardButton('About 🚩', callback_data='about')
        ],[
            InlineKeyboardButton('Close 🔐', callback_data='close')
        ]]
    
        reply_markup = InlineKeyboardMarkup(buttons)
        
        await query.message.edit_text(
            Translation.HELP_TEXT,
            reply_markup=reply_markup,
            parse_mode="html",
            disable_web_page_preview=True
        )
    
    elif cb_data == "about": 
        buttons = [[
            InlineKeyboardButton('Home ⚡', callback_data='start'),
            InlineKeyboardButton('Close 🔐', callback_data='close')
        ]]
        
        reply_markup = InlineKeyboardMarkup(buttons)
        
        await query.message.edit_text(
            Translation.ABOUT_TEXT,
            reply_markup=reply_markup,
            parse_mode="html",
            disable_web_page_preview=True
        )
    
    elif cb_data == "close":
        await query.message.delete()


    elif "btn" in cb_data :
        cb_data = cb_data.split("|") 

        index_val = cb_data[0]
        user_id = cb_data[1]
        data = cb_data[2].strip()
    
        if int(query.from_user.id) != int(user_id):
            await query.answer("You Arent Worth To Do That!!",show_alert=True) # Lol😆
            return
        else:
            pass
    

        if data == "next_btn":
            index_val = int(index_val) + 1
        elif data == "back_btn":
            index_val = int(index_val) - 1
        
        try:
            temp_results = result[index_val].copy()
        except IndexError:
            return # Quick Fix🏃🏃
        except Exception as e:
            print(e)
            return
    
        if int(index_val) == (len(result) -1) or int(index_val) == 10: # Max 10 Page
            temp_results.append([
                InlineKeyboardButton("⏪ Back", callback_data=f"{index_val} | {query.from_user.id} | back_btn")
            ])
    
        elif int(index_val) == 0:
            pass
    
        else:
            temp_results.append([
                InlineKeyboardButton("⏪ Back", callback_data=f"{index_val} | {query.from_user.id} | back_btn"),
                InlineKeyboardButton("Next ⏩", callback_data=f"{index_val} | {query.from_user.id} | next_btn")
            ])
    
        reply_markup = InlineKeyboardMarkup(temp_results)
        
        if index_val == 0:
           text=f"Found {(len(result)*30 - (30 - len(result [-1])))} Results For Query"
        else:
           text=f"Page `{index_val}` For Your Query....."
        
        time.sleep(1) # Just A Mesure To Prevent Flood Wait🙁
        try:
            await query.message.edit(
                    text,
                    reply_markup=reply_markup,
                    parse_mode="md"
            )
        except FloodWait as f:
            await asyncio.sleep(f.x)
            await query.message.edit(
                    text,
                    reply_markup=reply_markup,
                    parse_mode="md"
            )
