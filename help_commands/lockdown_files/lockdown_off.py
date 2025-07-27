from aiogram import types
from sql.update import Update
from sql.search import Search
from main.creat_bot import bot


async def turn_off_lockdown(msg: types.Message, send_message):
    search = Search(0, 0, None)
    update = Update(0, 0, None)
    result = search.search_level(msg.chat.id, msg.from_user.id)
    result = str(result)[1:][:1]
    if result == "4":
        lockdown_status = str(search.search_lockdown(msg.chat.id))
        if "1" in lockdown_status:
            update.update_lockdown(0, msg.chat.id)
            await msg.reply("Режим локдауна выключен!")
            await bot.unpin_chat_message(msg.chat.id, send_message.message_id)
        else:
            await msg.reply("Локдаун уже выключен")
    else:
        await msg.reply(
            "У вас недостаточно прав для выполнения этой команды! \n Только создатель может использовать эту команду!")