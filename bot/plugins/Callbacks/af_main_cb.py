import re
import time
import asyncio

from pyrogram import Client, filters
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
 
from . import (
    FIND,
    Database,
    admin_list,
    ACTIVE_CHATS,
    CHAT_DETAILS,
    INVITE_LINK, 
    remove_emoji,
    gen_invite_links,
)
from bot import Translation

db = Database()



@Client.on_callback_query(filters.regex(r"navigate\((.+)\)"), group=2)
async def cb_navg(bot, update: CallbackQuery):
    """
    A Callback Funtion For The Next Button Appearing In Results
    """
    global CHAT_DETAILS
    query_data = update.data
    chat_id = update.message.chat.id
    user_id = update.from_user.id
    
    index_val, btn, query = re.findall(r"navigate\((.+)\)", query_data)[0].split("|", 2)
    try:
        ruser_id = update.message.reply_to_message.from_user.id
    except Exception as e:
        print(e)
        ruser_id = None
    
    chat_dict = CHAT_DETAILS.get(str(chat_id))
    chat_admins = chat_dict.get("admins") if chat_dict != None else None

    # Make Admin's ID List
    if ( chat_dict or chat_admins ) == None: 
        chat_admins = await admin_list(chat_id, bot, update)
    
    # Checks if user is same as requested user or is admin
    if not ((user_id == ruser_id) or (user_id in chat_admins)):
        await update.answer("Nice Try ;)",show_alert=True)
        return


    if btn == "next":
        index_val = int(index_val) + 1
    elif btn == "back":
        index_val = int(index_val) - 1
    
    achats = ACTIVE_CHATS[str(chat_id)]
    configs = await db.find_chat(chat_id)
    pm_file_chat = configs["configs"]["pm_fchat"]
    show_invite = configs["configs"]["show_invite_link"]
    
    # show_invite = (False if pm_file_chat == True else show_invite) # turn show_invite to False if pm_file_chat is True

    results = FIND.get(query).get("results")
    leng = FIND.get(query).get("total_len")
    max_pages = FIND.get(query).get("max_pages")
    
    try:
        temp_results = results[index_val].copy()
    except IndexError:
        return # Quick Fix🏃🏃
    except Exception as e:
        print(e)
        return

    if ((index_val + 1 )== max_pages) or ((index_val + 1) == len(results)): # Max Pages
        temp_results.append([
            InlineKeyboardButton("⏪ Back", callback_data=f"navigate({index_val}|back|{query})")
        ])

    elif int(index_val) == 0:
        pass

    else:
        temp_results.append([
            InlineKeyboardButton("⏪ Back", callback_data=f"navigate({index_val}|back|{query})"),
            InlineKeyboardButton("Next ⏩", callback_data=f"navigate({index_val}|next|{query})")
        ])

    if not int(index_val) == 0:    
        temp_results.append([
            InlineKeyboardButton(f"🔰 Page {index_val + 1}/{len(results) if len(results) < max_pages else max_pages} 🔰", callback_data="ignore")
        ])
    
    if show_invite and int(index_val) !=0 :
        
        ibuttons = []
        achatId = []
        await gen_invite_links(configs, chat_id, bot, update)
        
        for x in achats["chats"] if isinstance(achats, dict) else achats:
            achatId.append(int(x["chat_id"])) if isinstance(x, dict) else achatId.append(x)
        
        for y in INVITE_LINK.get(str(chat_id)):
            
            chat_id = int(y["chat_id"])
            
            if chat_id not in achatId:
                continue
            
            chat_name = y["chat_name"]
            invite_link = y["invite_link"]
            
            if ((len(ibuttons)%2) == 0):
                ibuttons.append(
                    [
                        InlineKeyboardButton
                            (
                                f"⚜ {chat_name} ⚜", url=invite_link
                            )
                    ]
                )

            else:
                ibuttons[-1].append(
                    InlineKeyboardButton
                        (
                            f"⚜ {chat_name} ⚜", url=invite_link
                        )
                )
            
        for x in ibuttons:
            temp_results.insert(0, x)
        ibuttons = None
        achatId = None
    
    reply_markup = InlineKeyboardMarkup(temp_results)
    
    text=f"<i>Found</i> <code>{leng}</code> <i>Results For Your Query:</i> <code>{query}</code>"
        
    try:
        await update.message.edit(
                text,
                reply_markup=reply_markup,
                parse_mode="html"
        )
        
    except FloodWait as f: # Flood Wait Caused By Spamming Next/Back Buttons
        await asyncio.sleep(f.x)
        await update.message.edit(
                text,
                reply_markup=reply_markup,
                parse_mode="html"
        )



@Client.on_callback_query(filters.regex(r"settings"), group=2)
async def cb_settings(bot, update: CallbackQuery):
    """
    A Callback Funtion For Back Button in /settings Command
    """
    global CHAT_DETAILS
    chat_id = update.message.chat.id
    user_id = update.from_user.id

    chat_dict = CHAT_DETAILS.get(str(chat_id))
    chat_admins = chat_dict.get("admins") if chat_dict != None else None

    if ( chat_dict or chat_admins ) == None: # Make Admin's ID List
        chat_admins = await admin_list(chat_id, bot, update)

    if user_id not in chat_admins: # Check If User Is Admin
        return

    bot_status = await bot.get_me()
    bot_fname= bot_status.first_name
    
    text =f"<i>{bot_fname}'s</i> Auto Filter Settings Pannel.....\n"
    text+=f"\n<i>You Can Use This Menu To Change Connectivity And Know Status Of Your Every Connected Channel, Change Filter Types, Configure Filter Results And To Know Status Of Your Group...</i>"
    
    buttons = [
        [
            InlineKeyboardButton
                (
                    "Channels", callback_data=f"channel_list({chat_id})"
                ), 
            
            InlineKeyboardButton
                (
                    "Filter Types", callback_data=f"types({chat_id})"
                )
        ],
        [
            InlineKeyboardButton
                (
                    "Configure 🛠", callback_data=f"config({chat_id})"
                )
        ], 
        [
            InlineKeyboardButton
                (
                    "Status", callback_data=f"status({chat_id})"
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

    await update.message.edit_text(
        text, 
        reply_markup=reply_markup, 
        parse_mode="html"
        )



@Client.on_callback_query(filters.regex(r"warn\((.+)\)"), group=2)
async def cb_warn(bot, update: CallbackQuery):
    """
    A Callback Funtion For Acknowledging User's About What Are They Upto
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
    
    channel_id, channel_name, action = re.findall(r"warn\((.+)\)", query_data)[0].split("|", 2)
    
    if action == "connect":
        text=f"<i>Are You Sure You Want To Enable Connection With</i> <code>{channel_name}</code><i>..???</i>\n"
        text+=f"\n<i>This Will Show File Links From</i> <code>{channel_name}</code> <i>While Showing Results</i>..."


    elif action == "disconnect":
        text=f"<i>Are You Sure You Want To Disable</i> <code>{channel_name}</code> <i>Connection With The Group???....</i>\n"
        text+=f"\n<i>The DB Files Will Still Be There And You Can Connect Back To This Channel Anytime From Settings Menu Without Adding Files To DB Again...</i>\n"
        text+=f"\n<i>This Disabling Just Hide Results From The Filter Results...</i>"


    elif action == "c_delete":
        text=f"<i>Are You Sure You Want To Disconnect</i> <code>{channel_name}</code> <i>From This Group??</i>\n"
        text+=f"\n<i><b>This Will Delete Channel And All Its Files From DB Too....!!</b></i>\n"
        text+=f"\nYou Need To Add Channel Again If You Need To Shows It Result..."
        text+=f"\n<s>ProTip: Make Use Of Disconnect Button To Disable <code>{channel_name}</code> Results Temporarily....</s>"


    elif action=="f_delete":
        text=f"<i>Are You Sure That You Want To Clear All Filter From This Chat</i> <code>{channel_name}</code><i>???</i>\n"
        text+=f"\n<i>This Will Erase All Files From DB..</i>"


    elif action == "gcmds" and channel_name == "conn":
        text=f"<i>Are You Sure You Want To Enable All Connection Of</i> <code>{chat_name}</code><i>..???</i>\n"
        text+=f"\n<i>This Will Show File In The Results From All Chat Connections Of</i> <code>{chat_name}</code>..."


    elif action == "gcmds" and channel_name == "disconn":
        text=f"<i>Are You Sure You Want To Disable All Connection Of</i> <code>{chat_name}</code><i>....???</i>\n"
        text+=f"\n<i>The DB Files Will Still Be There And You Can Connect Back To All Channel Anytime From Settings Menu Without Adding Files To DB Again...</i>\n"
        text+=f"\n<i>This Disabling Will No Longer Show Results To Any Query Unless You Enable Back Them...</i>"
    
    
    elif action == "gcmds" and channel_name == "c_delete":
        text=f"<i>Are You Sure You Want To Disconnect ALl COnnected Chats Of </i> <code>{chat_name}</code> <i>....???</i>\n"
        text+=f"\n<i><b>This Will Delete All Connected Channel And All Its Files From DB Too....!!</b></i>\n"
        text+=f"\nYou Need To Add Channel Again If You Need To Shows It's Results Again.....\n"
        text+=f"\n<s>ProTip: Make Use Of Disconnect Button To Disable All Chat Results Temporarily....</s>"


    elif action == "gcmds" and channel_name == "f_delete":
        text=f"<i>Are You Sure That You Want To Clear All Filters Of</i> <code>{chat_name}</code><i>....???</i>\n"
        text+=f"\n<i>This Will Erase All Files Of <code>{chat_name}</code> From DB..</i>"
    
    
    buttons = [
        [
            InlineKeyboardButton
                (
                    "Yes", callback_data=f"{action}({channel_id}|{channel_name})"
                ), 
            
            InlineKeyboardButton
                (
                    "No", callback_data="close"
                )
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(buttons)
    
    await update.message.edit_text(
        text,
        reply_markup=reply_markup,
        parse_mode="html"
    )



@Client.on_callback_query(filters.regex(r"set\((.+)\)"), group=2)
async def cb_set(bot, update: CallbackQuery):
    """
    A Callback Funtion Support For config()
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


    action, val, chat_id, curr_val = re.findall(r"set\((.+)\)", query_data)[0].split("|", 3)

    try:
        val, chat_id, curr_val = float(val), int(chat_id), float(curr_val)
    except:
        chat_id = int(chat_id)
    
    if val == curr_val:
        await update.answer("New Value Cannot Be Old Value...Please Choose Different Value...!!!", show_alert=True)
        return
    
    prev = await db.find_chat(chat_id)

    accuracy = float(prev["configs"].get("accuracy", 0.80))
    max_pages = int(prev["configs"].get("max_pages"))
    max_results = int(prev["configs"].get("max_results"))
    max_per_page = int(prev["configs"].get("max_per_page"))
    pm_file_chat = True if prev["configs"].get("pm_fchat") == (True or "True") else False
    show_invite_link = True if prev["configs"].get("show_invite_link") == (True or "True") else False
    
    if action == "accuracy": # Scophisticated way 😂🤣
        accuracy = val
    
    elif action == "pages":
        max_pages = int(val)
        
    elif action == "results":
        max_results = int(val)
        
    elif action == "per_page":
        max_per_page = int(val)

    elif action =="showInv":
        show_invite_link = True if val=="True" else False

    elif action == "inPM":
        pm_file_chat = True if val=="True" else False
        

    new = dict(
        accuracy=accuracy,
        max_pages=max_pages,
        max_results=max_results,
        max_per_page=max_per_page,
        pm_fchat=pm_file_chat,
        show_invite_link=show_invite_link
    )
    
    append_db = await db.update_configs(chat_id, new)
    
    if not append_db:
        text="Something Wrong Please Check Bot Log For More Information...."
        await update.answer(text=text, show_alert=True)
        return
    
    text=f"Your Request Was Updated Sucessfully....\nNow All Upcoming Results Will Show According To This Settings..."
        
    buttons = [
        [
            InlineKeyboardButton
                (
                    "Back 🔙", callback_data=f"config({chat_id})"
                ),
            
            InlineKeyboardButton
                (
                    "Close 🔐", callback_data="close"
                )
        ]
    ]
    
    reply_markup=InlineKeyboardMarkup(buttons)
    
    await update.message.edit_text(
        text, reply_markup=reply_markup, parse_mode="html"
    )



@Client.on_callback_query(filters.regex(r"^(start|help|about|close)$"), group=2)
async def callback_data(bot, update: CallbackQuery):

    query_data = update.data

    if query_data == "start":
        buttons = [[
            InlineKeyboardButton('My Dev 👨‍🔬', url='https://t.me/CrazyBotsz'),
            InlineKeyboardButton('Source Code 🧾', url ='https://github.com/CrazyBotsz/Adv-Auto-Filter-Bot-V2')
        ],[
            InlineKeyboardButton('Support 🛠', url='https://t.me/CrazyBotszGrp')
        ],[
            InlineKeyboardButton('Help ⚙', callback_data="help")
        ]]
    
        reply_markup = InlineKeyboardMarkup(buttons)
        
        await update.message.edit_text(
            Translation.START_TEXT.format(update.from_user.mention),
            reply_markup=reply_markup,
            parse_mode="html",
            disable_web_page_preview=True
        )


    elif query_data == "help":
        buttons = [[
            InlineKeyboardButton('Home ⚡', callback_data='start'),
            InlineKeyboardButton('About 🚩', callback_data='about')
        ],[
            InlineKeyboardButton('Close 🔐', callback_data='close')
        ]]
    
        reply_markup = InlineKeyboardMarkup(buttons)
        
        await update.message.edit_text(
            Translation.HELP_TEXT,
            reply_markup=reply_markup,
            parse_mode="html",
            disable_web_page_preview=True
        )


    elif query_data == "about": 
        buttons = [[
            InlineKeyboardButton('Home ⚡', callback_data='start'),
            InlineKeyboardButton('Close 🔐', callback_data='close')
        ]]
        
        reply_markup = InlineKeyboardMarkup(buttons)
        
        await update.message.edit_text(
            Translation.ABOUT_TEXT,
            reply_markup=reply_markup,
            parse_mode="html"
        )


    elif query_data == "close":
        await update.message.delete()
        
