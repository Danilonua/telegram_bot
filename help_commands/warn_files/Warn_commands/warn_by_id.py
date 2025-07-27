import asyncio
from aiogram import types
from main.creat_bot import bot
import datetime
from sql.back_up_of_bd import BD
from sql.search import Search
from sql.update import Update
from help_commands.ban_files.ban_commands.ban_reason.ban_reason import cmd_ban_reason

global ban_time


async def cmd_warn_by_id(message: types.Message):
    global ban_time
    search = Search(0, 0, None)
    update = Update(0, 0, None)
    db = BD(0, 0, None)
    cut_ban = await cmd_ban_reason(message, 1)
    words = message.text.split()
    if "@" in cut_ban:
        ckeck = words[1]
        if ckeck.isdigit():
            ban_time_int = int(ckeck)
            user_name = message.text.split()[2][1:]
            result = str(search.search_id(message.chat.id, user_name))
            user_id = "".join(filter(str.isdigit, result))
            date = datetime.datetime.now() + datetime.timedelta(days=ban_time_int)
            until_date = int(date.timestamp())
            chat_member = await bot.get_chat_member(message.chat.id, user_id)
            if chat_member.is_chat_member():
                if "Причина" in message.text:
                    reason = await cmd_ban_reason(message, 4)
                    check_warns = str(search.search_warns(message.chat.id, user_id))
                    if check_warns is None or check_warns == "0":
                        update.update_warns(0, message.chat.id, user_id)
                    db.warn_db(message.chat.id, user_id)
                    new_check_warns = str(search.search_warns(message.chat.id, user_id))
                    if "3" in new_check_warns:
                        await bot.kick_chat_member(message.chat.id, user_id)
                        await message.reply(f"Пользователь был забаненный, из-за 3 варнов.")
                        update.update_warns(0, message.chat.id, user_id)
                    await message.reply(
                        f"Пользователь получил варн. Он/она сейчас имеет {new_check_warns} варна "
                        f"\nВарн будет снят через"
                        f" {ckeck} дней\n"
                        f"Причина: {reason}")
                    await asyncio.sleep(until_date)
                    new_check_warns = str(search.search_warns(message.chat.id, user_id))
                    if new_check_warns is not None:
                        warns_count = db.un_warn_db(message.chat.id, user_id)
                        await message.reply(f"Варн был снят, он/она сейчас имеет {warns_count} варна")
                else:
                    check_warns = str(search.search_warns(message.chat.id, user_id))
                    if check_warns is None or check_warns == "0":
                        update.update_warns(0, message.chat.id, user_id)
                    db.warn_db(message.chat.id, user_id)
                    new_check_warns = str(search.search_warns(message.chat.id, user_id))
                    if "3" in new_check_warns:
                        await bot.kick_chat_member(message.chat.id, user_id)
                        await message.reply(f"Пользователь был забаненный, из-за 3 варнов.")
                        update.update_warns(0, message.chat.id, user_id)
                    await message.reply(
                        f"Пользователь получил варн. Он/она сейчас имеет {new_check_warns} варна \n"
                        f"Варн будет снят через"
                        f" {ckeck} дней")
                    await asyncio.sleep(until_date)
                    new_check_warns = str(search.search_warns(message.chat.id, user_id))
                    if new_check_warns is not None:
                        warns_count = db.un_warn_db(message.chat.id, user_id)
                        await message.reply(f"Варн был снят, он/она сейчас имеет {warns_count} варна")
        else:
            user_name = message.text.split()[1][1:]
            result = search.search_id(message.chat.id, user_name)
            if result is None:
                pass
            else:
                user_id = str(result)[1:][:10]
                chat_member = await bot.get_chat_member(message.chat.id, user_id)
                if chat_member.is_chat_member():
                    if "Причина" in message.text:
                        reason = await cmd_ban_reason(message, 3)
                        check_warns = str(search.search_warns(message.chat.id, user_id))
                        if check_warns is None or check_warns == "0":
                            update.update_warns(1, message.chat.id, user_id)
                        else:
                            db.warn_db(message.chat.id, user_id)
                        new_check_warns = str(search.search_warns(message.chat.id, user_id))
                        if "3" in new_check_warns:
                            await bot.kick_chat_member(message.chat.id, user_id)
                            await message.reply(f"Пользователь был забаненный, из-за 3 варнов.")
                            update.update_warns(0, message.chat.id, user_id)
                        await message.reply(
                            f"Пользователь получил варн.\nУ него сейчас {new_check_warns} варнов.\nПричина: {reason}")
                    else:
                        check_warns = str(search.search_warns(message.chat.id, user_id))
                        if check_warns is None or check_warns == "0":
                            update.update_warns(1, message.chat.id, user_id)
                        else:
                            db.warn_db(message.chat.id, user_id)
                        new_check_warns = str(search.search_warns(message.chat.id, user_id))
                        if "3" in new_check_warns:
                            await bot.kick_chat_member(message.chat.id, user_id)
                            await message.reply(f"Пользователь был забаненный, из-за 3 варнов.")
                            update.update_warns(0, message.chat.id, user_id)
                        await message.reply(f"Пользователь получил варн.\nУ него сейчас {new_check_warns} варна")
                else:
                    await message.reply("Убедитесь что правильно написали айди или не забыли время бана.")
    else:
        if len(message.text) == 20:
            ban_time = str(cut_ban[:1])
        if len(message.text) == 21:
            ban_time = str(cut_ban[:2])
        else:
            ban_time = str(cut_ban[:3])
        length_ban_time = len(ban_time)
        user_id = str(message.text[8 + length_ban_time:][:10])
        no_try = message.text.split()[1]
        if no_try.isdigit():
            user_id = int(user_id)
            ban_time_int = int(ban_time)
            date = datetime.datetime.now() + datetime.timedelta(days=ban_time_int)
            until_date = int(date.timestamp())
            try:
                chat_member = await bot.get_chat_member(message.chat.id, user_id)
                if chat_member.is_chat_member():
                    if 'Причина' in message.text:
                        reason = await cmd_ban_reason(message, 4)
                        check_warns = str(search.search_warns(message.chat.id, user_id))
                        if check_warns is None or check_warns == "0":
                            update.update_warns(0, message.chat.id, user_id)
                        db.warn_db(message.chat.id, user_id)
                        new_check_warns = str(search.search_warns(message.chat.id, user_id))
                        if "3" in new_check_warns:
                            await bot.kick_chat_member(message.chat.id, user_id)
                            await message.reply(f"Пользователь был забаненный, из-за 3 варнов.")
                            update.update_warns(0, message.chat.id, user_id)
                        await message.reply(
                            f"Пользователь получил варн. Он/она сейчас имеет {new_check_warns} варна \nВарн будет"
                            f" снят через"
                            f" {ban_time} дней"
                            f"Причина: {reason}")
                        await asyncio.sleep(until_date)
                        new_check_warns = str(search.search_warns(message.chat.id, user_id))
                        if new_check_warns is not None:
                            warns_count = db.un_warn_db(message.chat.id, user_id)
                            await message.reply(f"Варн был снят, он/она сейчас имеет {warns_count} варна")
                    else:
                        check_warns = str(search.search_warns(message.chat.id, user_id))
                        if check_warns is None or check_warns == "0":
                            update.update_warns(0, message.chat.id, user_id)
                        db.warn_db(message.chat.id, user_id)
                        new_check_warns = str(search.search_warns(message.chat.id, user_id))
                        if "3" in new_check_warns:
                            await bot.kick_chat_member(message.chat.id, user_id)
                            await message.reply(f"Пользователь был забаненный, из-за 3 варнов.")
                            update.update_warns(0, message.chat.id, user_id)
                        await message.reply(
                            f"Пользователь получил варн. Он/она сейчас имеет {new_check_warns} варна \n"
                            f"Варн будет снят через"
                            f" {ban_time} дней")
                        await asyncio.sleep(until_date)
                        new_check_warns = str(search.search_warns(message.chat.id, user_id))
                        if new_check_warns is not None:
                            warns_count = db.un_warn_db(message.chat.id, user_id)
                            await message.reply(f"Варн был снят, он/она сейчас имеет {warns_count} варна")
                else:
                    await message.reply('Пользователь не находится в чате')
            except UnboundLocalError:
                await message.reply("Неправильный формат команды")
                return
            except Exception as e:
                await message.reply(f" {e}")
                return
        else:
            value_error_true = str([message.text[7:][:10]])
            value_error_true_convert = eval(value_error_true)
            user_id = int(value_error_true_convert[0])
            chat_member = await bot.get_chat_member(message.chat.id, user_id)
            if chat_member.is_chat_member():
                if 'Причина' in message.text:
                    reason = await cmd_ban_reason(message, 3)
                    check_warns = str(search.search_warns(message.chat.id, user_id))
                    if check_warns is None or check_warns == "0":
                        update.update_warns(0, message.chat.id, user_id)
                    db.warn_db(message.chat.id, user_id)
                    new_check_warns = str(search.search_warns(message.chat.id, user_id))
                    if "3" in new_check_warns:
                        await bot.kick_chat_member(message.chat.id, user_id)
                        await message.reply(f"Пользователь был забаненный, из-за 3 варнов.")
                        update.update_warns(0, message.chat.id, user_id)
                    await message.reply(f"Пользователь получил варн.\nУ него сейчас {new_check_warns} варна\n"
                                        f"Причина: {reason}")
                else:
                    check_warns = str(search.search_warns(message.chat.id, user_id))
                    if check_warns is None or check_warns == "0":
                        update.update_warns(0, message.chat.id, user_id)
                    db.warn_db(message.chat.id, user_id)
                    new_check_warns = str(search.search_warns(message.chat.id, user_id))
                    if "3" in new_check_warns:
                        await bot.kick_chat_member(message.chat.id, user_id)
                        await message.reply(f"Пользователь был забаненный, из-за 3 варнов.")
                        update.update_warns(0, message.chat.id, user_id)
                    await message.reply(f"Пользователь получил варн.\nУ него сейчас {new_check_warns} варна")
            else:
                await message.reply("Убедитесь что правильно написали айди или не забыли время бана.")
            return