from aiogram import types, Dispatcher
from main.creat_bot import bot


async def cmd_say(message: types.Message):
    text = message.text[5:]
    await bot.send_message(message.chat.id, text)


def register_handlers_say_command(dp: Dispatcher):
    dp.register_message_handler(cmd_say, commands='say')