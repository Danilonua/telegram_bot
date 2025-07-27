from aiogram import types, Dispatcher


async def send_hit(message: types.Message):
    try:
        your_id = message.from_id
        your_name = message.from_user.username
        friend_name = message.reply_to_message.from_user.username
        friend_id = message.reply_to_message.from_user.id
        await message.answer(f'[{your_name}](tg://user?id={str(your_id)}) ударил/a [{friend_name}](tg:'
                             f'//user?id={str(friend_id)})', parse_mode="Markdown")
    except AttributeError:
        your_id = message.from_id
        your_name = message.from_user.username
        await message.answer(f'[{your_name}](tg://user?id={str(your_id)}) ударил/а всех! ',
                             parse_mode="Markdown")


def register_handlers_hit_command(dp: Dispatcher):
    dp.register_message_handler(send_hit, commands='hit')
