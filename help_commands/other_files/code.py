from aiogram import types, Dispatcher
from random import sample


async def code(message: types.Message):
    text = message.text.lower()[6:]
    if text == "":
        await message.reply("Введите сообщение, которое надо зашифровать!")
    else:
        new_name = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "<", ">"]
        old_name = ["м", "л", "с", "т", "н", "г", "д", "к", "р", "п", "б"]
        new_name = sample(new_name, 11)
        code_text = message.text.lower()[6:]

        for i in range(0, 11, 1):
            code_text = code_text.replace(old_name[i], new_name[i])

        code_for_uncode = ""
        for x in range(0, 11, 1):
            code_for_uncode += new_name[x]

        await message.reply(f"Ваше сообщение зашифровано успешно. Вот оно: `{code_text}` . Ваш код для расшифровки"
                            f" сообщения: `{code_for_uncode}`"
                            f" \n м - {new_name[0]} \n л - {new_name[1]} \n с - {new_name[2]} \n т - {new_name[3]}"
                            f" \n н - {new_name[4]} \n г - {new_name[5]} \n д - {new_name[6]} \n к - {new_name[7]}"
                            f" \n р - {new_name[8]} \n п - {new_name[9]} \n б - {new_name[10]}", parse_mode="Markdown")


async def uncode(message: types.Message):
    check_all_elements = len(message.text.split())
    if check_all_elements < 3:
        await message.reply(f"Внимание! Вы что-то забыли написать! Убедитесь что в начале идет команда, дальше код для"
                            f" расшифровки и потом сам текст, который надо расшифровать. ")
    else:
        code_for_uncode = message.text.split()[1]
        len_of_code_for_uncode = len(code_for_uncode)
        if len_of_code_for_uncode < 11:
            await message.reply(f"Внимание! Код для расшифровки не правильно написан!")
        else:
            uncode_text = message.text[20:]

            new_name = ["м", "л", "с", "т", "н", "г", "д", "к", "р", "п", "б"]
            for i in range(0, 11, 1):
                uncode_text = uncode_text.replace(code_for_uncode[i], new_name[i])

            await message.reply(f"Ваше сообщение расшифровано успешно. Вот оно: `{uncode_text}` .",
                                parse_mode="Markdown")


def register_handlers_code(dp: Dispatcher):
    dp.register_message_handler(code, commands="code")
    dp.register_message_handler(uncode, commands="uncode")