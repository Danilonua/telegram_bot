from aiogram import types, Dispatcher


# @dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    """
    Start the bot
    """
    group_type = message.chat.type
    if group_type == "supergroup":
        await message.reply("Привет, я бот модератор! Что бы увидеть мои команды напишите в чат /help.")
    elif group_type != "supergroup":
        await message.reply("Привет, я бот модератор! Перед использованиям моих команд, добавте меня в супер-группу, "
                            "и прочитайте <a href='https://teletype.in/@pythonhelper/NlOZOS5iAB5'>инструкцию</a>\n\n"
                            "Что я могу вам предложить?\n"
                            "1) 🚫 Удалять весь спам и маты в чате 🚫\n"
                            "2) 🔫 Идеально модерировать чат 🔫\n"
                            "3) 🎮 Много игровых команд 🎮 "
                            , parse_mode="HTML")


# @dp.message_handler(commands='help')
async def cmd_help(message: types.Message):
    """
    Show help message
    """
    await message.reply("Сейчас я покажу самые главные команды, но если хочешь увидеть больше команд и подробную"
                        " инструкцию до них перейдите, пожалуйста, за ссылкой ниже. Команды: \n\n /start - для "
                        "начала работы с ботом\n /help - для помощи\n /warn - для надавания предупреждений пользователю"
                        "\n /view_warns - для просмотра количества варнов пользователя\n /mute - для забирания прав "
                        "у человека, писать что то в чат\n /unmute - для размута\n /ban - для бана пользователя\n"
                        " /unban - для разбана пользователя. Вот ссылка на подробную инструкцию и дополнительные "
                        "команды:\nhttps://teletype.in/@pythonhelper/NlOZOS5iAB5 ")


def register_handlers_other_commands(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands='start')
    dp.register_message_handler(cmd_help, commands='help')