from aiogram import types
import asyncio
from main.creat_bot import bot
from sql.search import Search
from sql.update import Update
from sql.back_up_of_bd import BD
from help_commands.ban_files.ban_commands.ban_reason.ban_reason import cmd_ban_reason


async def cmd_warn_reply(message: types.Message):
    search = Search(0, 0, None)
    update = Update(0, 0, None)
    db = BD(0, 0, None)
    user_id = message.reply_to_message.from_user.id
    chat_member = await bot.get_chat_member(message.chat.id, user_id)
    words = message.text.split()
    if len(words) > 1:
        if chat_member.is_chat_member():
            check_warns = str(search.search_warns(message.chat.id, user_id))
            if check_warns is None:
                update.update_warns(0, message.chat.id, user_id)
            if "3" in check_warns:
                await bot.kick_chat_member(message.chat.id, user_id)
                await message.reply(f"Пользователь был забаненный, из-за 3 варнов.")
                update.update_warns(0, message.chat.id, user_id)
            else:
                # check if admin wants to warn forever
                if message.text.strip() == "/warn":
                    warns_count = db.warn_db(message.chat.id, user_id)
                    new_check_warns = str(search.search_warns(message.chat.id, user_id))
                    if "3" in new_check_warns:
                        await bot.kick_chat_member(message.chat.id, user_id)
                        await message.reply(f"Пользователь был забаненный, из-за 3 варнов.")
                        update.update_warns(0, message.chat.id, user_id)
                    else:
                        await message.reply(f"Пользователь получил варн. Он/она сейчас имеет {warns_count} варна")
                elif "Причина" in message.text and "1" or "2" or "3" or "4" or "5" or "6" or "7" or "8" or "9" not in message.text.split()[1]:
                    reason = await cmd_ban_reason(message, 2)
                    warns_count = db.warn_db(message.chat.id, user_id)
                    new_check_warns = str(search.search_warns(message.chat.id, user_id))
                    if "3" in new_check_warns:
                        await bot.kick_chat_member(message.chat.id, user_id)
                        await message.reply(f"ППользователь был забаненный, из-за 3 варнов.")
                        update.update_warns(0, message.chat.id, user_id)
                    else:
                        await message.reply(f"Пользователь получил варн. Он/она сейчас имеет {warns_count} варна\nПричина: {reason}")
                else:
                    try:
                        warn_time = int(message.text.split()[1])
                    except ValueError:
                        await message.reply("Пожалуйста правильно введите число")
                        return
                    if warn_time <= 0:
                        await message.reply("Пожалуйста, введите число больше чем 0!")
                        return
                    warn_time = int(warn_time * 60 * 60)
                    new_check_warns = str(search.search_warns(message.chat.id, user_id))
                    if "3" in new_check_warns:
                        await bot.kick_chat_member(message.chat.id, user_id)
                        await message.reply(f"Пользователь был забаненный, из-за 3 варнов.")
                        update.update_warns(0, message.chat.id, user_id)
                    else:
                        if 'Причина' in message.text:
                            reason = await cmd_ban_reason(message, 3)
                            warns_count = db.warn_db(message.chat.id, user_id)
                            await message.reply(
                                f"Пользователь получил варн. Он/она сейчас имеет {warns_count} варна \nВарн будет снят через"
                                f" {int(warn_time / 3600)} дней\n"
                                f"Причина: {reason}")
                            await asyncio.sleep(warn_time)
                            new_check_warns = str(search.search_warns(message.chat.id, user_id))
                            if new_check_warns is not None:
                                warns_count = db.un_warn_db(message.chat.id, user_id)
                                await message.reply(f"Варн был снят, он/она сейчас имеет {warns_count} варна")
                        else:
                            warns_count = db.warn_db(message.chat.id, user_id)
                            await message.reply(
                                f"Пользователь получил варн. Он/она сейчас имеет {warns_count} варна \nВарн будет снят через"
                                f" {int(warn_time / 3600)} дней")
                            await asyncio.sleep(warn_time)
                            new_check_warns = str(search.search_warns(message.chat.id, user_id))
                            if new_check_warns is not None:
                                warns_count = db.un_warn_db(message.chat.id, user_id)
                                await message.reply(f"Варн был снят, он/она сейчас имеет {warns_count} варна")
        else:
            await message.reply('Пользователь не является участником чата!')
            return
    else:
        if message.text.strip() == "/warn":
            warns_count = db.warn_db(message.chat.id, user_id)
            if warns_count is None:
                warns_count = 1
            new_check_warns = str(search.search_warns(message.chat.id, user_id))
            if "3" in new_check_warns:
                await bot.kick_chat_member(message.chat.id, user_id)
                await message.reply(f"Пользователь был забаненный, из-за 3 варнов.")
                update.update_warns(0, message.chat.id, user_id)
            else:
                await message.reply(f"Пользователь получил варн. Он/она сейчас имеет {warns_count} варна")
