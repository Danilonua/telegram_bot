import aiohttp
import json
from aiogram import types, Dispatcher
from help_commands.ban_files.ban_commands.ban_reason.ban_reason import cmd_ban_reason


async def shorten_url(message: types.Message):
    url = await cmd_ban_reason(message, 1)
    api_url = "https://api-ssl.bitly.com/v4/shorten"
    headers = {
        "Authorization": f"Bearer bb79a14f117623676dd11199eace9d746c4de5c4",
        "Content-Type": "application/json",
    }
    payload = {"long_url": url}
    async with aiohttp.ClientSession() as session:
        async with session.post(api_url, headers=headers, data=json.dumps(payload)) as response:
            if response.status == 200:
                data = await response.json()
                await message.reply(data["link"])
            else:
                pass


def register_handlers_shorten_url_command(dp: Dispatcher):
    dp.register_message_handler(shorten_url, commands='short')
