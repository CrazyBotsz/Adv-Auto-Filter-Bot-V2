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


@Client.on_callback_query(filters.regex(r"types\((.+)\)"), group=2)
async def cb_types(bot, update: CallbackQuery):
    """
    A Callback Funtion For Changing The Result Types To Be Shown In While Sending Results
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

    chat_id = re.findall(r"types\((.+)\)", query_data)[0]
    
    _types = await db.find_chat(int(chat_id))
    
    text=f"<i>Filter Types Enabled/Disbled In <code>{chat_name}</code></i>\n"
    
    _types = _types["types"]
    vid = _types["video"]
    doc = _types["document"]
    aud = _types["audio"]
    
    buttons = []
    
    if vid:
        text+="\n<i><b>Video Index:</b> Enabled</i>\n"
        v_e = "✅"
        vcb_data = f"toggle({chat_id}|video|False)"
    
    else:
        text+="\n<i><b>Video Index:</b> Disabled</i>\n"
        v_e="❎"
        vcb_data = f"toggle({chat_id}|video|True)"

    if doc:
        text+="\n<i><b>Document Index:</b> Enabled</i>\n"
        d_e = "✅"
        dcb_data = f"toggle({chat_id}|document|False)"

    else:
        text+="\n<i><b>Document Index:</b> Disabled</i>\n"
        d_e="❎"
        dcb_data = f"toggle({chat_id}|document|True)"

    if aud:
        text+="\n<i><b>Audio Index:</b> Enabled</i>\n"
        a_e = "✅"
        acb_data = f"toggle({chat_id}|audio|False)"

    else:
        text+="\n<i><b>Audio Index:</b> Disabled</i>\n"
        a_e="❎"
        acb_data = f"toggle({chat_id}|audio|True)"

    
    text+="\n<i>Below Buttons Will Toggle Respective Media Types As Enabled Or Disabled....\n</i>"
    text+="<i>This Will Take Into Action As Soon As You Change Them....</i>"
    
    buttons.append([InlineKeyboardButton(f"Video Index: {v_e}", callback_data=vcb_data)])
    buttons.append([InlineKeyboardButton(f"Audio Index: {a_e}", callback_data=acb_data)])
    buttons.append([InlineKeyboardButton(f"Document Index: {d_e}", callback_data=dcb_data)])
    
    buttons.append(
        [
            InlineKeyboardButton
                (
                    "🔙 Back", callback_data=f"settings"
                )
        ]
    )
    
    reply_markup = InlineKeyboardMarkup(buttons)
    
    await update.message.edit_text(
        text,
        reply_markup=reply_markup, 
        parse_mode="html"
    )



@Client.on_callback_query(filters.regex(r"toggle\((.+)\)"), group=2)
async def cb_toggle(bot, update: CallbackQuery):
    """
    A Callback Funtion Support handler For types()
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

    chat_id, types, val = re.findall(r"toggle\((.+)\)", query_data)[0].split("|", 2)
    
    _types = await db.find_chat(int(chat_id))
    
    _types = _types["types"]
    vid = _types["video"]
    doc = _types["document"]
    aud = _types["audio"]
    
    if types == "video":
        vid = True if val=="True" else False
    elif types == "audio":
        aud = True if val=="True" else False
    elif types == "document":
        doc = True if val=="True" else False
    
        
    settings = {
        "video": vid,
        "audio": aud,
        "document": doc
    }

    process = await db.update_settings(chat_id, settings)
    
    if process:
        await update.answer(text="Filter Types Updated Sucessfully", show_alert=True)
    
    else:
        text="Something Wrong Please Check Bot Log For More Information...."
        await update.answer(text, show_alert=True)
        return
    
    _types = await db.find_chat(int(chat_id))
    
    text =f"<i>Filter Types Enabled In <code>{update.message.chat.title}</code></i>\n"
    
    _types = _types["types"]
    vid = _types["video"]
    doc = _types["document"]
    aud = _types["audio"]
    
    buttons = []
    
    if vid:
        text+="\n<i><b>Video Index:</b> Enabled</i>\n"
        v_e = "✅"
        vcb_data = f"toggle({chat_id}|video|False)"
    
    else:
        text+="\n<i><b>Video Index:</b> Disabled</i>\n"
        v_e="❎"
        vcb_data = f"toggle({chat_id}|video|True)"

    if doc:
        text+="\n<i><b>Document Index:</b> Enabled</i>\n"
        d_e = "✅"
        dcb_data = f"toggle({chat_id}|document|False)"

    else:
        text+="\n<i><b>Document Index:</b> Disabled</i>\n"
        d_e="❎"
        dcb_data = f"toggle({chat_id}|document|True)"

    if aud:
        text+="\n<i><b>Audio Index:</b> Enabled</i>\n"
        a_e = "✅"
        acb_data = f"toggle({chat_id}|audio|False)"

    else:
        text+="\n<i><b>Audio Index:</b> Disabled</i>\n"
        a_e="❎"
        acb_data = f"toggle({chat_id}|audio|True)"

    
    text+="\n<i>Below Buttons Will Toggle Respective Media Types As Enabled Or Disabled....\n</i>"
    text+="<i>This Will Take Into Action As Soon As You Change Them....</i>"
    
    buttons.append([InlineKeyboardButton(f"Video Index : {v_e}", callback_data=vcb_data)])
    buttons.append([InlineKeyboardButton(f"Audio Index : {a_e}", callback_data=acb_data)])
    buttons.append([InlineKeyboardButton(f"Document Index : {d_e}", callback_data=dcb_data)])
    
    buttons.append(
        [
            InlineKeyboardButton
                (
                    "🔙 Back", callback_data=f"settings"
                )
        ]
    )
    
    reply_markup = InlineKeyboardMarkup(buttons)
    
    await update.message.edit_text(
        text,
        reply_markup=reply_markup, 
        parse_mode="html"
    )

