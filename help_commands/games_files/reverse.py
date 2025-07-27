from aiogram import types, Dispatcher
from help_commands.ban_files.ban_commands.ban_reason.ban_reason import cmd_ban_reason


async def reverse(message: types.Message):
    # Функция возвращает перевёрнутый текст

    text = await cmd_ban_reason(message, 1)
    await message.reply(str(text[::-1]))


def register_reverse_commands(dp: Dispatcher):
    dp.register_message_handler(reverse, commands='reverse')
