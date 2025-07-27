from aiogram import types, Dispatcher


async def example(message: types.Message):
    # Example Description

    pass


def register_example_commands(dp: Dispatcher):
    dp.register_message_handler(example, commands='example')
