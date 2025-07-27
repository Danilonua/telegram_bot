from aiogram import types
from sql.search import Search
from main.creat_bot import bot
from sql.update import Update
from help_commands.ban_files.ban_commands.ban_reason.ban_reason import cmd_ban_reason


async def cmd_ban(message: types.Message):
    # функция будет использована в случае бана навсегда, в ответ на сообщение

    search = Search(0, 0, None)
    update = Update(0, 0, None)

    # получаем айди пользователя а заодно и на всякий случай проверяем что это точно ответ на сообщение

    try:
        user_id = message.reply_to_message.from_user.id
    except AttributeError:
        await message.reply("Эта команда должна быть ответом на сообщение!")
        return

    # проверка есть ли слово "Причина" в сообщении

    if "Причина" in message.text:
        reason = await cmd_ban_reason(message, 2)

        # баним пользователя и заносим об этом информацию в базу данных

        await bot.kick_chat_member(message.chat.id, user_id)
        update.update_ban(message.chat.id, user_id, 1)

        # получаем текст причины и отпроваляем сообщение о бане в чат

        await message.reply(f"Пользователь был забаненный.\nПричина: {reason}")

        # отсылаем сообщение в контрольную группу о бане

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

        await bot.kick_chat_member(message.chat.id, user_id)
        update.update_ban(message.chat.id, user_id, 1)
        await message.reply(f"Пользователь был забаненный.")