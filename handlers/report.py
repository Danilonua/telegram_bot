from sql.search import Search
from main.creat_bot import bot
from aiogram import types, Dispatcher

id_photo = ""


async def report(msg: types.Message):
    global id_photo
    try:
        search = Search(0, 0, None)
        result = search.search_level(msg.chat.id, msg.from_user.id)
        result = str(result)[1:][:1]
        if result == "4" or result == "3" or result == "2":
            if msg.reply_to_message:
                if len(msg.text) == 7:
                    await msg.reply('Вы должны указать причину жалобы')
                else:
                    report_message = msg.text[8:]
                    if msg.reply_to_message.text:
                        answer_message = msg.reply_to_message.text
                        await msg.reply('Ваша жалоба успешно отправлена!')
                        await bot.send_message(-1001870910942, f"Внимание! Пользователь "
                                                               f"[{msg.from_user.username}]"
                                                               f"(tg://user?id={str(msg.from_user.id)})"
                                                               f" сделал репорт"
                                                               f"! Текст репорта:\n{report_message}\n"
                                                               f"Сообщение на которое был зделан репорт:\n"
                                                               f"{answer_message}\n"
                                                               f"Вот подробная информация:\n{msg}", parse_mode='Markdown')
                    else:
                        id_photo = msg.reply_to_message.photo[-1].file_id
                        await msg.reply('Ваша жалоба успешно отправлена!')
                        await bot.send_message(-1001870910942, f"Внимание! Пользователь "
                                                               f"[{msg.from_user.username}]"
                                                               f"(tg://user?id={str(msg.from_user.id)})"
                                                               f" сделал репорт"
                                                               f"! Текст репорта:\n{report_message}\n"
                                                               f"Фото на которое был зделан репорт будет снизу\n"
                                                               f"Вот подробная информация:\n{msg}", parse_mode='Markdown')
                        await bot.send_photo(-1001870910942, id_photo)
            else:
                if len(msg.text) == 7:
                    await msg.reply('Вы должны указать причину жалобы')
                else:
                    report_message = msg.text[8:]
                    await msg.reply('Ваша жалоба успешно отправлена!')
                    await bot.send_message(-1001870910942, f"Внимание! Пользователь "
                                                           f"[{msg.from_user.username}]"
                                                           f"(tg://user?id={str(msg.from_user.id)})"
                                                           f" сделал репорт"
                                                           f"! Текст репорта:\n{report_message}\n"
                                                           f"Вот подробная информация:\n{msg}", parse_mode='Markdown')
    except Exception as e:
        await msg.reply(f"{e}")

def register_handlers_report(dp: Dispatcher):
    dp.register_message_handler(report, commands="report")
