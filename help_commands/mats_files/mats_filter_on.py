from aiogram import types, Dispatcher
from sql.search import Search
from sql.update import Update


async def turn_on_mats_filter(msg: types.Message):
    search = Search(0, 0, None)
    update = Update(0, 0, None)
    result = search.search_level(msg.chat.id, msg.from_user.id)
    result = str(result)[1:][:1]
    if result == "4" or result == "3" or result == "2" or result == "1":
        update.update_mats(1, msg.chat.id)
        await msg.reply("Фильтр матов включен. Все маты будут удаляться.")
        return
    else:
        await msg.reply(f"Этой командой может пользоваться только администратор!")
        return


def register_handlers_mats_on_filter(dp: Dispatcher):
    dp.register_message_handler(turn_on_mats_filter, commands="mats", commands_prefix='-')
