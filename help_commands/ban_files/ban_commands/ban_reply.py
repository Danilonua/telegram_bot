import datetime
from aiogram import types
from main.creat_bot import bot
from help_commands.ban_files.ban_commands.cmd_ban import cmd_ban
from help_commands.ban_files.ban_commands.ban_reason.ban_reason import cmd_ban_reason
from sql.search import Search
from sql.update import Update

global check_warns
search = Search(0, 0, None)
update = Update(0, 0, None)


async def cmd_ban_reply(message: types.Message):
    #  функция будет активироватся в случае использования команды /ban с ответом на сообщение

    global check_warns

    #  получаем айди пользователя

    user_id = message.reply_to_message.from_user.id
    words = message.text.split()

    # проверка на количество слов в сообщении, что бы не было ошибки с обрезанием данных

    if len(words) > 1:
        ban_duration = message.text.split()[1]

        #  проверка на то, что первое слово число

        if ban_duration.isdigit():
            ban_duration = int(ban_duration)

            # Calculate ban end time
            until_date = datetime.datetime.now() + datetime.timedelta(days=ban_duration)
            until_timestamp = int(until_date.timestamp())

            # проверка есть ли слово "Причина" в сообщении

            if "Причина" in message.text:
                reason = await cmd_ban_reason(message, 3)

                # баним пользователя и заносим об этом информацию в базу данных

                await bot.kick_chat_member(message.chat.id, user_id, until_date=until_timestamp)
                update.update_ban(message.chat.id, user_id, 1)

                # получаем текст причины и отпроваляем сообщение о бане в чат

                await message.reply(f"Пользователь был забаненный на {ban_duration} дней.\nПричина: {reason}")
                check_warns = check_warns = str(search.search_warns(message.chat.id, user_id))

                # онилируем варны

                if check_warns is None or check_warns == "0":
                    update.update_warns(0, message.chat.id, user_id)

                # отсылаем сообщение о бане в нашу контрольную группу

                await bot.send_message(-1001870910942, f"Внимание!"
                                                       f" Пользователь "
                                                       f"[{message.from_user.username}]"
                                                       f"(tg://user?id={str(message.from_user.id)}) "
                                                       f"забанил [{message.reply_to_message.from_user.username}]"
                                                       f"(tg://user?id={str(user_id)}) по причине {reason}.\n"
                                                       f"Вот подробная информация о сообщении:\n"
                                                       f"{message}", parse_mode="Markdown")
            else:

                # баним пользователя если нет причины, и заносим всю нужную информацию в базу данных

                await bot.kick_chat_member(message.chat.id, user_id, until_date=until_timestamp)
                update.update_ban(message.chat.id, user_id, 1)
                await message.reply(f"Пользователь был забаненный на {ban_duration} дней.")

                # онилируем варны

                check_warns = check_warns = str(search.search_warns(message.chat.id, user_id))
                if check_warns is None or check_warns == "0":
                    update.update_warns(0, message.chat.id, user_id)
        else:

            # проверка есть ли слово "Причина" в сообщении

            if "Причина" in message.text:
                await cmd_ban(message)
            else:
                # если число не целое

                await message.reply("Пожалуйста, введите целое число!")
                return

        # проверка на то, что число минусовое
        if ban_duration <= 0:
            await message.reply("Пожалуйста, введите число больше чем 0!")
            return
    else:
        if message.text == "/ban":

            # код будет активироватся в случае использования команды /ban и все

            # выполняется команда бана навсегда в ответ

            await cmd_ban(message)

            # онилируем варны
            check_warns = check_warns = str(search.search_warns(message.chat.id, user_id))
            if check_warns is None or check_warns == "0":
                update.update_warns(0, message.chat.id, user_id)

