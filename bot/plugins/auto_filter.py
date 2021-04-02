import re
import logging
import asyncio

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.errors import ButtonDataInvalid

from bot.database import Database # pylint: disable=import-error
from bot.bot import Bot # pylint: disable=import-error


Find = {}
InviteLink = {}
ActiveChats = {}
db = Database()

@Bot.on_message(filters.text & filters.group, group=0)
async def auto_filter (bot, update):
    """
    A Funtion To Handle Incoming Text And Reply With Appropriate Results
    """
    group_id = update.chat.id

    if re.findall(r"((^\/|^,|^\.|^[\U0001F600-\U000E007F]).*)", update.text):
        return
    
    query = update.text
    if len(query) < 2:
        return
    
    results = []
    
    global ActiveChats
    
    configs = await db.find_chat(group_id)
    achats = ActiveChats[str(group_id)] if ActiveChats.get(str(group_id)) else await db.find_active(group_id)
    
    if not configs:
        return
    
    allow_v = configs["types"]["video"]
    allow_a = configs["types"]["audio"]
    allow_d = configs["types"]["document"]
    
    maxp = configs["configs"]["max_pages"]
    maxr = configs["configs"]["max_results"]
    maxb = configs["configs"]["max_per_page"]
    showInvite = configs["configs"]["show_invite_link"]
    
    filters = await db.get_filters(group_id, query)
    
    if filters:
        for filter in filters:
            file_name = filter.get("file_name")
            file_type = filter.get("file_type")
            file_link = filter.get("file_link")
            
            if file_type == "video":
                if allow_v:
                    pass
                else:
                    continue
                
            elif file_type == "audio":
                if allow_a:
                    pass
                else:
                    continue
                
            elif file_type == "document":
                if allow_d:
                    pass
                else:
                    continue
            
            if len(results) >= maxr:
                break
            
            results.append(
                [
                    InlineKeyboardButton
                        (
                            file_name, url=file_link
                        )
                ]
            )
        
    else:
        return
    

    if len(results) == 0:
        return
    
    else:
        global Find
    
        result = []
        result += [results[i * maxb :(i + 1) * maxb ] for i in range((len(results) + maxb - 1) // maxb )]
        len_results = len(results)
        results = None # Free Up Memory
        
        Find[query] = {"results": result, "total_len": len_results, "max_pages": maxp} # TrojanzHex's Idea Of Dicts😅

        if len_results >maxb:
            result[0].append([InlineKeyboardButton("Next ⏩", callback_data=f"navigate(0|next|{query})")])
        
        # Just A Decarator
        result[0].append([
            InlineKeyboardButton(f"🔰 Page 1/{len_results if len_results < maxp else maxp} 🔰", callback_data="ignore")
        ])
        
        if showInvite:
            
            ibuttons = []
            achatId = []
            await GenInviteLinks(configs, group_id, bot, update)
            
            for x in achats["chats"] if isinstance(achats, dict) else achats:
                achatId.append(int(x["chat_id"])) if isinstance(x, dict) else achatId.append(x)
            
            ActiveChats[str(group_id)] = achatId
            
            for y in InviteLink.get(str(group_id)):
                
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
                result[0].insert(0, x)
            ibuttons = None
            achatId = None
            
            
        reply_markup = InlineKeyboardMarkup(result[0])

        try:
            await bot.send_message(
                chat_id = update.chat.id,
                text=f"Found {(len_results)} Results For Your Query: <code>{query}</code>",
                reply_markup=reply_markup,
                parse_mode="html",
                reply_to_message_id=update.message_id
            )

        except ButtonDataInvalid:
            print(result[0])
        
        except Exception as e:
            print(e)


async def GenInviteLinks(db, g_id, bot, update):

    chats = db.get("chat_ids")
    global InviteLink
    
    if InviteLink.get(str(g_id)):
        return
    
    Links = []
    if chats:
        for x in chats:
            Name = x["chat_name"]
            
            if Name == None:
                continue
            
            chatId=int(x["chat_id"])
            
            Link = await bot.export_chat_invite_link(chatId)
            Links.append({"chat_id": chatId, "chat_name": Name, "invite_link": Link})

        InviteLink[str(g_id)] = Links
    return 


async def ReCacher(g_id, ReCacheInvite=True, ReCacheActive=False, bot=Bot, update=Message):

    global InviteLink, ActiveChats

    if ReCacheInvite:
        if InviteLink.get(str(g_id)):
            InviteLink.pop(str(g_id))
        
        Links = []
        chats = await db.find_chat(g_id)
        chats = chats["chat_ids"]
        
        if chats:
            for x in chats:
                Name = x["chat_name"]
                chat_id = int(x["chat_id"])
                if (Name == None or chat_id == None):
                    continue
                
                Link = await bot.export_chat_invite_link(chat_id)
                Links.append({"chat_id": chat_id, "chat_name": Name, "invite_link": Link})

            InviteLink[str(g_id)] = Links
    
    if ReCacheActive:
        
        if ActiveChats.get(str(g_id)):
            ActiveChats.pop(str(g_id))
        
        achats = await db.find_active(g_id)
        achatId = []
        if achats:
            for x in achats["chats"]:
                achatId.append(int(x["chat_id"]))
            
            ActiveChats[str(g_id)] = achatId
    return 
