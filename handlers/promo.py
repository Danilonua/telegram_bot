from aiogram import types, Dispatcher
from sql.update import Update
from sql.search import Search
from help_commands.ban_files.ban_commands.ban_reason.ban_reason import cmd_ban_reason


update = Update(0, 0, None)
search = Search(0, 0, None)


async def promo(message: types.Message):
    try:
        promokod = await cmd_ban_reason(message, 1)
        check = str(search.search_promo(message.from_user.id))
        if "ПеРвЫй запуск" in promokod:
            if "1" in str(check):
                await message.reply("Вы уже использовали промокод")
            else:
                update.update_promo(1, message.chat.id, message.from_user.id)
                update.update_pydollar('10', message.from_user.id, 1988813101)
                await message.reply('Вам было выдано 10 pydollars')
        else:
            await message.reply('Неправильный промокод')
    except Exception as e:
        await message.reply(f"{e}")


def register_handlers_level(dp: Dispatcher):
    dp.register_message_handler(promo, commands="promo")