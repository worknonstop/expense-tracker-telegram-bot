import re
import os
from functools import wraps

import text
from aiogram import Dispatcher
from aiogram import types
from db.db import DataBase
from dotenv import load_dotenv

db = DataBase()

load_dotenv('.env')
ADMIN_IDS = os.getenv("ADMIN_IDS")


def auth(func):
    @wraps(func)
    async def wrapped(message: types.Message, *args, **kwargs):
        user_id = message.from_user.id
        if str(user_id) not in ADMIN_IDS:
            await message.answer("Нет доступа.")
            return
        return await func(message, *args, **kwargs)
    return wrapped


@auth
async def add_expense(message: types.Message):
    match_message = re.match(r'([\d ]+) (.*)', message.text)
    cost = int(match_message.group(1))
    category_name = match_message.group(2)

    if category_name in db.get_list_categories():
        db.insert(cost, category_name)
        await message.answer("Записано!")
        return
    await message.answer("Такой категории не существует")


@auth
async def get_day_expenses(message: types.Message):
    query = db.get_sql_day_expenses().fetchall()
    reply_message = ""
    for q in query:
        reply_message += f"*{q[0]}:* {q[1]}\n"

    amount = sum(q[1] for q in query)
    await message.answer("*Расходы за сегодня:*\n\n" + reply_message +
                         f"\n*Итог:* {amount}", parse_mode="Markdown")


@auth
async def get_month_expenses(message: types.Message):
    query = db.get_sql_month_expenses().fetchall()
    reply_message = ""
    for q in query:
        reply_message += f"*{q[0]}:* {q[1]}\n"

    amount = sum(q[1] for q in query)
    await message.answer("*Расходы за месяц:*\n\n" + reply_message +
                         f"\n*Итог:* {amount}", parse_mode="Markdown")


@auth
async def get_week_expenses(message: types.Message):
    query = db.get_sql_week_expenses().fetchall()
    reply_message = ""
    for q in query:
        reply_message += f"*{q[0]}:* {q[1]}\n"

    amount = sum(q[1] for q in query)
    await message.answer("*Расходы за неделю:*\n\n" + reply_message +
                         f"\n*Итог:* {amount}", parse_mode="Markdown")


@auth
async def get_commands(message: types.Message):
    commands = text.commands
    await message.answer(commands, parse_mode="Markdown")


@auth
async def get_categories(message: types.Message):
    list_categories = db.get_list_categories()
    category_names = "\n".join(category for category in list_categories)
    await message.answer("Все категории расходов:\n" + category_names)


@auth
async def get_five_last(message: types.Message):
    query = db.get_sql_five_last().fetchall()
    five_last = ""
    for i, q in enumerate(query, start=1):
        five_last += f"*{q[0]}:* {q[1]}    /del{i}\n"
    await message.answer("Показать последние расходы:\n" + five_last, parse_mode="Markdown")


@auth
async def delete_entry(message: types.Message):
    number_from_message = int(message.text[4:])
    five_last = db.get_sql_five_last().fetchall()
    for i, entry in enumerate(five_last, start=1):
        if i == number_from_message:
            db.delete_sql_entry(str(entry[2]))
            await message.answer(f"Удалено {entry[0]}: {entry[1]}")


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(add_expense, regexp=r'([\d ]+) (.*)')
    dp.register_message_handler(get_day_expenses, commands=['day'])
    dp.register_message_handler(get_month_expenses, commands=['month'])
    dp.register_message_handler(get_week_expenses, commands=['week'])
    dp.register_message_handler(get_commands, commands=['start', 'help'])
    dp.register_message_handler(get_categories, commands=['kinds'])
    dp.register_message_handler(get_five_last, commands=['last'])
    dp.register_message_handler(delete_entry, regexp=r'/del(\d+)')
