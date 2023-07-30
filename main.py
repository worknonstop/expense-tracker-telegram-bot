import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv
from db.db import DataBase
from handlers.handlers import register_handlers


load_dotenv('.env')
token = os.getenv("TOKEN")

bot = Bot(token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

d_base = DataBase()


async def main():
    register_handlers(dp)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
