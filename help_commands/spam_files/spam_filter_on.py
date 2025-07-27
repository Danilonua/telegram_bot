from sql.update import Update
from aiogram import types, Dispatcher

update = Update(0, 0, None)


async def turn_on_spam_filter(message: types.Message):
    update.update_spam(message.chat.id, 1)
    await message.reply("Фильтр спама включен. Весь спам будет удаляться и спамеры будут наказаны!")


def register_handlers_spam_on_filter(dp: Dispatcher):
    dp.register_message_handler(turn_on_spam_filter, commands="spam", commands_prefix='-')
