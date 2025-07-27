from aiogram import types
from sql.search import Search
from sql.update import Update
from main.creat_bot import bot
from help_commands.ban_files.ban_commands.ban_reason.ban_reason import cmd_ban_reason


update = Update(0, 0, None)


async def cmd_mute_forever(message: types.Message):
    """
    Mute user
    """
    search = Search(0, 0, None)
    result = search.search_level(message.chat.id, message.from_user.id)
    result = str(result)[1:][:1]
    if result == "4" or result == "3":
        user_id = message.reply_to_message.from_user.id
        chat_member = await bot.get_chat_member(message.chat.id, user_id)
        if chat_member.is_chat_member():
            if "Причина" in message.text:
                reason = await cmd_ban_reason(message, 2)
                await bot.restrict_chat_member(message.chat.id, user_id, until_date=None)
                await bot.restrict_chat_member(message.chat.id, user_id, until_date=float("inf"))
                await message.reply(f"Пользователь был замучен на всегда!\nПричина: {reason}")
                update.update_mute(message.chat.id, user_id, 1)
            else:
                await bot.restrict_chat_member(message.chat.id, user_id, until_date=None)
                await bot.restrict_chat_member(message.chat.id, user_id, until_date=float("inf"))
                await message.reply("Пользователь был замучен на всегда!")
                update.update_mute(message.chat.id, user_id, 1)
        else:
            await message.reply('Пользователь не находится в чате')
    else:
        await message.reply(f"Этой командой может пользоваться только администратор!")
