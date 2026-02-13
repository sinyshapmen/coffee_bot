import os
from datetime import datetime, timedelta
from aiogram import Router, types, Bot
from aiogram.filters import Command
from aiogram.exceptions import TelegramBadRequest
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db.api import get_stats

router = Router()

ADMINS_ID = list(map(int, os.getenv("ADMINS_ID", "").split(",")))

class StatsCallbacks:
    TODAY = "stats_today"
    YESTERDAY = "stats_yesterday"
    EARLIER = "stats_earlier"

def stats_keyboard() -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="Сегодня", callback_data=StatsCallbacks.TODAY))
    builder.add(types.InlineKeyboardButton(text="Вчера", callback_data=StatsCallbacks.YESTERDAY))
    builder.add(types.InlineKeyboardButton(text="Позавчера", callback_data=StatsCallbacks.EARLIER))
    return builder.as_markup()

def _day_range(day_offset: int) -> tuple[datetime, datetime]:
    now = datetime.now().astimezone()
    tz = now.tzinfo
    day = (now - timedelta(days=day_offset)).date()
    start = datetime.combine(day, datetime.min.time(), tzinfo=tz)
    end = start + timedelta(days=1)
    return start, end

def _format_stats(stats, selected_date: datetime) -> str:
    date_text = selected_date.strftime("%d.%m.%Y")
    if not stats:
        return f"📊 {date_text}\n\nНет данных за выбранный период"
    text = f"📊 {date_text}\n\n"
    for item, count in stats.items():
        emoji = "☕" if item == "coffee" else "🍰"
        display_name = "Кофе" if item == 'coffee' else 'Пирожок'
        text += f"{emoji} {display_name} — {count}\n"
    return text

@router.message(lambda m: m.new_chat_members is not None)
async def handle_adding(message: types.Message, bot: Bot):
    for member in message.new_chat_members:
        if member.is_bot and member.id == bot.id:
            added = message.from_user.id

            if added in ADMINS_ID:
                await message.answer(
                    "👋 Привет!\n"
                    "Я бот для учета заказов ☕🍰\n\n"
                    "<b>Посмотреть статистику: /stats</b>",
                    parse_mode='HTML'
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

    await message.answer(
        "Выберите период:",
        reply_markup=stats_keyboard()
    )

@router.callback_query(lambda c: c.data in {StatsCallbacks.TODAY, StatsCallbacks.YESTERDAY, StatsCallbacks.EARLIER})
async def stats_callback(callback_query: types.CallbackQuery):
    if callback_query.message.chat.type not in ("group", "supergroup"):
        return

    if callback_query.from_user.id not in ADMINS_ID:
        await callback_query.message.answer("❌ У вас нет прав на эту команду")
        await callback_query.answer()
        return

    if callback_query.data == StatsCallbacks.TODAY:
        start, end = _day_range(0)
    elif callback_query.data == StatsCallbacks.YESTERDAY:
        start, end = _day_range(1)
    else:
        start, end = _day_range(2)

    stats = get_stats(start, end)
    text = _format_stats(stats, start)
    try:
        await callback_query.message.edit_text(
            text,
            reply_markup=stats_keyboard()
        )
    except TelegramBadRequest as e:
        if "message is not modified" not in str(e):
            raise
    await callback_query.answer()
