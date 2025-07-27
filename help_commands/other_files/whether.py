import aiohttp
from aiogram import types, Dispatcher
from googletrans import Translator

API_KEY = 'ab66bedf8a0b13f2850b0c813d2220b6'


async def whether(message: types.Message):
    translator = Translator()
    city = message.text.strip().split()[1]
    detected_weather_lang = translator.detect(city).lang
    if detected_weather_lang != 'en':
        city_for_url = translator.translate(city, dest='en').text
    else:
        city_for_url = city
    weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={city_for_url}&appid={API_KEY}&units=metric'

    async with aiohttp.ClientSession() as session:
        async with session.get(weather_url) as response:
            response = await response.json()
    if response.get('cod') == 200:
        weather = response['weather'][0]['description']
        temperature = response['main']['temp']
        feels_like = response['main']['feels_like']
        humidity = response['main']['humidity']

        weather = translator.translate(weather, dest='ru').text
        reply = f'Погода в  {city}:\n'
        reply += f'- Погода: {weather}\n'
        reply += f'- Температура: {temperature}°C\n'
        reply += f'- Чуствуется: {feels_like}°C\n'
        reply += f'- Влажность: {humidity}%\n\n'

        await message.answer(text=reply)
    else:
        await message.answer(text='Попытайтесь написать название города на английском языке🏴󠁧󠁢󠁥󠁮󠁧󠁿')


def register_handlers_whether_command(dp: Dispatcher):
    dp.register_message_handler(whether, commands='weather')
