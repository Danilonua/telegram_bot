from aiogram import types, Dispatcher
from main.creat_bot import bot
from sql.search import Search
from sql.update import Update

search = Search(0, 0, None)
update = Update(0, 0, None)


async def cmd_give(message: types.Message):

    # Эта функция передает pydollars от одного человека к другому.
    try:
        if message.reply_to_message:
            cut_give = message.text[6:]
            count_pydollar = search.search_pydollar(message.from_user.id)
            count_pydollar = str(count_pydollar)[1:][:len(str(count_pydollar)) - 3]

            # Проверки на 0, на пустоту, меньше чем имеется pydollars, проверка на выдачу pydollars боту,
            # на отрицательное число и на ответ на сообщение.

            if cut_give == "" or cut_give == "0":
                await bot.send_message(message.chat.id, "Введите пожалуйста правильные данные!")
            elif int(count_pydollar) < int(cut_give):
                await bot.send_message(message.chat.id, f"У вас не достаточно средств! Вы хотите перечислить {cut_give}"
                                                        f" pydollars, а на вашем счету {count_pydollar}.")
            else:
                if message.reply_to_message.from_user.is_bot:
                    await bot.send_message(message.chat.id, "Нельзя выдать pydollars для бота!")
                else:
                    result = update.update_pydollar(cut_give, message.reply_to_message.from_user.id, message.from_user.id)
                    if result == 1:
                        await bot.send_message(message.chat.id, "Введите пожалуйста правильные данные!")
                    if result == 2:
                        await bot.send_message(message.chat.id, "Нельзя ставить отрицательное число!")
                    else:
                        await bot.send_message(message.chat.id, f'Вы успешно перечислили свои pydollars для '
                                                                f'[{message.reply_to_message.from_user.username}]'
                                                                f'(tg://user?id='
                                                                f'{str(message.reply_to_message.from_user.id)})',
                                               parse_mode="Markdown")
        else:
            await bot.send_message(message.chat.id, "Эта команда должна быть ответом на сообщение!")
    except Exception as e:
        await message.reply(f"{e}")


async def cmd_pocket(message: types.Message):

    # Эта функция отправляет в чат твое количество pydollars, а если ты ее вызвал в ответ на сообщение,
    # тогда отправляется текст: "Нельзя заглядывать в чужой карман!".

    if message.reply_to_message:
        await bot.send_message(message.chat.id, "Нельзя заглядывать в чужой карман!")
    else:
        count_pydollar = search.search_pydollar(message.from_user.id)
        count_pydollar = str(count_pydollar)[1:][:len(str(count_pydollar)) - 3]
        await bot.send_message(message.chat.id, f'В вашем кармане {count_pydollar} pydollars')


def register_handlers_give_file(dp: Dispatcher):
    dp.register_message_handler(cmd_give, commands='give')
    dp.register_message_handler(cmd_pocket, commands='pocket')