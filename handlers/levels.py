from aiogram import types, Dispatcher
from main.creat_bot import bot
from sql.update import Update


# level_0 обычный пользователь
# level_1 все команды, кроме бан, варн, мут
# level_2 все команды, кроме бан и мут
# level_3 все команды, кроме бан
# level_4 все команды


async def set_level(msg: types.Message):
    try:
        update = Update(0, 0, None)
        owner = await bot.get_chat_administrators(msg.chat.id)
        u = f"{owner}"
        chat_member_owner = (u[u.find('ChatMemberOwner') + 32:])[:10]
        if str(msg.from_user.id) == str(chat_member_owner):
            update.update_level(4, msg.chat.id, msg.from_user.id)
            try:
                user_id = msg.reply_to_message.from_user.id
                user_name = msg.reply_to_message.from_user.username
            except AttributeError:
                await msg.reply("Эта команда должна быть ответом на сообщение!")
                return
            try:
                level = int(msg.text[7:])
            except ValueError:
                await msg.reply("Пожалуйста, введите целое число!")
                return
            if level < 0:
                await msg.reply("Пожалуйста, введите число 0 или больше")
                return
            elif level > 4:
                await msg.reply("Пожалуйста, введите число меньше чем 5")
                return
            else:
                update.update_level(level, msg.chat.id, user_id)
                await msg.reply(f"Пользователь [{user_name}](tg://user?id={str(user_id)}) получил {level} уровень.",
                                parse_mode="Markdown")
                return
        else:
            await msg.reply(f"Этой командой может пользоваться только создатель!")
    except Exception as e:
        await msg.reply(f"{e}")


def register_handlers_level(dp: Dispatcher):
    dp.register_message_handler(set_level, commands="level")
