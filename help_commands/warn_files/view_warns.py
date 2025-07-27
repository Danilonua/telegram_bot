from aiogram import types, Dispatcher
from main.creat_bot import bot
from sql.search import Search
from sql.update import Update
from help_commands.ban_files.ban_commands.ban_reason.ban_reason import cmd_ban_reason


# @dp.message_handler(commands='view_warns')
async def view_warns(message: types.Message):
    """
    View warns of user
    """
    user_id = None
    search = Search(0, 0, None)
    update = Update(0, 0, None)
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        check_warns = str(search.search_warns(message.chat.id, user_id))
        if check_warns is None or check_warns == "0":
            update.update_warns(0, message.chat.id, user_id)
        await message.reply(f"Он/она сейчас имеет {check_warns} варна.")

    else:
        if "@" in message.text:
            cut_ban = await cmd_ban_reason(message, 1)
            user_name = cut_ban[1:]
            result = str(search.search_id(message.chat.id, user_name))
            user_id = "".join(filter(str.isdigit, result))
            chat_member = await bot.get_chat_member(message.chat.id, user_id)
            if chat_member.is_chat_member():
                check_warns = str(search.search_warns(message.chat.id, user_id))
                if check_warns is None or check_warns == "0":
                    update.update_warns(0, message.chat.id, user_id)
                await message.reply(f"Он/она сейчас имеет {check_warns} варна.")
            else:
                await message.reply("Убедитесь что правильно написали айди")
        else:
            try:
                value_error_true = str([message.text[13:][:10]])
                value_error_true_convert = eval(value_error_true)
                user_id = int(value_error_true_convert[0])
                chat_member = await bot.get_chat_member(message.chat.id, user_id)
            except ValueError:
                chat_member = None
                await message.reply('Убедитесь что написали все как в инструкции')
            if chat_member.is_chat_member():
                check_warns = str(search.search_warns(message.chat.id, user_id))
                if check_warns is None or check_warns == "0":
                    update.update_warns(0, message.chat.id, user_id)
                await message.reply(f"Он/она сейчас имеет {check_warns} варна.")
            else:
                await message.reply("Убедитесь что правильно написали айди")
            return


def register_handlers_view_warns(dp: Dispatcher):
    dp.register_message_handler(view_warns, commands='view_warns')