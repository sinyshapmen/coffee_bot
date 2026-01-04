import logging
from aiogram import Bot, Dispatcher
import asyncio
import os

from handlers import router as private_router
from group import router as group_router

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

    bot = Bot(token=os.getenv("TELEGRAM_API_KEY"))
    dp = Dispatcher()

    dp.include_router(group_router)
    dp.include_router(private_router)

    logging.info("Bot started")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())