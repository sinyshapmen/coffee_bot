import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types, enums
from aiogram.enums import ParseMode
from handlers import router as handlers_router

API_TOKEN = os.getenv("TELEGRAM_API_KEY")
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

async def main():
    dp.include_router(handlers_router) 
    logging.info("bot polling")
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Bot stopped by user")
    except Exception as e:
        logging.error(f"error: {e}")