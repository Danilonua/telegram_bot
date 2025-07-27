from main.creat_bot import bot
from aiogram import types, Dispatcher
import random


async def ruletka(msg: types.Message):
    die = random.randint(1, 3)
    if die == 1:
        await bot.send_message(msg.chat.id, "Ого! Ты смельчак, но к сожелению сегодня проиграл.")
        await bot.kick_chat_member(msg.chat.id, msg.from_user.id)
    else:
        await bot.send_message(msg.chat.id, "Ого! Ты смельчак, и тебе сегодня повезло, но будь по осторожнее.")


def register_handlers_ruletka_command(dp: Dispatcher):
    dp.register_message_handler(ruletka, commands='ruletka')