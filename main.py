import logging
from aiogram import Bot, Dispatcher, executor, types

import exceptions
import dochody
from categories import Categories

logging.basicConfig(level=logging.INFO)

API_TOKEN = '1632822509:AAG_qRuLro27FinBs5-ugOpuR7RP9AY8UEQ'
ACCESS_ID = 573332887

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.answer(
        "Bot Złota Koza\n\n"
        "Dodajemy dochod: napisz dochod oraz kategorije\n"
        "Statystyka za dziszaj: /today\n"
        "Statystyka za miesząc: /month\n"
        "Ostatnie dochody: /dochody\n"
        "categories: /categories")


@dp.message_handler(lambda message: message.text.startswith('/del'))
async def del_dochod(message: types.Message):
    row_id = int(message.text[4:])
    dochody.delete_dochod(row_id)
    answer_message = "Usunięto"
    await message.answer(answer_message)


@dp.message_handler(commands=['categories'])
async def categories_list(message: types.Message):
    categories = Categories().get_all_categories()
    answer_message = "Kategorije dochodów:\n\n* " + \
                     ("\n* ".join([c.name + ' (' + ", ".join(c.aliases) + ')' for c in categories]))
    await message.answer(answer_message)


@dp.message_handler(commands=['today'])
async def today_statistics(message: types.Message):
    answer_message = dochody.get_today_statistics()
    await message.answer(answer_message)


@dp.message_handler(commands=['month'])
async def month_statistics(message: types.Message):
    answer_message = dochody.get_month_statistics()
    await message.answer(answer_message)


@dp.message_handler(commands=['dochody'])
async def list_dochody(message: types.Message):
    last_dochody = dochody.last()
    if not last_dochody:
        await message.answer("Nie masz jeszcze dochodów")
        return

    last_dochody_rows = [
        f"{dochod.amount} zł. na {dochod.category_name} — naćiśni "
        f"/del{dochod.id} żeby usunąć"
        for dochod in last_dochody]
    answer_message = "Ostatnie dochody:\n\n* " + "\n\n* " \
        .join(last_dochody_rows)
    await message.answer(answer_message)


@dp.message_handler()
async def add_dochod(message: types.Message):
    try:
        dochod = dochody.add_dochod(message.text)
    except exceptions.NotCorrectMessage as e:
        await message.answer(str(e))
        return
    answer_message = (
        f"Dodajemy dochod {dochod.amount} zł na {dochod.category_name}.\n\n"
        f"{dochody.get_today_statistics()}")
    await message.answer(answer_message)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
