from aiogram import types, Dispatcher
from sql.search import Search


search = Search(0, 0, None)


async def top(message: types.Message):

    # Топ 10 самых богатых пользователей бота pythonsuperhelper. Пишет имя и количество.

    pydollars_top = search.search_max_pydollar()
    pydollars_order = 0
    pydollars_number = 1
    result = ''

    for top in pydollars_top:
        result += f'{pydollars_number}) [{top[0]}](tg://user?id={str(top[1])}) : {top[2]}\n'
        pydollars_number += 1

    pydollars_number = 1

    await message.reply(f'Топ 10 самых богатых пользователей бота pythonsuperhelper: \n{result}', parse_mode='Markdown')


def register_handlers_top_command(dp: Dispatcher):
    dp.register_message_handler(top, commands='top')
