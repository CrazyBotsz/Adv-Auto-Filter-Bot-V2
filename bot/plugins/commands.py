#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) @AlbertEinsteinTG & @Mrk_YT


        
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
                                    '👨‍💼 𝙳𝚎𝚟𝚎𝚕𝚘𝚙𝚎𝚛𝚜 👨‍💼', url="https://t.me/Mo_TECH_YT/26"
                                )
                        ]
                    ]
                )
            )

        elif file_type == "video":
        
            await update.bot.send_video(
                chat_id=update.chat.id,
                video = file_id,
                caption = caption,
                parse_mode="html",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton
                                (
                                    '👨‍💼 𝙳𝚎𝚟𝚎𝚕𝚘𝚙𝚎𝚛𝚜 👨‍💼', url="https://t.me/Mo_TECH_YT/26"
                                )
                        ]
                    ]
                )
            )
            
        elif file_type == "audio":
        
            await update.bot.send_audio(
                chat_id=update.chat.id,
                audio = file_id,
                caption = caption,
                parse_mode="html",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton
                                (
                                    '👨‍💼 𝙳𝚎𝚟𝚎𝚕𝚘𝚙𝚎𝚛𝚜 👨‍💼', url="https://t.me/Mo_TECH_YT/26"
                                )
                        ]
                    ]
                )
            )

        else:
            print(file_type)
        
        return

    buttons = [[
        InlineKeyboardButton('👨‍💼 𝙼𝚊𝚜𝚝𝚎𝚛', url='https://t.me/MRK_YT'),
        InlineKeyboardButton('𝙷𝚎𝚕𝚙 🤔', callback_data="help")
    ],[
        InlineKeyboardButton('🖥️ 𝚃𝚞𝚝𝚘𝚛𝚒𝚊𝚕 𝚅𝚒𝚍𝚎𝚘 🖥️', url='https://youtu.be/uAHl5jvnrhk')
    ],[
        InlineKeyboardButton('🗣️ 𝙰𝚗𝚢 𝙳𝚘𝚞𝚋𝚝', url='https://t.me/Mo_Tech_group'),
        InlineKeyboardButton('𝚄𝚙𝚍𝚊𝚝𝚎𝚜 🤖', url='https://t.me/Mo_Tech_YT')
    ],[
        InlineKeyboardButton('💥 𝚂𝚞𝚋𝚜𝚌𝚛𝚒𝚋𝚎 𝙼𝚢 𝚈𝚘𝚞𝚃𝚞𝚋𝚎 𝙲𝚑𝚊𝚗𝚗𝚎𝚕 💥', url='https://youtube.com/channel/UCmGBpXoM-OEm-FacOccVKgQ')
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
        InlineKeyboardButton('🏠 𝙷𝚘𝚖𝚎', callback_data='start'),
        InlineKeyboardButton('𝙰𝚋𝚘𝚞𝚝 🚩', callback_data='about')
    ],[
        InlineKeyboardButton('🔐 𝙲𝚕𝚘𝚜𝚎 🔐', callback_data='close')
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
        InlineKeyboardButton('👤 @𝙼𝚛𝚔_𝚈𝚃 👤', url='https://t.me/MRK_YT')
    ],[
        InlineKeyboardButton('👤 @𝙰𝚕𝚋𝚎𝚛𝚝𝙴𝚒𝚗𝚜𝚝𝚎𝚒𝚗𝚃𝙶 👤', url='https://t.me/AlbertEinsteinTG')
    ],[
        InlineKeyboardButton('🏠 𝙷𝚘𝚖𝚎', callback_data='start'),
        InlineKeyboardButton('𝙲𝚕𝚘𝚜𝚎 🔐', callback_data='close')
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
