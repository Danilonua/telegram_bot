from main.creat_bot import bot
from aiogram import types, Dispatcher

from sql.update import Update
from sql.search import Search

search = Search(0, 0, None)
async def local_spammer(message: types.Message):
    try:
        info_for_true = message.text[15:][:4]
        info_for_false = message.text[15:][:5]
        user_id_for_true = message.text[21:][:10]
        user_id_for_false = message.text[22:][:10]
        chat_id_for_true = message.text[32:]
        chat_id_for_false = message.text[33:]
        if str(info_for_true) == "True":
            update = Update(int(user_id_for_true), int(chat_id_for_true), None)
            update.update_local_spammer(1, chat_id_for_true, user_id_for_true)
            await bot.send_message(message.chat.id, "Локальный спамер добавлен в систему!")
        elif str(info_for_false) == "False":
            update = Update(int(user_id_for_false), int(chat_id_for_false), None)
            update.update_local_spammer(0, chat_id_for_false, user_id_for_false)
            await bot.send_message(message.chat.id, "Локальный спамер удален из системы!")
        else:
            await bot.send_message(message.chat.id, "Пожалуйста, введите правильные данные!")
    except Exception as e:
        await message.reply(f"{e}")


async def global_spammer(message: types.Message):
    try:
        info_for_true = message.text[16:][:4]
        info_for_false = message.text[16:][:5]
        user_id_for_true = message.text[22:][:10]
        user_id_for_false = message.text[23:][:10]
        chat_id_for_true = message.text[33:]
        chat_id_for_false = message.text[34:]
        if str(info_for_true) == "True":
            update = Update(int(user_id_for_true), int(chat_id_for_true), None)
            update.update_global_spammer(1, chat_id_for_true, user_id_for_true)
            await bot.send_message(message.chat.id, "Глобальный спамер добавлен в систему!")
        elif str(info_for_false) == "False":
            update = Update(int(user_id_for_false), int(chat_id_for_false), None)
            update.update_global_spammer(0, chat_id_for_false, user_id_for_false)
            await bot.send_message(message.chat.id, "Глобальный спамер удален из системы!")
        else:
            await bot.send_message(message.chat.id, "Пожалуйста, введите правильные данные!")
    except Exception as e:
        await message.reply(f"{e}")



def register_handlers_spammer(dp: Dispatcher):
    dp.register_message_handler(local_spammer, commands="local_spammer")
    dp.register_message_handler(global_spammer, commands="global_spammer")