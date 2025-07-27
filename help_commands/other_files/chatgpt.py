import openai
from aiogram import Dispatcher, types
from main.creat_bot import bot
from help_commands.ban_files.ban_commands.ban_reason.ban_reason import cmd_ban_reason


openai.api_key = 'api_key'

openai.Model.list()


async def chat_gpt(message: types.Message):
    try:
        question = await cmd_ban_reason(message, 1)
        responce = openai.Completion.create(
            model='text-davinci-003',
            prompt=question,
            temperature=1,
            max_tokens=2048,
            top_p=0.7,
        )
        text = responce['choices'][0]['text']
        await message.reply(text)
    except Exception as e:
        await message.reply(f"{e}")


def register_handlers_gpt(dp: Dispatcher):
    dp.register_message_handler(chat_gpt, commands="gpt")
