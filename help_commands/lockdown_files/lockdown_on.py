from sql.search import Search
from main.creat_bot import bot
from aiogram import types
from sql.update import Update


async def turn_on_lockdown(msg: types.Message):
    search = Search(0, 0, None)
    update = Update(0, 0, None)
    result = search.search_level(msg.chat.id, msg.from_user.id)
    result = str(result)[1:][:1]
    if result == "4":
        update.update_lockdown(1, msg.chat.id)
        send_message = await msg.reply("Режим локдауна включен, никто не может отправлять сообщения кроме "
                                       "администраторов")
        await bot.pin_chat_message(msg.chat.id, send_message.message_id)
        return send_message
    else:
        await msg.reply(
            "У вас недостаточно прав для выполнения этой команды! \n Только создатель может использовать эту команду!")
