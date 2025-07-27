from help_commands.lockdown_files.lockdown_on import turn_on_lockdown
from help_commands.lockdown_files.lockdown_off import turn_off_lockdown
from sql.update import Update
from sql.search import Search
from sql.back_up_of_bd import BD
from main.creat_bot import bot
from aiogram import types, Dispatcher


bad_words = {'бля', 'сука', 'хуй', 'долбоеб', 'ебать', "блять", "ебал", "шлюха", "пидорас", "пизда", "пиздец",
             "ебля", "пиздабол", "хуя", "ебан"}
send_message = ''

global creator_username
global creator_id

update = Update(0, 0, None)
search = Search(0, 0, None)
bd = BD(0, 0, None)


async def check_join(msg: types.Message):
    update.update_username(msg.chat.id, msg.from_user.id, msg.from_user.username)  # добовляем юзера в базу данных
    update.update_ban(msg.chat.id, msg.from_user.id, 0)
    check_spam = search.search_spam(msg.chat.id)
    if "1" in str(check_spam):
        check_global_spammer = str(search.search_global_spammer(msg.from_user.id))[2:][:1]
        if "1" in str(check_global_spammer):
            await bot.ban_chat_member(msg.chat.id, msg.from_user.id)


async def check_sticker(msg: types.Message):
    checking_sticker = search.search_check_sticker(msg.chat.id)
    if "1" in str(checking_sticker):
        await msg.delete()


async def message_is_spam(msg: types.Message):

    # Функция для удаления сообщения со спамом.

    await msg.delete()
    await bot.send_message(-1001870910942, f"Внимание! Кто-то написал спам в чате"
                                           f", но благодаря системе анти-спам сообщение "
                                           f"было успешно удаленно! "
                                           f"Вот подробная информация {msg}")


async def sticker_on(message: types.Message):
    update.update_check_sticker(1, message.chat.id)
    await message.reply("Фильтр стикеров включен. Все стикеры будут удаляться!")


async def sticker_off(message: types.Message):
    update.update_check_sticker(0, message.chat.id)
    await message.reply("Фильтр стикеров выключен. Все стикеры будут храниться здесь!")


async def lockdown_on(message: types.Message):

    # Функция, которая вызывает другую функцию. Она включает лок даун и возвращает id закрепленного сообщения.

    global send_message
    send_message = await turn_on_lockdown(message)
    return send_message


async def lockdown_off(message: types.Message):

    # Функция, которая вызывает другую функцию. Она принимает id закрепленного сообщения и выключает лок даун.

    global send_message
    await turn_off_lockdown(message, send_message)


async def cmd_filter_message(msg: types.Message):

    # В этой функции хранятся все фильтры и команды, которые программа находит их сама в тексте. Здесь есть:
    # фильтр спама, фильтр мата, фильтр лок дауна, команды кто админ, снять админов, бан лист.

    global creator_username
    global creator_id

    try:
        update.update_ban(msg.chat.id, msg.from_user.id, 0)
        update.update_username(msg.chat.id, msg.from_user.id, msg.from_user.username)
        check_local_spammer = str(search.search_local_spammer(msg.chat.id, msg.from_user.id))[2:][:1]
        check_global_spammer = str(search.search_global_spammer(msg.from_user.id))[2:][:1]
        check_spam = search.search_spam(msg.chat.id)
        lower_text = msg.text.lower()
        space_text = lower_text.replace(' ', '')
        dot_text = space_text.replace('.', '')
        question_text = dot_text.replace('?', '')
        text = question_text.replace(',', '')
        text_for_spam = question_text.replace(',', '')
        length = len(text_for_spam)
        words = msg.text.split()
        result = " ".join(words[:1])
        seen = ""

        # Проверка на спам. Программа проверяет сообщение: это спам или нет? Если да, тогда сообщение удаляется и
        # подробности про сообщение присылается в специальный чат. В этом чату есть создатели бота, которые следят
        # за всеми сообщениями. Если программа пожаловалась на человека больше чем 3-4 раза, тогда человек становиться
        #  локальным или глобальным спамером (это создатели делают вручную).

        if "1" in str(check_spam):
            for word in words:
                if len(word) > 25:
                    await message_is_spam(msg)
                    return
            if length > 500:
                if result == msg.text:
                    await message_is_spam(msg)
                    return
                all_words_equal = all(word == words[0] for word in words)
                if all_words_equal or (len(words) > 25 and len(set(words)) < 3):
                    await message_is_spam(msg)
                    return
            for c in text_for_spam:
                if c not in seen:
                    q = int(text_for_spam.count(c) / len(text_for_spam) * 100)
                    if text_for_spam.count(c) > 10 and int(q) > 30:
                        await message_is_spam(msg)
                        return
                seen += c

            # Проверка на спамера. Когда человек что-то пишет в чат, тогда программа проверяет: он спамер или нет?
            # Если да, тогда программа удаляет сообщение.

            if "1" in str(check_local_spammer):
                await msg.reply("Обнаружен локальный спамер!")
                await bot.ban_chat_member(msg.chat.id, msg.from_user.id)

            if "1" in str(check_global_spammer):
                await msg.reply("Обнаружен глобальный спамер!")
                await bot.ban_chat_member(msg.chat.id, msg.from_user.id)

        # Проверка на мат. Если в сообщении есть мат тогда сообщение удаляется и подробности про сообщение
        # присылается в специальный чат.

        check_mats = str(search.search_mats(msg.chat.id))
        if "1" in check_mats:
            for word in bad_words:
                if word in text:
                    await bot.send_message(-1001870910942, f"Внимание! Кто-то написал предложение с матом в чате"
                                                           f", но благодаря системе анти-мат сообщение "
                                                           f"было успешно удаленно! "
                                                           f"Вот подробная информация {msg}")
                    await msg.delete()

            # Кто админ? Когда в чате кто-то спросит: кто админ? Тогда программа сама подскажет у кого есть level и
            # кто создатель чата.

        if text == "ктоадмин":
            list_id = bd.all_admins_id(msg.chat.id)
            all_admins_str = str(bd.all_admins(msg.chat.id))
            all_admins = eval(all_admins_str)
            result = ""
            chat_administrators = await bot.get_chat_administrators(msg.chat.id)
            for chat_member in chat_administrators:
                if chat_member.status == "creator":
                    creator_id = chat_member.user.id
                    creator_username = chat_member.user.username
            for (admin, Id) in zip(all_admins, list_id):
                result += f"[{admin[0]}](tg://user?id={str(Id[0])}): {admin[1]}\n"
            if result == "":
                await bot.send_message(msg.chat.id, f"Нету администраторов в чате")
            else:
                await bot.send_message(msg.chat.id, f"Администраторы: \n"
                                                    f"{result}Создатель группы: \n"
                                                    f"[{creator_username}](tg://user?id={str(creator_id)})",
                                       parse_mode="Markdown")

        # Снять админов. Если создатель чата напишет снять админов, тогда у всех админов level станет 0.

        if text == "снятьадминов":
            creator = await bot.get_chat_member(msg.chat.id, msg.from_user.id)
            if creator.is_chat_creator():
                update.update_all_admins(msg.chat.id, 0)
                await msg.reply('Снятие администраторов в чате прошло успешно')
            else:
                await msg.reply('Єта команда доступна только создателю')

        # Лок даун. Если лок даун включен, тогда все сообщения будут удаляться(если пользователь не админ).

        lockdown_check = str(search.search_lockdown(msg.chat.id))
        if "1" in lockdown_check:
            creator = await bot.get_chat_member(msg.chat.id, msg.from_user.id)
            if creator.is_chat_creator() or creator.is_chat_admin():
                pass
            else:
                if msg.from_user.id != msg.chat.id:
                    await msg.delete()

        # Бан лист. Когда в чате кто-то напишет: бан лист. Тогда программа сама подскажет, кто забаненный.

        if "банлист" in text:
            ban_result = search.search_banned_person(msg.chat.id)
            ban_list = str(ban_result)
            if "None" not in ban_list:
                ban_list = eval(ban_list)
                result = ''
                x = 0
                for ban in zip(ban_list):
                    if x == 0:
                        result += f"[{ban[0]}]"
                        x += 1
                    elif x == 1:
                        result += f'(tg://user?id={str(ban[0])})\n'
                        x = 0
                await msg.reply(f"Список банлистов: \n{result}", parse_mode="Markdown")
            else:
                await msg.reply(f"Нет забаненных пользователей или данных о них!")

        # Мут лист. Когда в чате кто-то напишет: мут лист. Тогда программа сама подскажет, кто замучен.

        if "мутлист" in text:
            mute_result = search.search_muted_person(msg.chat.id)
            mute_list = str(mute_result)
            if "None" not in mute_list:
                mute_list = eval(mute_list)
                result = ''
                x = 0
                for mute in zip(mute_list):
                    if x == 0:
                        result += f"[{mute[0]}]"
                        x += 1
                    elif x == 1:
                        result += f'(tg://user?id={str(mute[0])})\n'
                        x = 0
                await msg.reply(f"Список мутлистов: \n{result}", parse_mode="Markdown")
            else:
                await msg.reply(f"Нет замученых пользователей или данных о них!")

        # Варн лист. Когда в чате кто-то напишет: варн лист. Тогда программа сама подскажет у кого и сколько варнов.

        if "варнлист" in text:
            warn_result = search.search_warned_person(msg.chat.id)
            warn_list = str(warn_result)
            if "None" not in warn_list:
                warn_list = eval(warn_list)
                result = ''
                x = 0
                for warn in zip(warn_list):
                    if x == 0:
                        result += f"[{warn[0]}]"
                        x += 1
                    elif x == 1:
                        result += f'(tg://user?id={str(warn[0])}) :'
                        x += 1
                    elif x == 2:
                        result += f'{warn[0]}\n'
                await msg.reply(f"Список пользователей с варнами: \n{result}", parse_mode="Markdown")
            else:
                await msg.reply(f"Нет пользователей с варнами или данных о них!")

        # Анбан всех. Когда в чате кто-то напишет: анбан_всех и имеет 4 левел, все пользователи будут разбанены.

        if 'анбан_всех' in text:
            all_ban = search.unban_all(msg.chat.id)
            if all_ban:
                if 'None' not in all_ban:
                    for unban in all_ban:
                        await bot.unban_chat_member(msg.chat.id, unban)
                        update.update_ban(msg.chat.id, unban, 0)
                    await msg.reply(f"Все пользователи в чате были разбанены")
                else:
                    await msg.reply(f"Нет забаненых пользователей в чате или данных о них")
            else:
                await msg.reply(f"Нет забаненых пользователей в чате или данных о них")

        # Анмут всех. Когда в чате кто-то напишет: анмут_всех и имеет 4 левел, все пользователи будут размучены.

        if 'анмут_всех' in text:
            all_mute = search.unmute_all(msg.chat.id)
            if all_mute:
                if 'None' not in all_mute:
                    for unmute in all_mute:
                        await bot.restrict_chat_member(msg.chat.id, str(unmute), can_send_messages=True)
                        update.update_mute(msg.chat.id, unmute, 0)
                    await msg.reply(f"Все пользователи в чате были размучены")
                else:
                    await msg.reply(f"Нет замученых пользователей в чате или данных о них")
            else:
                await msg.reply(f"Нет замученых пользователей в чате или данных о них")
    except Exception as e:
        await msg.reply(f"{e}")


def register_handlers_filter_file(dp: Dispatcher):
    dp.register_message_handler(sticker_on, commands="sticker", commands_prefix='-')
    dp.register_message_handler(sticker_off, commands="sticker", commands_prefix='+')
    dp.register_message_handler(lockdown_on, commands="lockdown_on")
    dp.register_message_handler(lockdown_off, commands="lockdown_off")
    dp.register_message_handler(check_join, content_types=types.ContentType.NEW_CHAT_MEMBERS)
    dp.register_message_handler(check_sticker, content_types=types.ContentType.STICKER)
    dp.register_message_handler(cmd_filter_message)
