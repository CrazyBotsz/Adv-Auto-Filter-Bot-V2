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

@Client.on_callback_query(filters.regex(r"status\((.+)\)"), group=2)
async def cb_status(bot, update: CallbackQuery):
    """
    A Callback Funtion For Showing Overall Status Of A Group
    """
    global CHAT_DETAILS
    query_data = update.data
    chat_id = update.message.chat.id
    chat_name = remove_emoji(update.message.chat.title)
    user_id = update.from_user.id
    
    chat_dict = CHAT_DETAILS.get(str(chat_id))
    chat_admins = chat_dict.get("admins") if chat_dict != None else None

    if ( chat_dict or chat_admins ) == None: # Make Admin's ID List
        chat_admins = await admin_list(chat_id, bot, update)

    if user_id not in chat_admins:
        return
    
    chat_id = re.findall(r"status\((.+)\)", query_data)[0]
    
    total_filters, total_chats, total_achats = await db.status(chat_id)
    
    text = f"<b><i>Status Of {chat_name}</i></b>\n"
    text += f"\n<b>Total Connected Chats:</b> <code>{total_chats}</code>\n"
    text += f"\n<b>Total Active Chats:</b> <code>{total_achats}</code>\n"
    text += f"\n<b>Total Filters:</b> <code>{total_filters}</code>"
    
    buttons = [
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
    ]
    
    reply_markup = InlineKeyboardMarkup(buttons)
    
    await update.message.edit_text(
        text, reply_markup=reply_markup, parse_mode="html"
    )


