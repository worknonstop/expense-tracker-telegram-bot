import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv
from db.db import DataBase


load_dotenv('.env')
token = os.getenv("TOKEN")

bot = Bot(token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

d_base = DataBase()


@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    await message.answer('Start!')


async def main():
    d_base.create_tables()
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
