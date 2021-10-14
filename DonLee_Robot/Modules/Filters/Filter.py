# (C) AlbertEinstein_TG
# (C) @Nacbots
# (E) @Muhammed_RK, @Mo_Tech_YT , @Mo_Tech_Group, @MT_Botz
# (M) @Jackbro007
# Copyright permission under MIT License
# All rights reserved by PR0FESS0R-99
# License -> https://github.com/PR0FESS0R-99/DonLee_Robot/blob/main/LICENSE

import re
import logging
import asyncio
from time import time
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.errors import ButtonDataInvalid, FloodWait
from DonLee_Robot.Modules.Filters.Main import Database 
from DonLee_Robot.donlee_robot import DonLee_Robot
from DonLee_Robot import Translation, Mo_Tech_YT
import imdb

FIND = {}
INVITE_LINK = {}
ACTIVE_CHATS = {}
db = Database()

@DonLee_Robot.on_message(filters.text & filters.group & ~filters.bot, group=0)
async def auto_filter(bot, update):
    """
    A Funtion To Handle Incoming Text And Reply With Appropriate Results
    """
    group_id = update.chat.id
    the_query = update.text
    query = re.sub(r"[1-2]\d{3}", "", update.text) # Targetting Only 1000 - 2999 😁
    tester = 2
    
    for i in Mo_Tech_YT.MO_TECH_YT_05 :
       if i in the_query.split() :
          for a in Mo_Tech_YT.MO_TECH_YT_08 :
             if a in the_query.split() :
                tester = 0
                break
             else :
                tester = 1
       if tester==0 :
          break
                
    if tester==1 :
        buttons = [[
                  InlineKeyboardButton("Help🥴",callback_data="help_me")
                  ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await bot.send_message(
        chat_id=update.chat.id,
        text="<b>Please dont send the word <code>Movie</code> with your Movie name 😪\nTry Reading the help box below</b> 👇🏽",
        reply_markup=reply_markup,
        parse_mode="html",
        reply_to_message_id=update.message_id)
        return
        
    for i in Mo_Tech_YT.MO_TECH_YT_06.split() :
       if i in the_query.lower() :
          buttons = [[
                  InlineKeyboardButton("Help🥴",callback_data="help_me")
                  ]]
          reply_markup = InlineKeyboardMarkup(buttons)
          await bot.send_message(
          text="<b> കിട്ടോ, അയക്കോ, ഉണ്ടോ, തരുമോ എന്ന് ഒന്നും ചോദിക്കേണ്ട സിനിമയുടെ പേര് മാത്രം കൃത്യമായി അയക്കുക</b> 😪",
          chat_id=update.chat.id,
          reply_to_message_id=update.message_id,
          parse_mode="html",
          reply_markup=reply_markup)
          return
        
    for i in "#admins #admin #complaint #report @admin @admins".split():
      if i in the_query.lower() :
         await update.forward(chat_id=Mo_Tech_YT.MO_TECH_YT_09)
         await bot.send_message(
             chat_id=update.chat.id,
             text="<b>Your report was successfully sent to admins please wait for a reply 😉</b>",
             reply_to_message_id=update.message_id,
             parse_mode="html")
         return

    if re.findall(r"((^\/|^,|^\.|^[\U0001F600-\U000E007F]).*)", update.text):
        return

    for a in "https:// http:// thanks thank tnx tnq tq tqsm #".split():
      if a in update.text.lower():
          return
    
    if len(query) < 2:
        return
                  
    results = []
    
    global ACTIVE_CHATS
    global FIND
    
    configs = await db.find_chat(group_id)
    achats = ACTIVE_CHATS[str(group_id)] if ACTIVE_CHATS.get(str(group_id)) else await db.find_active(group_id)
    ACTIVE_CHATS[str(group_id)] = achats
    
    if not configs:
        return
    
    allow_video = configs["types"]["video"]
    allow_audio = configs["types"]["audio"] 
    allow_document = configs["types"]["document"]
    
    max_pages = configs["configs"]["max_pages"] # maximum page result of a query
    pm_file_chat = configs["configs"]["pm_fchat"] # should file to be send from bot pm to user
    max_results = configs["configs"]["max_results"] # maximum total result of a query
    max_per_page = configs["configs"]["max_per_page"] # maximum buttom per page 
    show_invite = configs["configs"]["show_invite_link"] # should or not show active chat invite link
    
    show_invite = (False if pm_file_chat == True else show_invite) # turn show_invite to False if pm_file_chat is True
    
    filters = await db.get_filters(group_id, query)
    
    if filters:
        for filter in filters: # iterating through each files
            file_name = filter.get("file_name")
            file_type = filter.get("file_type")
            file_link = filter.get("file_link")
            file_size = int(filter.get("file_size", "0"))
            
            # from B to MiB
            
            if file_size < 1024:
                file_size = f"[{file_size} B]"
            elif file_size < (1024**2):
                file_size = f" {str(round(file_size/1024, 2))} KB "
            elif file_size < (1024**3):
                file_size = f" {str(round(file_size/(1024**2), 2))} MB "
            elif file_size < (1024**4):
                file_size = f"{str(round(file_size/(1024**3), 2))} GB "
            
            
            file_size = "" if file_size == ("[0 B]") else file_size
            
            # add emoji down below inside " " if you want..
   
            

            if file_type == "video":
                if allow_video: 
                    pass
                else:
                    continue
                
            elif file_type == "audio":
                if allow_audio:
                    pass
                else:
                    continue
                
            elif file_type == "document":
                if allow_document:
                    pass
                else:
                    continue
            
            if len(results) >= max_results:
                break
            
            if pm_file_chat: 
                unique_id = filter.get("unique_id")
                if not FIND.get("bot_details"):
                    try:
                        bot_= await bot.get_me()
                        FIND["bot_details"] = bot_
                    except FloodWait as e:
                        asyncio.sleep(e.x)
                        bot_= await bot.get_me()
                        FIND["bot_details"] = bot_
                
                bot_ = FIND.get("bot_details")
                file_link = f"https://t.me/{bot_.username}?start={unique_id}"
            if not Mo_Tech_YT.MO_TECH_YT_07:
               button_text = f"[{file_size}]📽️ {file_name}"
               results.append(

                [

                    InlineKeyboardButton(button_text, url=file_link)

                ]

            )
            else:
               results.append(
                [
                    InlineKeyboardButton(f"{file_name}", url=file_link),
                    InlineKeyboardButton(f"{file_size}", url=file_link)
                ]
            )
           
        
    else:
        pass # return if no files found for that query
    

    if len(results) == 0 : # double check
        buttons = [[
                 InlineKeyboardButton("Instructions 📑",callback_data="instructions")
                 ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await bot.send_message(
        chat_id=update.chat.id,
        text=f"<b>Sorry I couldn't find anything for <code>{the_query}</code> 🤧\nTry Reading the instructions below</b> 👇🏽",
        reply_markup=reply_markup,
        parse_mode="html",
        reply_to_message_id=update.message_id)
        return
    
    else:
    
        result = []
        # seperating total files into chunks to make as seperate pages
        result += [results[i * max_per_page :(i + 1) * max_per_page ] for i in range((len(results) + max_per_page - 1) // max_per_page )]
        len_result = len(result)
        len_results = len(results)
        results = None # Free Up Memory
        
        FIND[query] = {"results": result, "total_len": len_results, "max_pages": max_pages} # TrojanzHex's Idea Of Dicts😅

        # Add next buttin if page count is not equal to 1
        page_btn = "⓵ ❷ ❸ ❹ ❺ "
        cutter = len_result if len_result < max_pages else max_pages
        page_btn = page_btn[:cutter*2]
        
        if len_result != 1:           
            result[0].append(
                [
                    InlineKeyboardButton("⪼⪼", callback_data=f"navigate(0|next|{query})")
                ]
            )
        
        # Just A Decaration
        result[0].append([
            InlineKeyboardButton(f"📑 {page_btn} 📑", callback_data="ignore")
        ])
        
        
        # if show_invite is True Append invite link buttons
        if show_invite:
            
            ibuttons = []
            achatId = []
            await gen_invite_links(configs, group_id, bot, update)
            
            for x in achats["chats"] if isinstance(achats, dict) else achats:
                achatId.append(int(x["chat_id"])) if isinstance(x, dict) else achatId.append(x)

            ACTIVE_CHATS[str(group_id)] = achatId
            
            for y in INVITE_LINK.get(str(group_id)):
                
                chat_id = int(y["chat_id"])
                
                if chat_id not in achatId:
                    continue
                
                chat_name = y["chat_name"]
                invite_link = y["invite_link"]
                
                if ((len(ibuttons)%2) == 0):
                    ibuttons.append(
                        [
                            InlineKeyboardButton(f"⚜ {chat_name} ⚜", url=invite_link)
                        ]
                    )

                else:
                    ibuttons[-1].append(
                        InlineKeyboardButton(f"⚜ {chat_name} ⚜", url=invite_link)
                    )
                
            for x in ibuttons:
                result[0].insert(0, x) #Insert invite link buttons at first of page
                
            ibuttons = None # Free Up Memory...
            achatId = None
            
            
        reply_markup = InlineKeyboardMarkup(result[0])

        #To find any number in the query and remove it.
        year = 2021
        for i in the_query.split():
            try :
                year = int(i)
                the_query = the_query.replace(i,"")
            except :
                pass
        for i in "movie malayalam english tamil kannada telugu subtitles esub esubs".split():
            if i in the_query.lower().split():
                the_query = the_query.replace(i,"")

        try:
            ia = imdb.IMDb()
            my_movie=the_query
            movies = ia.search_movie(my_movie)
            #print(f"{movies[0].movieID} {movies[0]['title']}")
            movie_url = movies[0].get_fullsizeURL()

            await bot.send_photo(
                photo=movie_url,
                caption=f"""🎬 Title : {query}\n🗃️ Total Files : {len_results if len_results <= max_pages*8 else max_pages*8}""",
                reply_markup=reply_markup,
                chat_id=update.chat.id,
                reply_to_message_id=update.message_id,
                parse_mode="html"
            )

        except Exception as e:
          print(e)

          try:
              await bot.send_message(
                chat_id = update.chat.id,
                text=f"📀 Title : <code>{query}</code> \n🗃️ Total Files : <code>{len_results if len_results <= max_pages*8 else max_pages*8}</code>",
                reply_markup=reply_markup,
                parse_mode="html",
                reply_to_message_id=update.message_id
            )

          except ButtonDataInvalid:
              print(result[0])
        
async def gen_invite_links(db, group_id, bot, update):
    """
    A Funtion To Generate Invite Links For All Active 
    Connected Chats In A Group
    """
    chats = db.get("chat_ids")
    global INVITE_LINK
    
    if INVITE_LINK.get(str(group_id)):
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

        INVITE_LINK[str(group_id)] = Links
    return 


async def recacher(group_id, ReCacheInvite=True, ReCacheActive=False, bot=DonLee_Robot, update=Message):
    """
    A Funtion To rechase invite links and active chats of a specific chat
    """
    global INVITE_LINK, ACTIVE_CHATS

    if ReCacheInvite:
        if INVITE_LINK.get(str(group_id)):
            INVITE_LINK.pop(str(group_id))
        
        Links = []
        chats = await db.find_chat(group_id)
        chats = chats["chat_ids"]
        
        if chats:
            for x in chats:
                Name = x["chat_name"]
                chat_id = x["chat_id"]
                if (Name == None or chat_id == None):
                    continue
                
                chat_id = int(chat_id)
                
                Link = await bot.export_chat_invite_link(chat_id)
                Links.append({"chat_id": chat_id, "chat_name": Name, "invite_link": Link})

            INVITE_LINK[str(group_id)] = Links
    
    if ReCacheActive:
        
        if ACTIVE_CHATS.get(str(group_id)):
            ACTIVE_CHATS.pop(str(group_id))
        
        achats = await db.find_active(group_id)
        achatId = []
        if achats:
            for x in achats["chats"]:
                achatId.append(int(x["chat_id"]))
            
            ACTIVE_CHATS[str(group_id)] = achatId
    return
