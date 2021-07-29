import re
import time
import asyncio

from pyrogram import Client, filters
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from . import (
    FIND, 
    recacher,
    Database,
    admin_list,
    ACTIVE_CHATS,
    CHAT_DETAILS,
    INVITE_LINK, 
    remove_emoji,
    gen_invite_links,
)

db = Database()

@Client.on_callback_query(filters.regex(r"channel_list\((.+)\)"), group=2)
async def cb_channel_list(bot, update: CallbackQuery):    
    """
    A Callback Funtion For Displaying All Channel List And Providing A Menu To Navigate
    To Every COnnect Chats For Furthur Control
    """
    global CHAT_DETAILS
    query_data = update.data
    chat_id = update.message.chat.id
    chat_name = remove_emoji(update.message.chat.title)
    chat_name = chat_name.encode('ascii', 'ignore').decode('ascii')[:35]
    user_id = update.from_user.id

    chat_dict = CHAT_DETAILS.get(str(chat_id))
    chat_admins = chat_dict.get("admins") if chat_dict != None else None

    if ( chat_dict or chat_admins ) == None: # Make Admin's ID List
        chat_admins = await admin_list(chat_id, bot, update)

    if user_id not in chat_admins:
        return

    chat_id =  re.findall(r"channel_list\((.+)\)", query_data)[0]
    
    text = "<i>Semms Like You Dont Have Any Channel Connected...</i>\n\n<i>Connect To Any Chat To Continue With This Settings...</i>"
    
    db_list = await db.find_chat(int(chat_id))
    
    channel_id_list = []
    channel_name_list = []
    
    if db_list:
        for x in db_list["chat_ids"]:
            channel_id = x["chat_id"]
            channel_name = x["chat_name"]
            
            try:
                if (channel_id == None or channel_name == None):
                    continue
            except:
                break
            
            channel_name = remove_emoji(channel_name).encode('ascii', 'ignore').decode('ascii')[:35]
            channel_id_list.append(channel_id)
            channel_name_list.append(channel_name)
        
    buttons = []

    # For Future Update (Little Help Needed😪)
    # buttons.append([
    #     InlineKeyboardButton
    #         (
    #             "Global Connections", callback_data=f"global({chat_id})"
    #         )
    # ])


    buttons.append(
        [
            InlineKeyboardButton
                (
                    "🔙 Back", callback_data="settings"
                ),
            
            InlineKeyboardButton
                (
                    "Close 🔐", callback_data="close"
                )
        ]
    ) 

    if channel_name_list:
        
        text=f"<i>List Of Connected Channels With <code>{chat_name}</code> With There Settings..</i>\n"
    
        for x in range(1, (len(channel_name_list)+1)):
            text+=f"\n<code>{x}. {channel_name_list[x-1]}</code>\n"
    
        text += "\nChoose Appropriate Buttons To Navigate Through Respective Channels"
    
        
        btn_key = [
            "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟", 
            "1️⃣1️⃣", "1️⃣2️⃣", "1️⃣3️⃣", "1️⃣4️⃣", "1️⃣5️⃣", "1️⃣6️⃣", "1️⃣7️⃣", 
            "1️⃣8️⃣", "1️⃣9️⃣", "2️⃣0️⃣" # Just In Case 😂🤣
        ]
    
        for i in range(1, (len(channel_name_list) + 1)): # Append The Index Number of Channel In Just A Single Line
            if i == 1:
                buttons.insert(0,
                    [
                    InlineKeyboardButton
                        (
                            btn_key[i-1], callback_data=f"info({channel_id_list[i-1]}|{channel_name_list[i-1]})"
                        )
                    ]
                )
        
            else:
                buttons[0].append(
                    InlineKeyboardButton
                        (
                            btn_key[i-1], callback_data=f"info({channel_id_list[i-1]}|{channel_name_list[i-1]})"
                        )
                )
    
    
    reply_markup=InlineKeyboardMarkup(buttons)

    await update.message.edit_text(
            text = text,
            reply_markup=reply_markup,
            parse_mode="html"
        )



@Client.on_callback_query(filters.regex(r"info\((.+)\)"), group=2)
async def cb_info(bot, update: CallbackQuery):
    """
    A Callback Funtion For Displaying Details Of The Connected Chat And Provide
    Ability To Connect / Disconnect / Delete / Delete Filters of That Specific Chat
    """
    global CHAT_DETAILS
    query_data = update.data
    chat_id = update.message.chat.id
    user_id = update.from_user.id
    
    chat_dict = CHAT_DETAILS.get(str(chat_id))
    chat_admins = chat_dict.get("admins") if chat_dict != None else None

    if ( chat_dict or chat_admins ) == None: # Make Admin's ID List
        chat_admins = await admin_list(chat_id, bot, update)

    if user_id not in chat_admins:
        return

    channel_id, channel_name = re.findall(r"info\((.+)\)", query_data)[0].split("|", 1)
    
    f_count = await db.cf_count(chat_id, int(channel_id)) 
    active_chats = await db.find_active(chat_id)

    if active_chats: # Checks for active chats connected to a chat
        dicts = active_chats["chats"]
        db_cids = [ int(x["chat_id"]) for x in dicts ]
        
        if int(channel_id) in db_cids:
            active_chats = True
            status = "Connected"
            
        else:
            active_chats = False
            status = "Disconnected"
            
    else:
        active_chats = False
        status = "Disconnected"

    text=f"<i>Info About <b>{channel_name}</b></i>\n"
    text+=f"\n<i>Channel Name:</i> <code>{channel_name}</code>\n"
    text+=f"\n<i>Channel ID:</i> <code>{channel_id}</code>\n"
    text+=f"\n<i>Channel Files:</i> <code>{f_count}</code>\n"
    text+=f"\n<i>Current Status:</i> <code>{status}</code>\n"


    if active_chats:
        buttons = [
                    [
                        InlineKeyboardButton
                            (
                                "🚨 Disconnect 🚨", callback_data=f"warn({channel_id}|{channel_name}|disconnect)"
                            ),
                        
                        InlineKeyboardButton
                            (
                                "Delete ❌", callback_data=f"warn({channel_id}|{channel_name}|c_delete)"
                            )
                    ]
        ]

    else:
        buttons = [ 
                    [
                        InlineKeyboardButton
                            (
                                "💠 Connect 💠", callback_data=f"warn({channel_id}|{channel_name}|connect)"
                            ),
                        
                        InlineKeyboardButton
                            (
                                "Delete ❌", callback_data=f"warn({channel_id}|{channel_name}|c_delete)"
                            )
                    ]
        ]

    buttons.append(
            [
                InlineKeyboardButton
                    (
                        "Delete Filters ⚠", callback_data=f"warn({channel_id}|{channel_name}|f_delete)"
                    )
            ]
    )
    
    buttons.append(
            [
                InlineKeyboardButton
                    (
                        "🔙 Back", callback_data=f"channel_list({chat_id})"
                    )
            ]
    )

    reply_markup = InlineKeyboardMarkup(buttons)
        
    await update.message.edit_text(
            text, reply_markup=reply_markup, parse_mode="html"
        )


# 
    # @Client.on_callback_query(filters.regex(r"^global\((.+)\)"), group=2)
    # async def cb_global_chats(bot, update:CallbackQuery):
    #     """
    #     A Callback Funtion For Displaying Details Of All The Connected Chat And Provide
    #     Ability To Connect, Disconnect, Delete, Delete Filters of, All Connected Chat In
    #     1 Go
    #     """
    #     global CHAT_DETAILS
        
    #     chat_id = update.message.chat.id
    #     chat_name = update.message.chat.title
    #     user_id = update.from_user.id
        
    #     chat_dict = CHAT_DETAILS.get(str(chat_id))
    #     chat_admins = chat_dict.get("admins") if chat_dict != None else None

    #     if ( chat_dict or chat_admins ) == None: # Make Admin's ID List
    #         chat_admins = await admin_list(chat_id, bot, update)

    #     if user_id not in chat_admins:
    #         return
        
    #     f_count = await db.tf_count(chat_id) 
    #     connected_chats = await db.find_chat(chat_id)
    #     active_chats = await db.find_active(chat_id)
        
    #     db_cids = None
    #     db_cnames = None
    #     total_chats = 0
        
    #     if connected_chats: # Checks for active chats connected to a chat
    #         dicts = connected_chats["chat_ids"]
    #         adicts = active_chats["chats"]
    #         adb_cids = [ int(x["chat_id"]) for x in adicts ]
    #         db_cids = []
    #         db_cnames = []
    #         for x in dicts:
    #             cid = x["chat_id"]
    #             cname = x["chat_name"]
    #             print(cname)
                
    #             db_cids.append(cid)
    #             if cid in adb_cids:
    #                 cname + " (A)"
    #             db_cnames.append(cname)

    #             print(db_cnames)
        
    #         total_chats = len(db_cids)

    #     text=f"<i>Info About All Connected Of <b>{chat_name}</b></i>\n"
    #     text+=f"\n<i>Total Connected Chats:</i> {total_chats}\n"
        
    #     text+=f"\n<i>Channel Names:</i>\n"
        
    #     for y in db_cnames:
    #         text+=f"\n                   <code>{y}</code>"
            
    #     text+=f"\n<i>Channel ID's:</i>\n"
        
    #     for z in db_cids:
    #         text+=f"\n                 <code>{z}</code>"
        
    #     text+=f"\n<i>Total Files In DB:</i> <code>{f_count}</code>\n"



    #     buttons = [ 
    #                 [
    #                     InlineKeyboardButton
    #                         (
    #                             "💠 Connect All 💠", callback_data=f"warn({chat_id}|conn|gcmds)"
    #                         ),
                        
    #                     InlineKeyboardButton
    #                         (
    #                             "🚨 Disconnect All 🚨", callback_data=f"warn({chat_id}|disconn|gcmds)"
    #                         )
    #                 ]
    #     ]


    #     buttons.append(
    #             [                    
    #                 InlineKeyboardButton
    #                     (
    #                         "Delete All Chats ❌", callback_data=f"warn({chat_id}|c_delete|gcmds)"
    #                     )
    #             ]
    #     )


    #     buttons.append(
    #             [
    #                 InlineKeyboardButton
    #                     (
    #                         "Delete All Filters ⚠", callback_data=f"warn({chat_id}|f_delete|gcmds)"
    #                     )
    #             ]
    #     )
        
    #     buttons.append(
    #             [
    #                 InlineKeyboardButton
    #                     (
    #                         "🔙 Back", callback_data=f"channel_list({chat_id})"
    #                     )
    #             ]
    #     )

    #     reply_markup = InlineKeyboardMarkup(buttons)
            
    #     await update.message.edit_text(
    #             text, reply_markup=reply_markup, parse_mode="html"
    #         )

