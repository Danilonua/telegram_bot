from aiogram import types, Dispatcher

from sql.search import Search
from sql.back_up_of_bd import BD
from main.creat_bot import bot
from help_commands.ban_files.ban_commands.ban_reason.ban_reason import cmd_ban_reason


async def cmd_unwarn(message: types.Message):
    search = Search(0, 0, None)
    db = BD(0, 0, None)
    result = search.search_level(message.chat.id, message.from_user.id)
    result = str(result)[1:][:1]
    if result == "4" or result == "3" or result == "2":
        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
            chat_member = await bot.get_chat_member(message.chat.id, user_id)
            if chat_member.is_chat_member():
                check_warns = str(search.search_warns(message.chat.id, user_id))
                if check_warns is None or check_warns == "0":
                    await message.reply("У пользователя  не было варнов")
                else:
                    check_warns = int(search.search_warns(message.chat.id, user_id))
                    if check_warns > 0:
                        warns = db.un_warn_db(message.chat.id, user_id)
                        await message.reply(f"У пользователя теперь {warns} варнов")
            else:
                await message.reply("Пользователь не в чате!")
        else:
            cut_ban = await cmd_ban_reason(message, 1)
            if "@" in cut_ban:
                user_name = cut_ban[1:]
                result = search.search_id(message.chat.id, user_name)
                if result is None:
                    pass
                else:
                    user_id = str(result)[1:][:10]
                    chat_member = await bot.get_chat_member(message.chat.id, user_id)
                    if chat_member.is_chat_member():
                        check_warns = str(search.search_warns(message.chat.id, user_id))
                        if check_warns is None or check_warns == "0":
                            await message.reply("У пользователя не было варнов")
                        else:
                            check_warns = int(search.search_warns(message.chat.id, user_id))
                            if check_warns > 0:
                                warns = db.un_warn_db(message.chat.id, user_id)
                                await message.reply(f"У пользователя теперь {warns} варнов")
                    else:
                        await message.reply("Убедитесь что правильно написали айди")
                    return
            value_error_true = str([message.text[9:][:10]])
            value_error_true_convert = eval(value_error_true)
            user_id = int(value_error_true_convert[0])
            chat_member = await bot.get_chat_member(message.chat.id, user_id)
            if chat_member.is_chat_member():
                check_warns = str(search.search_warns(message.chat.id, user_id))
                if check_warns is None or check_warns == "0":
                    await message.reply("У пользователя  не было варнов")
                else:
                    check_warns = int(search.search_warns(message.chat.id, user_id))
                    if check_warns > 0:
                        warns = db.un_warn_db(message.chat.id, user_id)
                        await message.reply(f"У пользователя теперь {warns} варнов")
            else:
                await message.reply("Убедитесь что правильно написали айди")
            return
    else:
        await message.reply(f"Этой командой может пользоваться только администратор!")


def register_handlers_unwarn(dp: Dispatcher):
    dp.register_message_handler(cmd_unwarn, commands='unwarn')