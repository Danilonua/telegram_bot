from aiogram import types, Dispatcher
from main.creat_bot import bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
from sql.search import Search
from sql.update import Update

global id_second_fighter
global first_fighter_id
global second_fighter_name
global first_fighter_name
update = Update(0, 0, None)
global user_name
global count_of_pydollars
bet = 0


async def fight(msg: types.Message):
    global id_second_fighter
    global first_fighter_id
    global second_fighter_name
    global user_name
    global count_of_pydollars
    global bet
    search = Search(0, 0, None)
    first_fighter_id = msg.from_user.id
    if msg.reply_to_message:
        id_second_fighter = msg.reply_to_message.from_user.id
        count_of_pydollars = msg.text.split()[-1]
    else:
        if '@' in msg.text:
            user_name = msg.text.split()[1][1:]
            count_of_pydollars = msg.text.split()[-1]
            result = search.search_id(msg.chat.id, user_name)
            id_second_fighter = str(result)[1:][:10]
        else:
            id_second_fighter = msg.text[7:]
    if count_of_pydollars.isdigit():
        bet = count_of_pydollars
    else:
        pass
    second_fighter_name = await bot.get_chat_member(msg.chat.id, id_second_fighter)
    if second_fighter_name.is_chat_member():
        if second_fighter_name.user.id != first_fighter_id:
            keyboard = InlineKeyboardMarkup()
            accept_button = InlineKeyboardButton(text='Принять 🔫', callback_data='accept_callback')
            decline_button = InlineKeyboardButton(text='Отменить ❌', callback_data='decline_callback')
            keyboard.add(accept_button, decline_button)
            await bot.send_message(msg.chat.id, f"[{second_fighter_name.user.username}]"
                                                f"(tg://user?id={str(second_fighter_name.user.id)})"
                                                f" Внимание! "
                                                f"[{msg.from_user.username}](tg://user?id={str(msg.from_user.id)})"
                                                f" Вызвал вас на бой!\n"
                                                f"У каждого игрока по 1 патрону\n"
                                                f"Ставка: {bet} pydollar", parse_mode='Markdown',
                                                reply_markup=keyboard)
        else:
            await msg.reply('Вы не можете послать вызов на дуэль самому себе')
    else:
        await msg.reply('Пользователь не находиться в чате')


async def process_callback_button1(callback_query: types.CallbackQuery):
    global second_fighter_name
    second_fighter_name = await bot.get_chat_member(callback_query.message.chat.id, id_second_fighter)
    if int(id_second_fighter) != int(callback_query.from_user.id):
        await bot.answer_callback_query(callback_query.id, text="не тыкай куда попало", show_alert=True)
    else:
        await bot.send_message(callback_query.message.chat.id,
                               f"[{second_fighter_name.user.username}](tg://user?id={str(second_fighter_name.user.id)})"
                               f" Отклонил бой", parse_mode='Markdown')


async def process_callback_button2(callback_query: types.CallbackQuery):
    global second_fighter_name
    global first_fighter_name
    second_fighter_name = await bot.get_chat_member(callback_query.message.chat.id, id_second_fighter)
    first_fighter_name = await bot.get_chat_member(callback_query.message.chat.id, first_fighter_id)
    keyboard2 = InlineKeyboardMarkup()
    shot_button = InlineKeyboardButton(text='Выстрелить 🔫', callback_data='shot_callback')
    decline_shot_button = InlineKeyboardButton(text='Отменить выстрел ❌', callback_data='decline_shot_callback')
    keyboard2.add(shot_button, decline_shot_button)
    if int(id_second_fighter) != int(callback_query.from_user.id):
        await bot.answer_callback_query(callback_query.id, text="не тыкай куда попало", show_alert=True)
    else:
        await bot.send_message(callback_query.message.chat.id,
                               f"✅ [{second_fighter_name.user.username}](tg://user?id="
                               f"{str(second_fighter_name.user.id)})"
                               f" Принял бой и получает право стрелять первым", parse_mode='Markdown',
                               reply_markup=keyboard2)


async def process_callback_button3(callback_query: types.CallbackQuery):
    shot_aim = random.randint(1, 2)
    if int(id_second_fighter) != int(callback_query.from_user.id):
        await bot.answer_callback_query(callback_query.id, text="не тыкай куда попало", show_alert=True)
    else:
        if shot_aim == 1:
            if first_fighter_name.status == 'creator':
                await bot.send_message(callback_query.message.chat.id,
                                       f"[{second_fighter_name.user.username}]"
                                       f"(tg://user?id={str(second_fighter_name.user.id)}) "
                                       f" попал в "
                                       f"[{first_fighter_name.user.username}]"
                                       f"(tg://user?id={str(first_fighter_name.user.id)})"
                                       f" но он бессмертный потому что он создатель!", parse_mode='Markdown')
            else:
                update.update_pydollar(bet, first_fighter_id, second_fighter_name.user.id)
                await bot.send_message(callback_query.message.chat.id,
                                       f"[{second_fighter_name.user.username}](tg://user?id="
                                       f"{str(second_fighter_name.user.id)})"
                                       f" попал в "
                                       f"[{first_fighter_name.user.username}]"
                                       f"(tg://user?id={str(first_fighter_name.user.id)})",
                                       parse_mode='Markdown')
        else:
            keyboard3 = InlineKeyboardMarkup()
            shot_button_2 = InlineKeyboardButton(text='Выстрелить 🔫', callback_data='shot_callback_2')
            decline_shot_button_2 = InlineKeyboardButton(text='Отменить выстрел ❌',
                                                         callback_data='decline_shot_callback_2')
            keyboard3.add(shot_button_2, decline_shot_button_2)
            await bot.send_message(callback_query.message.chat.id,
                                   f"[{second_fighter_name.user.username}]"
                                   f"(tg://user?id={str(second_fighter_name.user.id)})"
                                   f" промазал, теперь очередь "
                                   f"[{first_fighter_name.user.username}]"
                                   f"(tg://user?id={str(first_fighter_name.user.id)})"
                                   f" стрелять",
                                   parse_mode='Markdown', reply_markup=keyboard3)


async def process_callback_button4(callback_query: types.CallbackQuery):
    shot_aim = random.randint(1, 2)
    if int(first_fighter_id) != int(callback_query.from_user.id):
        await bot.answer_callback_query(callback_query.id, text="не тыкай куда попало", show_alert=True)
    else:
        if shot_aim == 1:
            if second_fighter_name.status == 'creator':
                await bot.send_message(callback_query.message.chat.id,
                                       f"[{first_fighter_name.user.username}]"
                                       f"(tg://user?id={str(first_fighter_name.user.id)}) "
                                       f" попал в "
                                       f"[{second_fighter_name.user.username}]"
                                       f"(tg://user?id={str(second_fighter_name.user.id)})"
                                       f" но он бессмертный потому что он создатель группы!", parse_mode='Markdown')
            else:
                update.update_pydollar(bet, second_fighter_name.user.id, first_fighter_id)
                await bot.send_message(callback_query.message.chat.id,
                                       f"[{first_fighter_name.user.username}]"
                                       f"(tg://user?id={str(first_fighter_name.user.id)}) "
                                       f" попал в "
                                       f"[{second_fighter_name.user.username}]"
                                       f"(tg://user?id={str(second_fighter_name.user.id)})",
                                       parse_mode='Markdown')
        else:
            await bot.send_message(callback_query.message.chat.id, 'У обоих игроков закончились патроны, все выжили')


async def process_callback_button5(callback_query: types.CallbackQuery):
    keyboard3 = InlineKeyboardMarkup()
    shot_button_2 = InlineKeyboardButton(text='Выстрелить 🔫', callback_data='shot_callback_2')
    decline_shot_button_2 = InlineKeyboardButton(text='Отменить выстрел ❌', callback_data='decline_shot_callback_2')
    keyboard3.add(shot_button_2, decline_shot_button_2)
    if int(first_fighter_id) != int(callback_query.from_user.id):
        await bot.answer_callback_query(callback_query.id, text="не тыкай куда попало", show_alert=True)
    else:
        await bot.send_message(callback_query.message.chat.id,
                               f"[{second_fighter_name.user.username}]"
                               f"(tg://user?id={str(second_fighter_name.user.id)})"
                               f" отказался стрелять, теперь очередь "
                               f"[{first_fighter_name.user.username}]"
                               f"(tg://user?id={str(first_fighter_name.user.id)})"
                               f" стрелять",
                               parse_mode='Markdown', reply_markup=keyboard3)


async def process_callback_button6(callback_query: types.CallbackQuery):
    if int(first_fighter_id) != int(callback_query.from_user.id):
        await bot.answer_callback_query(callback_query.id, text="не тыкай куда попало", show_alert=True)
    else:
        await bot.send_message(callback_query.message.chat.id,
                               f"[{first_fighter_name.user.username}]"
                               f"(tg://user?id={str(second_fighter_name.user.id)})"
                               f" отказался стрелять, у обоих игроков закончились патроны!",
                               parse_mode='Markdown')


def register_handlers_fight(dp: Dispatcher):
    dp.register_message_handler(fight, commands="fight")
    dp.register_callback_query_handler(process_callback_button1, lambda c: c.data == 'decline_callback')
    dp.register_callback_query_handler(process_callback_button2, lambda c: c.data == 'accept_callback')
    dp.register_callback_query_handler(process_callback_button3, lambda c: c.data == 'shot_callback')
    dp.register_callback_query_handler(process_callback_button6, lambda c: c.data == 'decline_shot_callback_2')
    dp.register_callback_query_handler(process_callback_button5, lambda c: c.data == 'decline_shot_callback')
    dp.register_callback_query_handler(process_callback_button4, lambda c: c.data == 'shot_callback_2')
