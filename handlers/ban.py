from aiogram import types, Dispatcher
from sql.search import Search
from help_commands.ban_files.ban_commands.ban_by_id import cmd_ban_by_id
from help_commands.ban_files.ban_commands.ban_reply import cmd_ban_reply


async def ban(message: types.Message):

    # Эта функция проверяет level пользователя, который вызвал эту команду. Дальше функция проверяет:
    # эта команда была ответом на сообщение или нет? Тогда функция ban вызывает функцию cmd_ban_reply или cmd_ban_by_id.

    try:
        search = Search(0, 0, None)
        result = search.search_level(message.chat.id, message.from_user.id)
        result = str(result)[1:][:1]
        if result == "4":
            if message.reply_to_message:
                await cmd_ban_reply(message)
            else:
                await cmd_ban_by_id(message)
        else:
            await message.reply(f"Этой командой может пользоваться только администратор!")
    except Exception as e:
        await message.reply(f"{e}")


def register_handlers_ban(dp: Dispatcher):
    dp.register_message_handler(ban, commands='ban')