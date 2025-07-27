from aiogram import types
import datetime
from main.creat_bot import bot
from sql.update import Update
from help_commands.mute_files.mute_forever import cmd_mute_forever
from help_commands.ban_files.ban_commands.ban_reason.ban_reason import cmd_ban_reason


update = Update(0, 0, None)


async def cmd_mute_reply(message: types.Message):
    user_id = message.reply_to_message.from_user.id
    words = message.text.split()
    if len(words) > 1:
        no_try = message.text.split()[1]
        if no_try.isdigit():
            if "Причина" in message.text:
                mute_duration = int(words[1])
                if mute_duration <= 0:
                    await message.reply("Пожалуйста, введите число больше чем 0")
                    return
                until_date = datetime.datetime.now() + datetime.timedelta(hours=mute_duration)
                until_timestamp = int(until_date.timestamp())
                chat_member = await bot.get_chat_member(message.chat.id, user_id)
                if chat_member.is_chat_member():
                    reason = await cmd_ban_reason(message, 3)
                    await bot.restrict_chat_member(message.chat.id, user_id, until_date=until_timestamp)
                    await message.reply(f"Пользователь был замучен на {mute_duration} часов.\nПричина: {reason}")
                    update.update_mute(message.chat.id, user_id, 1)
                else:
                    await message.reply('Пользователь не находится в чате')
            else:
                mute_duration = int(message.text[6:])
                if mute_duration <= 0:
                    await message.reply("Пожалуйста, введите число больше чем 0")
                    return
                until_date = datetime.datetime.now() + datetime.timedelta(hours=mute_duration)
                until_timestamp = int(until_date.timestamp())
                chat_member = await bot.get_chat_member(message.chat.id, user_id)
                if chat_member.is_chat_member():
                    await bot.restrict_chat_member(message.chat.id, user_id, until_date=until_timestamp)
                    await message.reply(f"Пользователь был замучен на {mute_duration} часов.")
                    update.update_mute(message.chat.id, user_id, 1)
                else:
                    await message.reply('Пользователь не находится в чате')
        else:
            await cmd_mute_forever(message)
            return
    else:
        await cmd_mute_forever(message)
