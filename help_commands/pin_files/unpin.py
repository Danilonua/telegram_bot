from aiogram import types, Dispatcher

from sql.search import Search
from main.creat_bot import bot


async def cmd_unpin(message: types.Message):
    search = Search(0, 0, None)
    result = search.search_level(message.chat.id, message.from_user.id)
    result = str(result)[1:][:1]
    if result == "4" or result == "3" or result == "2" or result == "1":
        try:
            await bot.unpin_chat_message(message.chat.id, message.reply_to_message.message_id)
        except AttributeError:
            await message.reply("Эта команда должна быть ответом на сообщение!")
            return
    else:
        await message.reply(f"Этой командой может пользоваться только администратор!")


def register_handlers_pin_command(dp: Dispatcher):
    dp.register_message_handler(cmd_unpin, commands='unpin')
