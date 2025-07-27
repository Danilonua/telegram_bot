from aiogram import types
import datetime
from main.creat_bot import bot
from sql.search import Search
from sql.update import Update
from help_commands.ban_files.ban_commands.ban_reason.ban_reason import cmd_ban_reason

search = Search(0, 0, None)
update = Update(0, 0, None)
global ban_time


async def cmd_mute_id(message: types.Message):
    global ban_time
    cut_ban = str(message.text[6:])
    words = message.text.split()
    if "@" in cut_ban:
        check = words[1]
        if check.isdigit():
            mute_duration = int(check)
            user_name = message.text.split()[2][1:]
            result = str(search.search_id(message.chat.id, user_name))
            user_id = "".join(filter(str.isdigit, result))
            until_date = datetime.datetime.now() + datetime.timedelta(hours=mute_duration)
            until_timestamp = int(until_date.timestamp())
            chat_member = await bot.get_chat_member(message.chat.id, user_id)
            if chat_member.is_chat_member():
                if 'Причина' in message.text:
                    reason = await cmd_ban_reason(message, 4)
                    await bot.restrict_chat_member(message.chat.id, user_id, until_date=until_timestamp)
                    await message.reply(f"Пользователь был замучен на {mute_duration} часов.\nПричина: {reason}")
                    update.update_mute(message.chat.id, user_id, 1)
                else:
                    await bot.restrict_chat_member(message.chat.id, user_id, until_date=until_timestamp)
                    await message.reply(f"Пользователь был замучен на {mute_duration} часов.")
                    update.update_mute(message.chat.id, user_id, 1)
            else:
                await message.reply('Пользователь не находится в чате')
        else:
            user_name = words[1][1:]
            result = search.search_id(message.chat.id, user_name)
            if result is None:
                pass
            else:
                user_id = str(result)[1:][:10]
                chat_member = await bot.get_chat_member(message.chat.id, user_id)
                if chat_member.is_chat_member():
                    if 'Причина' in message.text:
                        reason = await cmd_ban_reason(message, 3)
                        await bot.restrict_chat_member(message.chat.id, user_id)
                        update.update_mute(message.chat.id, user_id, 1)
                        await message.reply(
                            f"Пользователь был замучен на всегда.\nПричина: {reason}"
                            f"\nДля размута используйте команду /unmute"
                            f" как в инструции к боту")
                    else:
                        await bot.restrict_chat_member(message.chat.id, user_id)
                        update.update_mute(message.chat.id, user_id, 1)
                        await message.reply(
                            f"Пользователь был замучен на всегда.\nДля размута используйте команду /unmute"
                            f" как в инструции к боту")
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
        user_id = str(message.text[9:][length_ban_time - 1:][:9 + length_ban_time][:10])
        no_try = message.text.split()[1]
        if no_try.isdigit():
            user_id = int(user_id)
            ban_time_int = int(ban_time)
            date = datetime.datetime.now() + datetime.timedelta(hours=ban_time_int)
            until_date = int(date.timestamp())
            try:
                chat_member = await bot.get_chat_member(message.chat.id, user_id)
                if chat_member.is_chat_member():
                    if 'Причина' in message.text:
                        reason = await cmd_ban_reason(message, 4)
                        await bot.restrict_chat_member(message.chat.id, user_id, until_date=until_date)
                        update.update_mute(message.chat.id, user_id, 1)
                        await message.reply(f"Пользователь был замучен на {ban_time} часов.\nПричина: {reason}"
                                            f"\nДля размута используйте команду /unmute"
                                            f" как в инструции к боту")
                    else:
                        await bot.restrict_chat_member(message.chat.id, user_id, until_date=until_date)
                        update.update_mute(message.chat.id, user_id, 1)
                        await message.reply(f"Пользователь был замучен на {ban_time} часов.")
                else:
                    await message.reply('Пользователь не находится в чате')
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
                    await bot.restrict_chat_member(message.chat.id, user_id)
                    update.update_mute(message.chat.id, user_id, 1)
                    await message.reply(
                        f"Пользователь был замучен на всегда.\nПричина: {reason}"
                        f"\nДля размута используйте команду /unmute"
                        f" как в инструции к боту")
                else:
                    await bot.restrict_chat_member(message.chat.id, user_id)
                    await message.reply(
                        f"Пользователь был замучен на всегда.\nДля размута используйте команду /unmute"
                        f" как в инструции к боту")
                    update.update_mute(message.chat.id, user_id, 1)
            else:
                await message.reply("Убедитесь что правильно написали айди или не забыли время бана.")
        return