from aiogram import Router, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()

class Callbacks:
    COFFEE = 'order_coffee'
    PIROZHOK = 'order_pirozhok'

def start_keyboard() -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.add(types.InlineKeyboardButton(text="☕ Кофе", callback_data=Callbacks.COFFEE))
    builder.add(types.InlineKeyboardButton(text="🍰 Пирожок", callback_data=Callbacks.PIROZHOK))

    return builder.as_markup()

@router.message(Command("start"))
async def handle_start(message: types.Message):
    keyboard = start_keyboard()
    await message.answer(
        "Привет! Выберите, что бы вы хотели заказать:",
        reply_markup=keyboard
    )

@router.callback_query()
async def handle_callback_query(callback_query: types.CallbackQuery):
    if callback_query.data == Callbacks.COFFEE:
        response = "Вы выбрали Кофе!"
    elif callback_query.data == Callbacks.PIROZHOK:
        response = "Вы выбрали Пирожок!"
    else:
        response = "Неизвестный выбор."

    await callback_query.message.answer(response)
    await callback_query.answer()