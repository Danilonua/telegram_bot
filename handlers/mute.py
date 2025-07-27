from aiogram import types, Dispatcher
from help_commands.mute_files.mute_commands.mute_by_id import cmd_mute_id
from help_commands.mute_files.mute_commands.mute_reply import cmd_mute_reply
from sql.search import Search


# @dp.message_handler(commands='mute')
async def cmd_mute(message: types.Message):
    try:
        search = Search(0, 0, None)
        result = search.search_level(message.chat.id, message.from_user.id)
        result = str(result)[1:][:1]
        if result == "3" or result == "4":
            if message.reply_to_message:
                await cmd_mute_reply(message)
            else:
                await cmd_mute_id(message)
        else:
            await message.reply(f"Этой командой может пользоваться только администратор!")
    except Exception as e:
        await message.reply(f"{e}")


def register_handlers_mute_file(dp: Dispatcher):
    dp.register_message_handler(cmd_mute, commands='mute')
