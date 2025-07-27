from aiogram import types


async def cmd_ban_reason(message: types.Message, number_of_words):
    """
    Функция берет количество слов на которые нужно поделить, и делает это
    """
    words = message.text.split()
    result = " ".join(words[number_of_words:])
    return result
