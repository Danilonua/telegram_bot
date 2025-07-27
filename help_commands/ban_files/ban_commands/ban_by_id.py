import datetime
from aiogram import types
from main.creat_bot import bot
from sql.search import Search
from sql.update import Update
from help_commands.ban_files.ban_commands.ban_reason.ban_reason import cmd_ban_reason

global check_warns
global ban_time
search = Search(0, 0, None)
update = Update(0, 0, None)


async def cmd_ban_by_id(message: types.Message):

    # это функция бана по айди или собачке, которая вызывается в случае того что команда
    # /ban была использована без ответа на соообщение

    global check_warns
    global ban_time
    try:
        words = message.text.split()
        no_try = message.text.split()[1]

        # проверка на то, что первое слово после команды /ban была буквеная, или числом.

        if no_try.isdigit():

            # проверка на то, есть ли собачка в сообщение, и если есть запускаеться бан по собачке

            if "@" in message.text:

                # получаем айди пользователя через контакт с базой данных

                ckeck = words[1]
                ckeck = int(ckeck)
                until_date = datetime.datetime.now() + datetime.timedelta(days=ckeck)
                until_timestamp = int(until_date.timestamp())
                user_name = message.text.split()[2][1:]
                result = search.search_id(message.chat.id, user_name)

                # проверка на то, что база данных не нашла информацию о пользователе

                if result is None:
                    await message.reply("Айди пользователя не найден")
                else:

                    # обрезка информации о пользователе с базы данных

                    user_id = str(result)[1:][:10]

                    # проверка есть ли слово "Причина" в сообщении, и если есть забускается скрипт по бане пользователя
                    # по собачке с причиной

                    if "Причина" in message.text:

                        # баним пользователя и заносим об этом информацию в базу данных

                        await bot.kick_chat_member(message.chat.id, user_id, until_date=until_timestamp)
                        update.update_ban(message.chat.id, user_id, 1)

                        # получаем текст причины и отпроваляем сообщение о бане в чат

                        reason = await cmd_ban_reason(message, 4)
                        await message.reply(f"Пользователь был забаненный на {ckeck} дней.\nПричина: {reason}")
                        await bot.send_message(-1001870910942, f"Внимание!"
                                                               f" Пользователь "
                                                               f"[{message.from_user.username}]"
                                                               f"(tg://user?id={str(message.from_user.id)}) "
                                                               f"забанил [{user_name}]"
                                                               f"(tg://user?id={str(user_id)}) по причине {reason}.\n"
                                                               f"Вот подробная информация о сообщении:\n"
                                                               f"{message}", parse_mode="Markdown")
                    else:

                        # баним пользователя если нет причины, и заносим всю нужную информацию в базу данных

                        await bot.kick_chat_member(message.chat.id, user_id)
                        update.update_ban(message.chat.id, user_id, 1)
                        await message.reply(f"Пользователь был забаненный на {ckeck} дней.")
            else:

                # этот код будет активироватся если в сообщении нет собачки, но первое сообщение все еще число

                cut_ban = str(message.text[5:])
                check = message.text.split()[1]

                # получаем время бана

                if len(check) == 1:
                    ban_time = str(cut_ban[:1])
                if len(check) == 2:
                    ban_time = str(cut_ban[:2])
                else:
                    ban_time = str(cut_ban[:1])
                length_ban_time = len(ban_time)

                # получаем айди пользователя

                user_id = str(message.text[7 + length_ban_time:][:10])
                user_id = int(user_id)
                ban_time_int = int(ban_time)
                date = datetime.datetime.now() + datetime.timedelta(days=ban_time_int)
                until_date = int(date.timestamp())
                try:
                    chat_member = await bot.get_chat_member(message.chat.id, user_id)

                    # проверка есть ли польователь в чате

                    if chat_member.is_chat_member():

                        # проверка есть ли слово "Причина" в сообщении

                        if "Причина" in message.text:
                            reason = await cmd_ban_reason(message, 4)

                            # баним пользователя и заносим об этом информацию в базу данных

                            await bot.kick_chat_member(message.chat.id, user_id, until_date=until_date)
                            update.update_ban(message.chat.id, user_id, 1)

                            # получаем текст причины и отпроваляем сообщение о бане в чат

                            await message.reply(f"Пользователь был забаненный на {ban_time} дней.\nПричина: {reason}")
                            await bot.send_message(-1001870910942, f"Внимание!"
                                                                   f" Пользователь "
                                                                   f"[{message.from_user.username}]"
                                                                   f"(tg://user?id={str(message.from_user.id)}) "
                                                                   f"забанил [{chat_member.user.username}]"
                                                                   f"(tg://user?id={str(chat_member.user.id)}) по причине"
                                                                   f" {reason}.\n"
                                                                   f"Вот подробная информация о сообщении:\n"
                                                                   f"{message}", parse_mode="Markdown")

                            # онилируем варны

                            check_warns = check_warns = str(search.search_warns(message.chat.id, user_id))
                            if check_warns is None or check_warns == "0":
                                update.update_warns(0, message.chat.id, user_id)
                        else:

                            # баним пользователя если нет причины, и заносим всю нужную информацию в базу данных

                            await bot.kick_chat_member(message.chat.id, user_id, until_date=until_date)
                            update.update_ban(message.chat.id, user_id, 1)
                            await message.reply(f"Пользователь был забаненный на {until_date} дней.")
                            check_warns = check_warns = str(search.search_warns(message.chat.id, user_id))

                            # онилируем варны

                            if check_warns is None or check_warns == "0":
                                update.update_warns(0, message.chat.id, user_id)
                    else:
                        # в случае того что пользователя нету в базе данных

                        await message.reply('Пользователь не находится в чате')
                except Exception as e:
                    # в случае неизвестной ошибки

                    await message.reply(f" {e}")
                    return

        else:

            # код будет активироватся если первое слово после команды /ban была буквеная

            # получаем время бана
            cut_ban = str(message.text[5:])

            # проверка на то ли есть собачка в сообщении
            if "@" in cut_ban:

                # ищем айди пользователя в базе данных

                user_name = message.text.split()[1][1:]
                result = search.search_id(message.chat.id, user_name)

                # проверка на то, что база данных не нашла информации

                if result is None:
                    await message.reply("Айди пользователя не найден")
                else:

                    # обрезаем информацию с базы данных

                    user_id = str(result)[1:][:10]

                    # проверка есть ли слово "Причина" в сообщении

                    if "Причина" in message.text:

                        # баним пользователя и заносим всю нужную информацию в базу данных

                        await bot.kick_chat_member(message.chat.id, user_id)
                        update.update_ban(message.chat.id, user_id, 1)

                        # получаем текст причины и отпроваляем сообщение о бане в чат

                        reason = await cmd_ban_reason(message, 3)
                        await message.reply(f"Пользователь был забаненный.\nПричина: {reason}")
                        await bot.send_message(-1001870910942, f"Внимание!"
                                                               f" Пользователь "
                                                               f"[{message.from_user.username}]"
                                                               f"(tg://user?id={str(message.from_user.id)}) "
                                                               f"забанил [{user_name}]"
                                                               f"(tg://user?id={str(user_id)}) по причине {reason}.\n"
                                                               f"Вот подробная информация о сообщении:\n"
                                                               f"{message}", parse_mode="Markdown")
                    else:

                        # баним пользователя если нет причины, и заносим всю нужную информацию в базу данных

                        await bot.kick_chat_member(message.chat.id, user_id)
                        update.update_ban(message.chat.id, user_id, 1)
                        await message.reply(f"Пользователь был забаненный.")
            else:

                # код будет активироватся если первое слово буквеное, и в сообщении нету собачки

                # получаем айди пользователя

                value_error_true = str([message.text[6:][:10]])
                value_error_true_convert = eval(value_error_true)
                user_id = int(value_error_true_convert[0])

                # проверк на то, есть ли пользователь в чате

                chat_member = await bot.get_chat_member(message.chat.id, user_id)
                if chat_member.is_chat_member():

                    # проверка есть ли слово "Причина" в сообщении

                    if "Причина" in message.text:
                        reason = await cmd_ban_reason(message, 3)

                        # баним пользователя и заносим об этом информацию в базу данных

                        await bot.kick_chat_member(message.chat.id, user_id)
                        update.update_ban(message.chat.id, user_id, 1)

                        # получаем текст причины и отпроваляем сообщение о бане в чат

                        await message.reply(f"Пользователь был забаненный.\nПричина: {reason}")
                        await bot.send_message(-1001870910942, f"Внимание!"
                                                               f" Пользователь "
                                                               f"[{message.from_user.username}]"
                                                               f"(tg://user?id={str(message.from_user.id)}) "
                                                               f"забанил [{chat_member.user.username}]"
                                                               f"(tg://user?id={str(chat_member.user.id)}) по причине"
                                                               f" {reason}.\n"
                                                               f"Вот подробная информация о сообщении:\n"
                                                               f"{message}", parse_mode="Markdown")
                    else:

                        # баним пользователя если нет причины, и заносим всю нужную информацию в базу данных

                        await bot.kick_chat_member(message.chat.id, user_id)
                        update.update_ban(message.chat.id, user_id, 1)
                        await message.reply(f"Пользователь был забаненный.")
                else:
                    # если пользователя нету в чате

                    await message.reply("Убедитесь что правильно написали айди или не забыли время бана.")
        return
    except Exception as e:
        await message.reply(f"{e}")
