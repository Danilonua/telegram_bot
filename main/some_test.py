import pytest
from main.utils import test_user, test_chat
from help_commands.pin_files.pin import cmd_pin
from unittest.mock import AsyncMock
from handlers.other_commands import cmd_start, cmd_help


@pytest.mark.asyncio
async def test_cmd_start():
    text_mock = "Привет, я бот модератор! Что бы увидеть мои команды напишите в чат /help."  # ожиданный результат
    message_mock = AsyncMock(text=text_mock)
    await cmd_start(message=message_mock)
    message_mock.reply.assert_called_with(text_mock)


@pytest.mark.asyncio
async def test_cmd_help():
    text_mock = "Сейчас я покажу самые главные команды, но если хочешь увидеть больше команд и подробную" \
                " инструкцию до них перейдите, пожалуйста, за ссылкой ниже. Команды: \n\n /start - для " \
                "начала работы с ботом\n /help - для помощи\n /warn - для надавания предупреждений пользователю" \
                "\n /view_warns - для просмотра количества варнов пользователя\n /mute - для забирания прав " \
                "у человека, писать что то в чат\n /unmute - для размута\n /ban - для бана пользователя\n" \
                " /unban - для разбана пользователя. Вот ссылка на подробную инструкцию и дополнительные " \
                "команды:\nhttps://teletype.in/@pythonhelper/NlOZOS5iAB5 "  # ожиданный результат
    message_mock = AsyncMock(text=text_mock)
    await cmd_help(message=message_mock)
    message_mock.reply.assert_called_with(text_mock)


@pytest.mark.asyncio
async def test_cmd_pin():
    text_mock = "/pin 1"
    message_mock = AsyncMock(text=text_mock)
    await cmd_pin(message=message_mock, test_user=test_user, test_chat=test_chat)
    message_mock.reply.assert_called_with("Ошибка: Chat not found")