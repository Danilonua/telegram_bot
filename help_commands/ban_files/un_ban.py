from aiogram import types, Dispatcher

from sql.search import Search
from sql.update import Update
from main.creat_bot import bot
from help_commands.ban_files.ban_commands.ban_reason.ban_reason import cmd_ban_reason

update = Update(0, 0, None)


async def cmd_unban(message: types.Message):
    """
    Unban user
    """
    search = Search(0, 0, None)
    result = search.search_level(message.chat.id, message.from_user.id)
    result = str(result)[1:][:1]
    if result == "4":
        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
            chat_member = await bot.get_chat_member(message.chat.id, user_id)
            if chat_member.is_chat_member():
                await message.reply('Пользователь не забаненный')
                return
            else:
                await bot.unban_chat_member(message.chat.id, user_id)
                update.update_ban(message.chat.id, user_id, 0)
                await message.reply("Пользователь разбаненный.")
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
                        await message.reply("Убедитесь что правильно написали имя и что пользователь забаненый")
                    else:
                        await bot.unban_chat_member(message.chat.id, user_id)
                        update.update_ban(message.chat.id, user_id, 0)
                        await message.reply("Пользователь был разбаненный.")
                    return
            else:
                value_error_true = str([message.text[8:][:10]])
                value_error_true_convert = eval(value_error_true)
                user_id = int(value_error_true_convert[0])
                chat_member = await bot.get_chat_member(message.chat.id, user_id)
                if chat_member.is_chat_member():
                    await message.reply("Убедитесь что правильно написали айди и что пользователь забаненый")
                else:
                    await bot.unban_chat_member(message.chat.id, user_id)
                    update.update_ban(message.chat.id, user_id, 0)
                    await message.reply("Пользователь был разбаненный.")
                return
    else:
        await message.reply(f"Этой командой может пользоваться только администратор!")


def register_handlers_unban(dp: Dispatcher):
    dp.register_message_handler(cmd_unban, commands='unban')