from aiogram import types, Dispatcher
from main.creat_bot import bot
from sql.search import Search


async def cmd_user_id(message: types.Message):
    search = Search(0, 0, None)
    if message.reply_to_message:
        await bot.send_message(message.chat.id, f"ID пользователя: `{message.reply_to_message.from_user.id}`"
                               , parse_mode="Markdown")
    else:
        if "@" in message.text:
            user_name = message.text.split()[1][1:]
            result = str(search.search_id(message.chat.id, user_name))
            user_id = result[1:][:len(result) - 3]
            await bot.send_message(message.chat.id, f"ID пользователя: `{user_id}`", parse_mode="Markdown")
        else:
            await message.reply(f"Эта команда должна быть ответом на сообщение или Вам"
                                f" надо упомянуть человека!")


async def cmd_group_id(message: types.Message):
    await bot.send_message(message.chat.id, f"ID группы: `{message.chat.id}`", parse_mode="Markdown")


async def cmd_usernames(message: types.Message):
    username = message.from_user.username
    if username:
        await bot.send_message(message.chat.id, f"Ваше имя: `{username}`", parse_mode="Markdown")
    else:
        await bot.send_message(message.chat.id, f"К сожелению у вас не было найдено юзернейма.\n"
                                                f"Вам нужно срочно зайти в <a href='https://teletype.in/@pythonhelper/NlOZOS5iAB5#X8RX'>инструкцию</a> к боту и поставить "
                                                f"юзернейм себе как написано в инструкции.", parse_mode="HTML")


def register_handlers_id_file(dp: Dispatcher):
    dp.register_message_handler(cmd_user_id, commands='user_id')
    dp.register_message_handler(cmd_group_id, commands='group_id')
    dp.register_message_handler(cmd_usernames, commands='username')