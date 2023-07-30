import re
from aiogram import Dispatcher
from aiogram import types
from db.db import DataBase

db = DataBase()


async def add_expense(message: types.Message):
    match_message = re.match(r'([\d ]+) (.*)', message.text)
    cost = int(match_message.group(1))
    category_name = match_message.group(2)

    if category_name in db.get_category_names():
        db.insert(cost, category_name)
        await message.answer("Записано!")
        return
    await message.answer("Такой категории не существует")


async def get_day_expenses(message: types.Message):
    query = db.get_sql_day_expenses().fetchall()
    reply_message = ""
    for q in query:
        reply_message += f"*{q[0]}:* {q[1]}\n"

    amount = db.get_sql_day_sum_expenses().fetchone()[0]
    await message.answer("*Расходы за сегодня:*\n\n" + reply_message +
                         f"\n*Итог:* {amount}", parse_mode="Markdown")


async def get_month_expenses(message: types.Message):
    query = db.get_sql_month_expenses().fetchall()
    reply_message = ""
    for q in query:
        reply_message += f"*{q[0]}:* {q[1]}\n"

    amount = sum(q[1] for q in query)
    await message.answer("*Расходы за месяц:*\n\n" + reply_message +
                         f"\n*Итог:* {amount}", parse_mode="Markdown")


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(add_expense, regexp=r'([\d ]+) (.*)')
    dp.register_message_handler(get_day_expenses, commands=['day'])
    dp.register_message_handler(get_month_expenses, commands=['month'])
