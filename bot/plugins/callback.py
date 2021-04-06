import re
import time
import asyncio

from pyrogram import Client, filters
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from bot import start_uptime, Translation # pylint: disable=import-error
from bot.plugins.auto_filter import ( # pylint: disable=import-error
    Find, 
    InviteLink, 
    ActiveChats,
    ReCacher,
    GenInviteLinks
    )
from bot.plugins.settings import( # pylint: disable=import-error
    verify,
    remove_emoji
)
from bot.database import Database # pylint: disable=import-error

db = Database()

@Client.on_callback_query()
async def callback_data(bot, update: CallbackQuery):

    query_data = update.data
    chat_id = update.message.chat.id
    chat_name = remove_emoji(update.message.chat.title).encode('ascii', 'ignore').decode('ascii')[:38]

    if re.fullmatch(r"navigate\((.+)\)", query_data):
        """
        A Callback Funtion For The Next Button Appearing In Results
        """
        index_val, btn, query = re.findall(r"navigate\((.+)\)", query_data)[0].split("|", 2)
        

        if update.message.reply_to_message.sender_chat == None: # Anonymous Admin Bypass
            ruser_id = update.message.reply_to_message.from_user.id or None
            auser_id = update.from_user.id
            try:
                user = await bot.get_chat_member(update.message.chat.id, auser_id)
            
            except UserNotParticipant:
                await update.answer("Nice Try ;)",show_alert=True)
                return
            
            except Exception as e:
                print(e)
                return
            
            if (auser_id != ruser_id) or (user.status == "member"):
                
                await update.answer("Nice Try ;)",show_alert=True)
                return


        if btn == "next":
            index_val = int(index_val) + 1
        elif btn == "back":
            index_val = int(index_val) - 1
        
        achats = ActiveChats[str(chat_id)]
        configs = await db.find_chat(chat_id)
        showInvite = configs["configs"]["show_invite_link"]
        
        results = Find.get(query).get("results")
        leng = Find.get(query).get("total_len")
        maxp = Find.get(query).get("max_pages")
        
        try:
            temp_results = results[index_val].copy()
        except IndexError:
            return # Quick Fix🏃🏃
        except Exception as e:
            print(e)
            return

        if ((index_val + 1 )== maxp) or ((index_val + 1) == len(results)): # Max Pages
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
                InlineKeyboardButton(f"🔰 Page {index_val + 1}/{len(results) if len(results) < maxp else maxp} 🔰", callback_data="ignore")
            ])
        
        if showInvite and int(index_val) !=0 :
            
            ibuttons = []
            achatId = []
            await GenInviteLinks(configs, chat_id, bot, update)
            
            for x in achats["chats"] if isinstance(achats, dict) else achats:
                achatId.append(int(x["chat_id"])) if isinstance(x, dict) else achatId.append(x)
            
            for y in InviteLink.get(str(chat_id)):
                
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


    elif re.fullmatch(r"settings", query_data):
        """
        A Callback Funtion For Back Button in /settings Command
        """
        if update.message.reply_to_message.sender_chat == None: # Anonymous Admin Bypass
            if verify.get(str(update.message.reply_to_message.message_id)) != update.from_user.id:
                return

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

        await update.message.edit_text(
            text, 
            reply_markup=reply_markup, 
            parse_mode="html"
            )


    elif re.fullmatch(r"warn\((.+)\)", query_data):
        """
        A Callback Funtion For Acknowledging User's About What Are They Upto
        """
        if update.message.reply_to_message.sender_chat == None:

            if verify.get(str(update.message.reply_to_message.message_id)) != update.from_user.id:
                return
        
        c_id, c_name, action = re.findall(r"warn\((.+)\)", query_data)[0].split("|", 2)
        
        if action == "connect":
            text=f"<i>Are You Sure You Want To Enable Connection With</i> <code>{c_name}</code><i>..???</i>\n"
            text+=f"\n<i>This Will Show File Links From</i> <code>{c_name}</code> <i>While Showing Results</i>..."
        
        elif action == "disconnect":
            text=f"<i>Are You Sure You Want To Disable</i> <code>{c_name}</code> <i>Connection With The Group???....</i>\n"
            text+=f"\n<i>The DB Files Will Still Be There And You Can Connect Back To This Channel Anytime From Settings Menu Without Adding Files To DB Again...</i>\n"
            text+=f"\n<i>This Disabling Just Hide Results From The Filter Results...</i>"
        
        elif action == "c_delete":
            text=f"<i>Are You Sure You Want To Disconnect</i> <code>{c_name}</code> <i>From This Group??</i>\n"
            text+=f"\n<i><b>This Will Delete Channel And All Its Files From DB Too....!!</b></i>\n"
            text+=f"\nYou Need To Add Channel Again If You Need To Shows It Result..."
            
        
        elif action=="f_delete":
            text=f"<i>Are You Sure That You Want To Clear All Filter From This Chat</i> <code>{c_name}</code><i>???</i>\n"
            text+=f"\n<i>This Will Erase All Files From DB..</i>"
            
        buttons = [
            [
                InlineKeyboardButton
                    (
                        "Yes", callback_data=f"{action}({c_id}|{c_name})"
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


    elif re.fullmatch(r"channel_list\((.+)\)", query_data):
        """
        A Callback Funtion For Displaying All Channel List And Providing A Menu To Navigate
        To Every COnnect Chats For Furthur Control
        """
        if update.message.reply_to_message.sender_chat == None: # Just To Make Sure If Its Anonymous Admin Or Not

            if verify.get(str(update.message.reply_to_message.message_id)) != update.from_user.id:
                return

            
        chat_id, chat_name =  re.findall(r"channel_list\((.+)\)", query_data)[0].split("|", 1)
        
        text = "<i>Semms Like You Dont Have Any Channel Connected...</i>\n\n<i>Connect To Any Chat To Continue With This Settings...</i>"
        
        db_list = await db.find_chat(int(chat_id))
        
        cid_list = []
        cname_list = []
        
        if db_list:
            for x in db_list["chat_ids"]:
                cid = x["chat_id"]
                cname = x["chat_name"]
                
                try:
                    if (cid == None or cname == None):
                        continue
                except:
                    break
                
                cname = remove_emoji(cname).encode('ascii', 'ignore').decode('ascii')[:38]
                cid_list.append(cid)
                cname_list.append(cname)
            
        buttons = []

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

        if cname_list:
            
            text=f"<i>List Of Connected Channels With <code>{chat_name}</code> With There Settings..</i>\n"
        
            for x in range(1, (len(cname_list)+1)):
                text+=f"\n<code>{x}. {cname_list[x-1]}</code>\n"
        
            text += "\nChoose Appropriate Buttons To Navigate Through Respective Channels"
        
            
            btn_key = [
                "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟", 
                "1️⃣1️⃣", "1️⃣2️⃣", "1️⃣3️⃣", "1️⃣4️⃣", "1️⃣5️⃣", "1️⃣6️⃣", "1️⃣7️⃣", 
                "1️⃣8️⃣", "1️⃣9️⃣", "2️⃣0️⃣" # Just In Case 😂🤣
            ]
        
            for i in range(1, (len(cname_list) + 1)):
                if i == 1:
                    buttons.insert(0,
                        [
                        InlineKeyboardButton
                            (
                                btn_key[i-1], callback_data=f"info({cid_list[i-1]}|{cname_list[i-1]})"
                            )
                        ]
                    )
            
                else:
                    buttons[0].append(
                        InlineKeyboardButton
                            (
                                btn_key[i-1], callback_data=f"info({cid_list[i-1]}|{cname_list[i-1]})"
                            )
                    )
        
        reply_markup=InlineKeyboardMarkup(buttons)
        
        await update.message.edit_text(
                text = text,
                reply_markup=reply_markup,
                parse_mode="html"
            )


    elif re.fullmatch(r"info\((.+)\)", query_data):
        """
        A Callback Funtion For Displaying Details Of The Connected Chat And Provide
        Ability To Connect / Disconnect / Delete / Delete Filters of That Specific Chat
        """
        if update.message.reply_to_message.sender_chat == None:
            if verify.get(str(update.message.reply_to_message.message_id)) != update.from_user.id:
                return

        c_id, c_name = re.findall(r"info\((.+)\)", query_data)[0].split("|", 1)
        
        f_count = await db.cf_count(chat_id, int(c_id)) 
        active = await db.find_active(chat_id)

        if active:
            dicts = active["chats"]
            db_cids = [ int(x["chat_id"]) for x in dicts ]
            
            if int(c_id) in db_cids:
                active = True
                status = "Connected"
                
            else:
                active = False
                status = "Disconnected"
                
        else:
            active = False
            status = "Disconnected"

        text=f"<i>Info About <b>{c_name}</b></i>\n"
        text+=f"\n<i>Channel Name:</i> <code>{c_name}</code>\n"
        text+=f"\n<i>Channel ID:</i> <code>{c_id}</code>\n"
        text+=f"\n<i>Channel Files:</i> <code>{f_count}</code>\n"
        text+=f"\n<i>Current Status:</i> <code>{status}</code>\n"


        if active:
            buttons = [
                        [
                            InlineKeyboardButton
                                (
                                    "🚨 Disconnect 🚨", callback_data=f"warn({c_id}|{c_name}|disconnect)"
                                ),
                            
                            InlineKeyboardButton
                                (
                                    "Delete ❌", callback_data=f"warn({c_id}|{c_name}|c_delete)"
                                )
                        ]
            ]

        else:
            buttons = [ 
                        [
                            InlineKeyboardButton
                                (
                                    "💠 Connect 💠", callback_data=f"warn({c_id}|{c_name}|connect)"
                                ),
                            
                            InlineKeyboardButton
                                (
                                    "Delete ❌", callback_data=f"warn({c_id}|{c_name}|c_delete)"
                                )
                        ]
            ]

        buttons.append(
                [
                    InlineKeyboardButton
                        (
                            "Delete Filters ⚠", callback_data=f"warn({c_id}|{c_name}|f_delete)"
                        )
                ]
        )
        
        buttons.append(
                [
                    InlineKeyboardButton
                        (
                            "🔙 Back", callback_data=f"channel_list({chat_id}|{chat_name})"
                        )
                ]
        )

        reply_markup = InlineKeyboardMarkup(buttons)
            
        await update.message.edit_text(
                text, reply_markup=reply_markup, parse_mode="html"
            )


    elif re.fullmatch(r"connect\((.+)\)", query_data):
        """
        A Callback Funtion Helping The user To Make A Chat Active Chat Which Will
        Make The Bot To Fetch Results From This Channel Too
        """

        if update.message.reply_to_message.sender_chat == None:
            if verify.get(str(update.message.reply_to_message.message_id)) != update.from_user.id:
                return

        c_id, c_name = re.findall(r"connect\((.+)\)", query_data)[0].split("|", 1)
        c_id = int(c_id)
        
        f_count = await db.cf_count(chat_id, c_id)
        
        add_active = await db.update_active(chat_id, c_id, c_name)
        
        if not add_active:
            await update.answer(f"<code>{c_name}</code> Is Aldready in Active Connection", show_alert=True)
            return

        text= f"<i>Sucessfully Connected To</i> <code>{c_name}</code>\n"
        text+=f"\n<i>Info About <b>{c_name}</b></i>\n"
        text+=f"\n<i>Channel Name:</i> <code>{c_name}</code>\n"
        text+=f"\n<i>Channel ID:</i> <code>{c_id}</code>\n"
        text+=f"\n<i>Channel Files:</i> <code>{f_count}</code>\n"
        text+=f"\n<i>Current Status:</i> <code>Connected</code>\n"

        buttons = [
                    [
                        InlineKeyboardButton
                            (
                                "🚨 Disconnect 🚨", callback_data=f"warn({c_id}|{c_name}|disconnect)"
                            ),
                        
                        InlineKeyboardButton
                            (
                                "Delete ❌", callback_data=f"warn({c_id}|{c_name}|c_delete)"
                            )
                    ]
        ]
        
        buttons.append(
                [
                    InlineKeyboardButton
                        (
                            "Delete Filters ⚠", callback_data=f"warn({c_id}|{c_name}|f_delete)"
                        )
                ]
        )
        
        buttons.append(
                [
                    InlineKeyboardButton
                        (
                            "🔙 Back", callback_data=f"channel_list({chat_id}|{chat_name})"
                        )
                ]
        )
        await ReCacher(chat_id, False, True, bot, update)
        
        reply_markup = InlineKeyboardMarkup(buttons)
            
        await update.message.edit_text(
                text, reply_markup=reply_markup, parse_mode="html"
            )


    elif re.fullmatch(r"disconnect\((.+)\)", query_data):
        """
        A Callback Funtion Helping The user To Make A Chat inactive Chat Which Will
        Make The Bot To Avoid Fetching Results From This Channel
        """
        if update.message.reply_to_message.sender_chat == None:
            if verify.get(str(update.message.reply_to_message.message_id)) != update.from_user.id:
                return

        c_id, c_name = re.findall(r"connect\((.+)\)", query_data)[0].split("|", 1)
        
        f_count = await db.cf_count(chat_id, int(c_id))
        
        remove_active = await db.del_active(chat_id, int(c_id))
        
        if not remove_active:
            await update.message.edit_text("Couldnt Full Fill YOur Request...\n Report This @CrazyBotszGrp Along With Bot's Log")
            return
        
        text= f"<i>Sucessfully Disconnected From</i> <code>{c_name}</code>\n"
        text+=f"\n<i>Info About <b>{c_name}</b></i>\n"
        text+=f"\n<i>Channel Name:</i> <code>{c_name}</code>\n"
        text+=f"\n<i>Channel ID:</i> <code>{c_id}</code>\n"
        text+=f"\n<i>Channel Files:</i> <code>{f_count}</code>\n"
        text+=f"\n<i>Current Status:</i> <code>Disconnected</code>\n"
        
        buttons = [ 
                    [
                        InlineKeyboardButton
                            (
                                "💠 Connect 💠", callback_data=f"warn({c_id}|{c_name}|connect)"
                            ),
                        
                        InlineKeyboardButton
                            (
                                "Delete ❌", callback_data=f"warn({c_id}|{c_name}|c_delete)"
                            )
                    ]
        ]
        
        buttons.append(
                [
                    InlineKeyboardButton
                        (
                            "Delete Filters ⚠", callback_data=f"warn({c_id}|{c_name}|f_delete)"
                        )
                ]
        )
        
        buttons.append(
                [
                    InlineKeyboardButton
                        (
                            "🔙 Back", callback_data=f"channel_list({chat_id}|{chat_name})"
                        )
                ]
        )
        
        reply_markup = InlineKeyboardMarkup(buttons)
        
        await ReCacher(chat_id, False, True, bot, update)

        await update.message.edit_text(
                text, reply_markup=reply_markup, parse_mode="html"
            )


    elif re.fullmatch(r"c_delete\((.+)\)", query_data):
        """
        A Callback Funtion For Delete A Channel Connection From A Group Chat History
        Along With All Its Filter Files
        """
        if update.message.reply_to_message.sender_chat == None:
            if verify.get(str(update.message.reply_to_message.message_id)) != update.from_user.id:
                return

        c_id, c_name = re.findall(r"c_delete\((.+)\)", query_data)[0].split("|", 1)
        c_id = int(c_id)
        
        c_delete = await db.del_chat(chat_id, c_id)
        a_delete = await db.del_active(chat_id, c_id) # pylint: disable=unused-variable
        f_delete = await db.del_filters(chat_id, c_id)

        if (c_delete and f_delete ):
            text=f"<code>{c_name} [ {c_id} ]</code> Has Been Sucessfully Deleted And All Its Files Were Cleared From DB...."

        else:
            text=f"<i>Couldn't Delete Channel And All Its Files From DB Sucessfully....</i>\n<i>Please Try Again After Sometimes...Also Make Sure To Check The Logs..!!</i>"
            await query.answer(text=text, show_alert=True)

        buttons = [
            [
                InlineKeyboardButton
                    (
                        "🔙 Back", callback_data=f"channel_list({chat_id}|{chat_name})"
                    ),
                    
                InlineKeyboardButton
                    (
                        "Close 🔐", callback_data="close"
                    )
            ]
        ]

        await ReCacher(chat_id, True, True, bot, update)
        
        reply_markup=InlineKeyboardMarkup(buttons)

        await update.message.edit_text(
            text, reply_markup=reply_markup, parse_mode="html"
        )


    elif re.fullmatch(r"f_delete\((.+)\)", query_data):
        """
        A Callback Funtion For Delete A Specific Channel's Filters Connected To A Group
        """
        if update.message.reply_to_message.sender_chat == None:
            if verify.get(str(update.message.reply_to_message.message_id)) != update.from_user.id:
                return

        c_id, c_name = re.findall(r"f_delete\((.+)\)", query_data)[0].split("|", 1)

        f_delete = await db.del_filters(chat_id, int(c_id))

        if not f_delete:
            text="<b><i>Oops..!!</i></b>\n\nEncountered Some Error While Deleteing Filters....\nPlease Check The Logs...."
            await update.answer(text=text, show_alert=True)
            return
    
        text =f"All Filters Of <code>{c_id}[{c_name}]</code> Has Been Deleted Sucessfully From My DB.."

        buttons=[
            [
                InlineKeyboardButton
                    (
                        "Back", callback_data="settings"
                    ),
                
                InlineKeyboardButton
                    (
                        "Close", callback_data="close"
                    )
            ]
        ]

        reply_markup = InlineKeyboardMarkup(buttons)

        await update.message.edit_text(
            text, reply_markup=reply_markup, parse_mode="html"
        )
    

    elif re.fullmatch(r"types\((.+)\)", query_data):
        """
        A Callback Funtion For Changing The Result Types To Be Shown In While Sending Results
        """
        if update.message.reply_to_message.sender_chat == None:
            if verify.get(str(update.message.reply_to_message.message_id)) != update.from_user.id:
                return

        chat_id, chat_name = re.findall(r"types\((.+)\)", query_data)[0].split("|", 1)
        
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


    elif re.fullmatch(r"toggle\((.+)\)", query_data):
        """
        A Callback Funtion Support handler For types()
        """
        if update.message.reply_to_message.sender_chat == None:
            if verify.get(str(update.message.reply_to_message.message_id)) != update.from_user.id:
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


    elif re.fullmatch(r"config\((.+)\)", query_data):
        """
        A Callback Funtion For Chaning The Number Of Total Pages / 
        Total Results / Results Per pages / Enable or Diable Invite Link
        """
        if update.message.reply_to_message.sender_chat == None:
            if verify.get(str(update.message.reply_to_message.message_id)) != update.from_user.id:
                return

        chat_id, chat_name = re.findall(r"config\((.+)\)", query_data)[0].split("|", 2)
        
        settings = await db.find_chat(int(chat_id))
        
        mp_count = settings["configs"]["max_pages"]
        mf_count = settings["configs"]["max_results"]
        mr_count = settings["configs"]["max_per_page"]
        show_invite = settings["configs"]["show_invite_link"]
        
        text=f"<i><b>Configure Your <u><code>{chat_name}</code></u> Group's Filter Settings...</b></i>\n"
        
        text+=f"\n<i>{chat_name}</i> Current Settings:\n"

        text+=f"\n - Max Filter Per Page: <code>{mr_count}</code>\n"
        
        text+=f"\n - Max Filter: <code>{mf_count}</code>\n"
        
        text+=f"\n - Max Pages: <code>{mp_count}</code>\n"
        
        text+=f"\n - Show Invitation Link: <code>{show_invite}</code>\n"
        
        text+="\nAdjust Above Value Using Buttons Below... "
        buttons=[
            [
                InlineKeyboardButton
                    (
                        "Filter Per Page", callback_data=f"mr_count({mr_count}|{chat_id}|{chat_name})"
                    ), 
        
                InlineKeyboardButton
                    (
                        "Max Pages",       callback_data=f"mp_count({mp_count}|{chat_id}|{chat_name})"
                    )
            ]
        ]
        
        buttons.append(
            [
                InlineKeyboardButton
                    (
                        "Total Filter Count", callback_data=f"mf_count({mf_count}|{chat_id}|{chat_name})"
                    )
            ]
        )
        
        buttons.append(
            [
                InlineKeyboardButton
                    (
                        "Show Invite Links", callback_data=f"showInvites({show_invite}|{chat_id}|{chat_name})"
                    )
            ]
        )
        buttons.append(
            [
                InlineKeyboardButton
                    (
                        "🔙 Back", callback_data=f"settings"
                    )
            ]
        )
        
        
        reply_markup=InlineKeyboardMarkup(buttons)
        
        await update.message.edit_text(
            text, 
            reply_markup=reply_markup, 
            parse_mode="html"
        )


    elif re.fullmatch(r"mr_count\((.+)\)", query_data):
        """
        A Callback Funtion For Changing The Count Of Result To Be Shown Per Page
        """
        if update.message.reply_to_message.sender_chat == None:
            if verify.get(str(update.message.reply_to_message.message_id)) != update.from_user.id:
                return

        count, chat_id, chat_name = re.findall(r"mr_count\((.+)\)", query_data)[0].split("|", 2)
    
        text = f"<i>Choose Your Desired 'Max Filter Count Per Page' For Every Filter Results Shown In</i> <code>{chat_name}</code>"
    
        buttons = [
            [
                InlineKeyboardButton
                    (
                        "5 Filters", callback_data=f"set(per_page|5|{chat_id}|{count})"
                    )
            ],
            [
                InlineKeyboardButton
                    (
                        "10 Filters", callback_data=f"set(per_page|10|{chat_id}|{count})"
                    )
            ],
            [
                InlineKeyboardButton
                    (
                        "15 Filters", callback_data=f"set(per_page|15|{chat_id}|{count})"
                    )
            ],
            [
                InlineKeyboardButton
                    (
                        "20 Filters", callback_data=f"set(per_page|20|{chat_id}|{count})"
                    )
            ],
            [
                InlineKeyboardButton
                    (
                        "25 Filters", callback_data=f"set(per_page|25|{chat_id}|{count})"
                    )
            ],
            [
                InlineKeyboardButton
                    (
                        "30 Filters", callback_data=f"set(per_page|30|{chat_id}|{count})"
                    )
            ],
            [
                InlineKeyboardButton
                    (
                        "🔙 Back", callback_data=f"config({chat_id}|{chat_name})"
                    )
            ]
        ]
    
        reply_markup = InlineKeyboardMarkup(buttons)
    
        await update.message.edit_text(
            text, reply_markup=reply_markup, parse_mode="html"
        )


    elif re.fullmatch(r"mp_count\((.+)\)", query_data):
        """
        A Callback Funtion For Changing The Count Of Maximum Result Pages To Be Shown
        """
        if update.message.reply_to_message.sender_chat == None:
            if verify.get(str(update.message.reply_to_message.message_id)) != update.from_user.id:
                return

        count, chat_id, chat_name = re.findall(r"mp_count\((.+)\)", query_data)[0].split("|", 2)
        
        text = f"<i>Choose Your Desired 'Max Filter Page Count' For Every Filter Results Shown In</i> <code>{chat_name}</code>"
        
        buttons = [

            [
                InlineKeyboardButton
                    (
                        "2 Pages", callback_data=f"set(pages|2|{chat_id}|{count})"
                    )
            ],
            [
                InlineKeyboardButton
                    (
                        "4 Pages", callback_data=f"set(pages|4|{chat_id}|{count})"
                    )
            ],
            [
                InlineKeyboardButton
                    (
                        "6 Pages", callback_data=f"set(pages|6|{chat_id}|{count})"
                    )
            ],
            [
                InlineKeyboardButton
                    (
                        "8 Pages", callback_data=f"set(pages|8|{chat_id}|{count})"
                    )
            ],
            [
                InlineKeyboardButton
                    (
                        "10 Pages", callback_data=f"set(pages|10|{chat_id}|{count})"
                    )
            ],
            [
                InlineKeyboardButton
                    (
                        "🔙 Back", callback_data=f"config({chat_id}|{chat_name})"
                    )
            ]

        ]
        
        reply_markup = InlineKeyboardMarkup(buttons)
        
        await update.message.edit_text(
            text, reply_markup=reply_markup, parse_mode="html"
        )


    elif re.fullmatch(r"mf_count\((.+)\)", query_data):
        """
        A Callback Funtion For Changing The Count Of Maximum Files TO Be Fetched From Database
        """
        if update.message.reply_to_message.sender_chat == None:
            if verify.get(str(update.message.reply_to_message.message_id)) != update.from_user.id:
                return

        count, chat_id, chat_name = re.findall(r"mf_count\((.+)\)", query_data)[0].split("|", 2)

        text = f"<i>Choose Your Desired 'Max Filter' To Be Fetched From DB For Every Filter Results Shown In</i> <code>{chat_name}</code>"

        buttons = [

            [
                InlineKeyboardButton
                    (
                        "50 Results", callback_data=f"set(results|50|{chat_id}|{count})"
                    )
            ],
            [
                InlineKeyboardButton
                    (
                        "100 Results", callback_data=f"set(results|100|{chat_id}|{count})"
                    )
            ],
            [
                InlineKeyboardButton
                    (
                        "150 Results", callback_data=f"set(results|150|{chat_id}|{count})"
                    )
            ],
            [
                InlineKeyboardButton
                    (
                        "200 Results", callback_data=f"set(results|200|{chat_id}|{count})"
                    )
            ],
            [
                InlineKeyboardButton
                    (
                        "250 Results", callback_data=f"set(results|250|{chat_id}|{count})"
                    )
            ],
            [
                InlineKeyboardButton
                    (
                        "300 Results", callback_data=f"set(results|300|{chat_id}|{count})"
                    )
            ],
            [
                InlineKeyboardButton
                    (
                        "🔙 Back", callback_data=f"config({chat_id}|{chat_name})"
                    )
            ]
        ]

        reply_markup = InlineKeyboardMarkup(buttons)

        await update.message.edit_text(
            text, reply_markup=reply_markup, parse_mode="html"
        )


    elif re.fullmatch(r"showInvites\((.+)\)", query_data):
        """
        A Callback Funtion For Enabling Or Diabling Invite Link Buttons
        """
        if update.message.reply_to_message.sender_chat == None:
            if verify.get(str(update.message.reply_to_message.message_id)) != update.from_user.id:
                return

        value, chat_id, chat_name = re.findall(r"showInvites\((.+)\)", query_data)[0].split("|", 2)
        
        value = True if value=="True" else False
        
        if value:
            buttons= [
                [
                    InlineKeyboardButton
                        (
                            "Disable ❌", callback_data=f"set(showInv|False|{chat_id}|{value})"
                        )
                ],
                [
                    InlineKeyboardButton
                        (
                            "Back 🔙", callback_data=f"config({chat_id}|{chat_name})"
                        )
                ]
            ]
        
        else:
            buttons =[
                [
                    InlineKeyboardButton
                        (
                            "Enable ✔", callback_data=f"set(showInv|True|{chat_id}|{value})"
                        )
                ],
                [
                    InlineKeyboardButton
                        (
                            "Back 🔙", callback_data=f"config({chat_id}|{chat_name})"
                        )
                ]
            ]
        
        text=f"<i>This Config Will Help You To Show Invitation Link Of All Active Chats Along With The Filter Results For The Users To Join.....</i>"
        
        reply_markup=InlineKeyboardMarkup(buttons)
        
        await update.message.edit_text(
            text,
            reply_markup=reply_markup,
            parse_mode="html"
        )
        

    elif re.fullmatch(r"set\((.+)\)", query_data):
        """
        A Callback Funtion Support For config()
        """
        if update.message.reply_to_message.sender_chat == None:
            if verify.get(str(update.message.reply_to_message.message_id)) != update.from_user.id:
                return

        action, val, chat_id, curr_val = re.findall(r"set\((.+)\)", query_data)[0].split("|", 3)

        try:
            val, chat_id, curr_val = int(val), int(chat_id), int(curr_val)
        except:
            chat_id = int(chat_id) # Quick bypass with try and 
            # except for show Invite Lol😂🤣
        
        if val == curr_val:
            await update.answer("New Value Cannot Be Old Value...Please Choose Different Value...!!!", show_alert=True)
            return
        
        prev = await db.find_chat(chat_id)

        p_max_pages = int(prev["configs"].get("max_pages"))
        p_max_results = int(prev["configs"].get("max_results"))
        p_max_per_page = int(prev["configs"].get("max_per_page"))
        show_invite_link = True if prev["configs"]["show_invite_link"] == True else False
        
        if action == "pages":
            p_max_pages = val
            
        elif action == "results":
            p_max_results = val
            
        elif action == "per_page":
            p_max_per_page = val
            
        elif action =="showInv":
            show_invite_link = True if val=="True" else False

        new = dict(
            max_pages=p_max_pages,
            max_results=p_max_results,
            max_per_page=p_max_per_page,
            show_invite_link=show_invite_link
        )
        
        append_db = await db.update_configs(chat_id, new)
        
        if not append_db:
            text="Something Wrong Please Check Bot Log For More Information...."
            await query.answer(text=text, show_alert=True)
            return
        
        text=f"Your Request Was Updated Sucessfully....\nNow All Upcoming Results Will Show According To This Settings..."
            
        buttons = [
            [
                InlineKeyboardButton
                    (
                        "Back 🔙", callback_data=f"config({chat_id}|{chat_name})"
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


    elif re.fullmatch(r"status\((.+)\)", query_data):
        """
        A Callback Funtion For Showing Overall Status Of A Group
        """
        if update.message.reply_to_message.sender_chat == None:
            if verify.get(str(update.message.reply_to_message.message_id)) != update.from_user.id:
                return
        
        chat_id, chat_name = re.findall(r"status\((.+)\)", query_data)[0].split("|", 2)
        
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


    elif re.fullmatch(r"about\((.+)\)", query_data):
        """
        A Callback Funtion For Showing About Section In Bot Setting Menu
        """
        if update.message.reply_to_message.sender_chat == None:
            if verify.get(str(update.message.reply_to_message.message_id)) != update.from_user.id:
                return

        text=f"<i><u>Bot's Status</u></i>\n"
        text+=f"\n<b><i>Bot's Uptime:</i></b> <code>{time_formatter(time.time() - start_uptime)}</code>\n"
        text+=f"\n<b><i>Bot Funtion:</i></b> <i>Auto Filter Files</i>\n"
        text+=f"""\n<b><i>Bot Support:</i></b> <a herf="https://t.me/CrazyBotszGrp">@CrazyBotszGrp</a>\n"""
        text+="""\n<b><i>Source Code:</i></b> <a herf="https://github.com/AlbertEinsteinTG/Adv-Filter-Bot">Source</a>"""

        buttons = [
            [
                InlineKeyboardButton
                    (
                        "My Dev ⚡", url="https://t.me/AlbertEinstein_TG"
                    ),
                    
                InlineKeyboardButton
                    (
                        "🔙 Back", callback_data="settings"
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
            text, reply_markup=reply_markup, parse_mode="html"
        )

        
    elif query_data == "start":
        buttons = [[
            InlineKeyboardButton('My Dev 👨‍🔬', url='https://t.me/AlbertEinstein_TG'),
            InlineKeyboardButton('Source Code 🧾', url ='https://github.com/AlbertEinsteinTG/Adv-Auto-Filter-Bot')
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



def time_formatter(seconds: float) -> str:
    """ humanize time """
    
    minutes, seconds = divmod(int(seconds),60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + "d, ") if days else "") + \
        ((str(hours) + "h, ") if hours else "") + \
        ((str(minutes) + "m, ") if minutes else "") + \
        ((str(seconds) + "s, ") if seconds else "")
    return tmp[:-2]

