import logging
from aiogram import Bot, Dispatcher
import asyncio
import os

from handlers import router as private_router
from group import router as group_router
from db.api import clear_old, cleanup_loop

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

    cleanup = asyncio.create_task(cleanup_loop())
    try:
        await dp.start_polling(bot)
    finally:
        cleanup.cancel()


if __name__ == "__main__":
    asyncio.run(main())