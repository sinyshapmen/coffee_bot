from aiogram import Router, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from db.api import add_user

router = Router()

class Callbacks:
    COFFEE = 'order_coffee'
    PIROZHOK = 'order_pirozhok'
    BUY = 'buy'
    PAY = 'pay'

def start_keyboard() -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.add(types.InlineKeyboardButton(text="☕ Кофе", callback_data=Callbacks.COFFEE))
    builder.add(types.InlineKeyboardButton(text="🍰 Пирожок", callback_data=Callbacks.PIROZHOK))

    return builder.as_markup()

def buy_keyboard(item_type: str) -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="Купить", callback_data=f"{Callbacks.BUY}_{item_type}"))
    return builder.as_markup()

def pay_keyboard(item_type: str) -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="Оплатить", callback_data=f"{Callbacks.PAY}_{item_type}"))
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
        keyboard = buy_keyboard('coffee')
        await callback_query.message.edit_text(
            "Вы выбрали Кофе!",
            reply_markup=keyboard
        )
    elif callback_query.data == Callbacks.PIROZHOK:
        keyboard = buy_keyboard('pirozhok')
        await callback_query.message.edit_text(
            "Вы выбрали Пирожок!",
            reply_markup=keyboard
        )
    elif callback_query.data.startswith(f"{Callbacks.BUY}_"):
        item_type = callback_query.data.split('_')[1]
        keyboard = pay_keyboard(item_type)
        await callback_query.message.edit_text(
            "К оплате 100р",
            reply_markup=keyboard
        )
    elif callback_query.data.startswith(f"{Callbacks.PAY}_"):
        item_type = callback_query.data.split('_')[1]
        user_id = callback_query.from_user.id
        add_user(user_id, item_type)
        await callback_query.message.edit_text("Оплата успешна! Вы добавлены в базу.")
    else:
        await callback_query.message.answer("err")

    await callback_query.answer()