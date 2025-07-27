from aiogram import types, Dispatcher
from sql.search import Search
from help_commands.warn_files.Warn_commands.warn_by_id import cmd_warn_by_id
from help_commands.warn_files.Warn_commands.warn_answer import cmd_warn_reply

global user_id


# @dp.message_handler(commands='warn')
async def cmd_warn(message: types.Message):
    global user_id
    try:
        search = Search(0, 0, None)
        result = search.search_level(message.chat.id, message.from_user.id)
        result = str(result)[1:][:1]
        if result == "4" or result == "3" or result == "2":
            if message.reply_to_message:
                await cmd_warn_reply(message)
            else:
                await cmd_warn_by_id(message)
        else:
            await message.reply(f"Этой командой может пользователь с 2 уровнем или выше!")
    except Exception as e:
        await message.reply(f"{e}")


def register_handlers_warn(dp: Dispatcher):
    dp.register_message_handler(cmd_warn, commands='warn')
