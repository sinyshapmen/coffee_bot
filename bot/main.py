import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types, enums
from aiogram.filters import Command 
from aiogram.enums import ParseMode

API_TOKEN = os.getenv("TELEGRAM_API_KEY")
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def send_start(message: types.Message):
    await message.answer("окак скебобчик")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        logging.info("Starting bot")
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Bot stopped by user")