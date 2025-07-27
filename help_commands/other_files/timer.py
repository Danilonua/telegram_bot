import asyncio
from aiogram import types, Dispatcher


async def timer_handler(message: types.Message):
    name = message.from_user.username
    if name is None:
        name = message.from_user.first_name
    try:
        time_s = int(message.text.split()[1])
        if time_s < 0:
            await message.answer(f"Неправильное время")
        else:
            time_format = str(message.text.split()[2])
            if "min" in time_format:
                time = time_s * 60
                await message.reply(f"Вы установили таймер на {time_s} {time_format}.")
                await asyncio.sleep(time)

                await message.answer(f"[{name}](tg://user?id={str(message.from_user.id)}) "
                                     f" Ваш таймер вышел", parse_mode="Markdown")
            if 'hour' in time_format:
                time = time_s * 3600
                await message.reply(f"Вы установили таймер на {time_s} {time_format}.")
                await asyncio.sleep(time)

                await message.answer(f"[{name}](tg://user?id={str(message.from_user.id)}) "
                                     f" Ваш таймер вышел", parse_mode="Markdown")
            if 'day' in time_format:
                time = time_s * 86400
                await message.reply(f"Вы установили таймер на {time_s} {time_format}.")
                await asyncio.sleep(time)
                await message.answer(f"[{name}](tg://user?id={str(message.from_user.id)}) "
                                     f" Ваш таймер вышел", parse_mode="Markdown")
            if 'sec' in time_format:
                time = time_s
                await message.reply(f"Вы установили таймер на {time_s} {time_format}.")
                await asyncio.sleep(time)
                await message.answer(f"[{name}](tg://user?id={str(message.from_user.id)}) "
                                     f" Ваш таймер вышел", parse_mode="Markdown")
            else:
                await message.reply('Неправильный формат времени')
    except IndexError:
        await message.reply("Вы должны указать время")
        return
    except ValueError:
        await message.reply("Неправильный формат")
        return


def register_handlers_timer_command(dp: Dispatcher):
    dp.register_message_handler(timer_handler, commands='timer')

