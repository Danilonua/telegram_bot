import asyncio
from aiogram import types, Dispatcher

from sql.search import Search
from main.creat_bot import bot


async def cmd_pin(message: types.Message):
    search = Search(0, 0, None)
    result = search.search_level(message.chat.id, message.from_user.id)
    result = str(result)[1:][:1]
    if result == "4" or result == "3" or result == "2" or result == "1":
        try:
            message_to_pin = message.reply_to_message
            if message_to_pin is None:
                await message.reply("Эта команда должна быть ответом на сообщение!")
                return

            if message.text == "/pin":
                await bot.pin_chat_message(message.chat.id, message_to_pin.message_id)
                return
            else:
                no_try = message.text.split()[1]
                if no_try.isdigit():
                    pin_time = int(message.text[5:])
                    if pin_time <= 0:
                        await message.reply("Пожалуйста, введите число больше чем 0!")
                        return
                    pin_time = int(pin_time * 60 * 60)
                    await bot.pin_chat_message(message.chat.id, message_to_pin.message_id)
                    await asyncio.sleep(pin_time)
                    await bot.unpin_chat_message(message.chat.id)
                else:
                    await message.reply("Пожалуйста правильно введите число")
                    return

        except Exception as e:
            await message.reply(f"Ошибка: {e}")
        else:
            await message.reply(f"Этой командой может пользоваться только администратор!")


def register_handlers_pin_command(dp: Dispatcher):
    dp.register_message_handler(cmd_pin, commands='pin')