from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant, FloodWait

from bot import verify # pylint: disable=import-error
from bot.bot import Bot # pylint: disable=import-error
from bot.database import Database # pylint: disable=import-error
from bot.plugins.auto_filter import ReCacher # pylint: disable=import-error

db = Database()

@Client.on_message(filters.command(["add"]) & filters.group, group=1)
async def connect(bot: Bot, update):
    """
    A Funtion To Handle Incoming /add Command TO COnnect A Chat With Group
    """
    chat_id = update.chat.id
    user_id = update.from_user.id if update.from_user else None
    target_chat = update.text.split(None, 1)[1]
    global verify
    
    if not verify[str(chat_id)]: # Make Admin's ID List
        admin_list = []
        async for x in bot.iter_chat_members(chat_id=chat_id, filter="administrators"):
            admin_id = x.user.id 
            admin_list.append(admin_id)
        admin_list.append(None)
        verify[str(chat_id)] = admin_list

    if not user_id in verify.get(str(chat_id)):
        return
    
    try:
        if target_chat.startswith("@"):
            if len(target_chat) < 5:
                await update.reply_text("Invalid Username...!!!")
                return
            target = target_chat
            
        elif not target_chat.startswith("@"):
            if len(target_chat) < 14:
                await update.reply_text("Invalid Chat Id...\nChat ID Should Be Something Like This: <code>-100xxxxxxxxxx</code>")
                return
            target = int(target_chat)
                
    except Exception:
        await update.reply_text("Invalid Input...\nYou Should Specify Valid <code>chat_id(-100xxxxxxxxxx)</code> or <code>@username</code>")
        return
    
    try:
        join_link = await bot.export_chat_invite_link(target)
    except Exception as e:
        print(e)
        await update.reply_text(f"Make Sure Im Admin At <code>{target}</code> And Have Permission For '<i>Inviting Users via Link</i>' And Try Again.....!!!")
        return
    
    userbot_info = await bot.USER.get_me()
    userbot_id = userbot_info.id
    userbot_name = userbot_info.first_name
    
    try:
        await bot.USER.join_chat(join_link)
        
    except UserAlreadyParticipant:
        pass
    
    except Exception:
        await update.reply_text(f"My UserBot [{userbot_name}](tg://user?id={userbot_id}) Couldnt Join The Channel `{target}` Make Sure Userbot Is Not Banned There Or Add It Manually And Try Again....!!")
        return
    
    try:
        c_chat = await bot.get_chat(target)
        channel_id = c_chat.id
        channel_name = c_chat.title
        
    except Exception as e:
        await update.reply_text("Encountered Some Issue..Please Check Logs..!!")
        raise e
        
        
    in_db = await db.in_db(chat_id, channel_id)
    
    if in_db:
        await update.reply_text("Channel Aldready In Db...!!!")
        return
    
    wait_msg = await update.reply_text("Please Wait Till I Add All Your Files From Channel To Db\n\n<i>This May Take 2 or 3 Mins Depending On Your No. Of Files In Channel.....</i>\n\nUntil Then Please Dont Sent Any Other Command Or This Operation May Be Intrupted....")
    
    try:
        type_list = ["video", "audio", "document"]
        data = []
        
        
        for typ in type_list:

            async for msgs in bot.USER.search_messages(channel_id,filter=typ): #Thanks To @PrgOfficial For Suggesting
                
                # Using 'if elif' instead of 'or' to determine 'file_type'
                # Better Way? Make A PR
                try:
                    if msgs.video:
                        file_id = msgs.video.file_id
                        file_name = msgs.video.file_name[0:-4]
                        file_type = "video"
                    
                    elif msgs.audio:
                        file_id = msgs.audio.file_id
                        file_name = msgs.audio.file_name[0:-4]
                        file_type = "audio"
                    
                    elif msgs.document:
                        file_id = msgs.document.file_id
                        file_name = msgs.document.file_name[0:-4]
                        file_type = "document"
                    
                    for i in ["_", "|", "-", "."]: # Work Around
                        try:
                            file_name = file_name.replace(i, " ")
                        except Exception:
                            pass
                    
                    file_link = msgs.link
                    group_id = chat_id
                    
                    dicted = dict(
                        file_id=file_id, # File Id For Future Updates Maybe...
                        chat_id=channel_id,
                        group_id=group_id,
                        file_name=file_name,
                        file_type=file_type,
                        file_link=file_link
                    )
                    
                    data.append(dicted)
                except Exception as e:
                    if 'NoneType' in str(e): # For Some Unknown Reason Some File Name is 'None'
                        continue
                    print(e)
                
    except Exception as e:
        await wait_msg.edit_text("Couldnt Fetch Files From Channel... Please look Into Logs For More Details")
        raise e
    
    await db.add_filters(data)
    await db.add_chat(chat_id, channel_id, channel_name)
    await ReCacher(chat_id, True, True, bot, update)
    
    await wait_msg.edit_text(f"Channel Was Sucessfully Added With <code>{len(data)}</code> Files..")


@Client.on_message(filters.command(["del"]) & filters.group, group=1)
async def disconnect(bot: Bot, update):
    """
    A Funtion To Handle Incoming /del Command TO Disconnect A Chat With A Group
    """
    chat_id = update.chat.id
    user_id = update.from_user.id if update.from_user else None
    target_chat = update.text.split(None, 1)[1]
    global verify
    
    if not verify[str(chat_id)]: # Make Admin's ID List
        admin_list = []
        async for x in bot.iter_chat_members(chat_id=chat_id, filter="administrators"):
            admin_id = x.user.id 
            admin_list.append(admin_id)
        admin_list.append(None)
        verify[str(chat_id)] = admin_list

    if not user_id in verify.get(str(chat_id)):
        return
    
    try:
        if target_chat.startswith("@"):
            if len(target_chat) < 5:
                await update.reply_text("Invalid Username...!!!")
                return
            target = target_chat
            
        elif not target_chat.startswith("@"):
            if len(target_chat) < 14:
                await update.reply_text("Invalid Chat Id...\nChat ID Should Be Something Like This: <code>-100xxxxxxxxxx</code>")
                return
            target = int(target_chat)
                
    except Exception:
        await update.reply_text("Invalid Input...\nYou Should Specify Valid chat_id(-100xxxxxxxxxx) or @username")
        return
    
    userbot = await bot.USER.get_me()
    userbot_name = userbot.first_name
    userbot_id = userbot.id
    
    try:
        channel_info = await bot.USER.get_chat(target)
        channel_id = channel_info.id
    except Exception:
        await update.reply_text(f"My UserBot [{userbot_name}](tg://user?id={userbot_id}) Couldnt Fetch Details Of `{target}` Make Sure Userbot Is Not Banned There Or Add It Manually And Try Again....!!")
        return
    
    in_db = await db.in_db(chat_id, channel_id)
    
    if not in_db:
        await update.reply_text("This Channel Is Not Connected With The Group...")
        return
    
    wait_msg = await update.reply_text("Deleting All Files Of This Channel From DB....!!!\n\nPlease Be Patience...Dont Sent Another Command Until This Process Finishes..")
    
    await db.del_filters(chat_id, channel_id)
    await db.del_active(chat_id, channel_id)
    await db.del_chat(chat_id, channel_id)
    await ReCacher(chat_id, True, True, bot, update)
    
    await wait_msg.edit_text("Sucessfully Deleted All Files From DB....")


@Client.on_message(filters.command(["delall"]) & filters.group, group=1)
async def delall(bot: Bot, update):
    """
    A Funtion To Handle Incoming /delall Command TO Disconnect All Chats From A Group
    """
    chat_id=update.chat.id
    user_id = update.from_user.id if update.from_user else None
    global verify
    
    if not verify[str(chat_id)]: # Make Admin's ID List
        admin_list = []
        async for x in bot.iter_chat_members(chat_id=chat_id, filter="administrators"):
            admin_id = x.user.id 
            admin_list.append(admin_id)
        admin_list.append(None)
        verify[str(chat_id)] = admin_list

    if not user_id in verify.get(str(chat_id)):
        return
    
    await db.delete_all(chat_id)
    await ReCacher(chat_id, True, True, bot, update)
    
    await update.reply_text("Sucessfully Deleted All Connected Chats From This Group....")


@Client.on_message(filters.channel & (filters.video | filters.audio | filters.document), group=0)
async def new_files(bot: Bot, update):
    """
    A Funtion To Handle Incoming New Files In A Channel ANd Add Them To Respective Channels..
    """
    channel_id = update.chat.id
    
    # Using 'if elif' instead of 'or' to determine 'file_type'
    # Better Way? Make A PR
    
    try:
        if update.video: 
            file_id = update.video.file_id
            file_name = update.video.file_name[0:-4]
            file_type = "video" 

        elif update.audio:
            file_id = update.audio.file_id
            file_name = update.audio.file_name[0:-4]
            file_type = "audio"

        elif update.document:
            file_id = update.document.file_id
            file_name = update.document.file_name[0:-4]
            file_type = "document"
        
        for i in ["_", "|", "-", "."]: # Work Around
            try:
                file_name = file_name.replace(i, " ")
            except Exception:
                pass
    except Exception as e:
        print(e)
        return
        
    
    file_link = update.link
    group_ids = await db.find_group_id(channel_id)
    
    data = []
    
    if group_ids:
        for group_id in group_ids:
            data_packets = dict(
                    file_id=file_id, # File Id For Future Updates Maybe...
                    chat_id=channel_id,
                    group_id=group_id,
                    file_name=file_name,
                    file_type=file_type,
                    file_link=file_link
                )
            
            data.append(data_packets)
        await db.add_filters(data)
    return

