from sql.update import Update
from aiogram import types, Dispatcher

update = Update(0, 0, None)


async def turn_off_spam_filter(message: types.Message):
    update.update_spam(message.chat.id, 0)
    await message.reply("Фильтр спама выключен. Весь спам будет храниться здесь!")


def register_handlers_spam_off_filter(dp: Dispatcher):
    dp.register_message_handler(turn_off_spam_filter, commands="spam", commands_prefix='+')
