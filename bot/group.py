import os
from aiogram import Router, types, Bot
from aiogram.filters import Command

from db.api import get_stats

router = Router()

ADMINS_ID = os.getenv("ADMINS_ID")

@router.message(lambda m: m.new_chat_members is not None)
async def handle_adding(message: types.Message, bot: Bot):
    for member in message.new_chat_members:
        if member.is_bot and member.id == bot.id:
            added = message.from_user.id

            if added == ADMIN_ID:
                await message.answer(
                    "👋 Привет!\n\n"
                    "Я бот для учета заказов ☕🍰\n"
                    "Вывод статистики /stats"
                )
            else:
                await message.answer(
                    "❌ Я работаю только в личных сообщениях.\n"
                    "Добавлять меня в группы может только администратор."
                )


@router.message(Command("stats"))
async def stats_command(message: types.Message):
    if message.chat.type not in ("group", "supergroup"):
        return

    if message.from_user.id not in ADMINS_ID:
        await message.answer("❌ У вас нет прав на эту команду")
        return

    stats = get_stats()

    if not stats:
        await message.answer("📊 Пока нет заказов")
        return

    text = "📊 Статистика заказов:\n\n"
    for item, count in stats.items():
        emoji = "☕" if item == "coffee" else "🍰"
        text += f"{emoji} {item} — {count}\n"

    await message.answer(text)