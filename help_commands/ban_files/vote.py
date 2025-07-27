from sql.search import Search
from sql.update import Update
from main.creat_bot import bot
from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

global vote_number
global user_id
global user_name

search = Search(0, 0, None)
update = Update(0, 0, None)

vote_kick = 0
vote_status = False
who_voted = " "


async def vote(message: types.Message):
    global vote_number
    global user_id
    global user_name
    global vote_status

    result = search.search_level(message.chat.id, message.from_user.id)
    result = str(result)[1:][:1]
    if result == "4":
        if message.reply_to_message:
            try:
                vote_number = int(message.text.split()[1])
            except ValueError:
                await message.reply('Пожалуйста введите число')
            user_id = message.reply_to_message.from_user.id
            user_name = message.reply_to_message.from_user.username
            keyboard = InlineKeyboardMarkup()
            accept_button = InlineKeyboardButton(text='Бан ❌', callback_data='accept_vote')
            decline_button = InlineKeyboardButton(text='Живи 👍', callback_data='decline_vote')
            stop_vote = InlineKeyboardButton(text='Oстоновить голосование🚫', callback_data='stop_vote')
            keyboard.add(accept_button, decline_button, stop_vote)
            await bot.send_message(message.chat.id, f'Голосование за бан'
                                                    f'[{user_name}](tg://user?id={str(user_id)})'
                                                    f'Началось.\n'
                                                    f'Состояние: до {vote_number} голосов.', reply_markup=keyboard,
                                                    parse_mode='Markdown')
            vote_status = True
        else:
            pass
    else:
        await message.reply("Только администратор с 4 уровнем может запустить голосование на кик")


async def vote_button(callback_query: types.CallbackQuery):
    global vote_kick
    global vote_number
    global who_voted
    global vote_status

    if vote_status:
        if f'{callback_query.from_user.id}' not in who_voted:
            who_voted += f'{callback_query.from_user.id}'
            vote_kick += 1
            await bot.answer_callback_query(callback_query.id, text="Вы успешно проголосовали", show_alert=True)
            if vote_kick == vote_number or vote_kick > vote_number:
                await bot.kick_chat_member(callback_query.message.chat.id, user_id)
                update.update_ban(callback_query.message.chat.id, user_id, 1)
                await bot.send_message(callback_query.message.chat.id,
                                       f'{vote_number} или больше людей прголосовали за бан'
                                       f' [{user_name}](tg://user?id={str(user_id)}) '
                                       f'и пользователь был забаненым', parse_mode='Markdown')

                who_voted = ''
        else:
            await bot.answer_callback_query(callback_query.id, text="Вы уже проголосовали", show_alert=True)
    else:
        await bot.answer_callback_query(callback_query.id, text="Голосование уже завершено", show_alert=True)


async def vote_stop(callback_query: types.CallbackQuery):
    global vote_status
    global who_voted

    result = search.search_level(callback_query.from_user.id, callback_query.message.chat.id)
    result = str(result)[1:][:1]
    if result == "4":
        who_voted = ''
        vote_status = False
        await bot.send_message(callback_query.message.chat.id, 'Голосование было отменено администратором')
    else:
        await bot.answer_callback_query(callback_query.id, text="Только администратор с 4 уровнем может запустить"
                                                                " голосование на кик", show_alert=True)


async def vote_decline(callback_query: types.CallbackQuery):
    global who_voted
    global vote_status

    if vote_status:
        who_voted += f'{callback_query.from_user.id}'
        await bot.answer_callback_query(callback_query.id, text="Вы успешно проголосовали", show_alert=True)
    else:
        await bot.answer_callback_query(callback_query.id, text="Голосование уже завершено", show_alert=True)


def register_handlers_report(dp: Dispatcher):
    dp.register_message_handler(vote, commands="vote")
    dp.register_callback_query_handler(vote_button, lambda c: c.data == 'accept_vote')
    dp.register_callback_query_handler(vote_stop, lambda c: c.data == 'stop_vote')
    dp.register_callback_query_handler(vote_decline, lambda c: c.data == 'decline_vote')
