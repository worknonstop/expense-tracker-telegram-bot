import re
from aiogram import Dispatcher
from aiogram import types
from db.db import DataBase
import text

db = DataBase()


async def add_expense(message: types.Message):
    match_message = re.match(r'([\d ]+) (.*)', message.text)
    cost = int(match_message.group(1))
    category_name = match_message.group(2)

    if category_name in db.get_list_categories():
        db.insert(cost, category_name)
        await message.answer("Записано!")
        return
    await message.answer("Такой категории не существует")


async def get_day_expenses(message: types.Message):
    query = db.get_sql_day_expenses().fetchall()
    reply_message = ""
    for q in query:
        reply_message += f"*{q[0]}:* {q[1]}\n"

    amount = sum(q[1] for q in query)
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


async def get_week_expenses(message: types.Message):
    query = db.get_sql_week_expenses().fetchall()
    reply_message = ""
    for q in query:
        reply_message += f"*{q[0]}:* {q[1]}\n"

    amount = sum(q[1] for q in query)
    await message.answer("*Расходы за неделю:*\n\n" + reply_message +
                         f"\n*Итог:* {amount}", parse_mode="Markdown")


async def get_commands(message: types.Message):
    commands = text.commands
    await message.answer(commands, parse_mode="Markdown")


async def get_categories(message: types.Message):
    list_categories = db.get_list_categories()
    category_names = "\n".join(category for category in list_categories)
    await message.answer("Все категории расходов:\n" + category_names)


async def get_five_last(message: types.Message):
    query = db.get_sql_five_last().fetchall()
    five_last = ""
    for q in query:
        five_last += f"*{q[0]}:* {q[1]}\n"
    await message.answer("Показать последние расходы:\n" + five_last, parse_mode="Markdown")


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(add_expense, regexp=r'([\d ]+) (.*)')
    dp.register_message_handler(get_day_expenses, commands=['day'])
    dp.register_message_handler(get_month_expenses, commands=['month'])
    dp.register_message_handler(get_week_expenses, commands=['week'])
    dp.register_message_handler(get_commands, commands=['start', 'help'])
    dp.register_message_handler(get_categories, commands=['categories'])
    dp.register_message_handler(get_five_last, commands=['last'])
