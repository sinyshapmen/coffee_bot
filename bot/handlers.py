from aiogram import Router, types, F, Bot
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db.api import add_user
from utils import send_invoice, validate, get_item, parse_payload

router = Router()

class Callbacks:
    COFFEE = 'order_coffee'
    PIROZHOK = 'order_pirozhok'
    PAY = 'pay'
    CANCEL = 'cancel'

def start_keyboard() -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.add(types.InlineKeyboardButton(text="☕ Кофе", callback_data=Callbacks.COFFEE))
    builder.add(types.InlineKeyboardButton(text="🍰 Пирожок", callback_data=Callbacks.PIROZHOK))

    return builder.as_markup()

def pay_keyboard(item_type: str) -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="Отмена", callback_data=Callbacks.CANCEL))
    builder.add(types.InlineKeyboardButton(text="Оплатить", callback_data=f"{Callbacks.PAY}_{item_type}"))
    return builder.as_markup()

@router.message(Command("start"))
async def handle_start(message: types.Message):
    keyboard = start_keyboard()
    await message.answer(
        "Приветствую! Выберите, что бы вы хотели заказать",
        reply_markup=keyboard
    )

@router.callback_query()
async def handle_callback_query(callback_query: types.CallbackQuery, bot: Bot):
    if callback_query.data == Callbacks.COFFEE:
        item = get_item('coffee')
        keyboard = pay_keyboard('coffee')
        await callback_query.message.edit_text(
            f"🧾 Сумма к оплате <b>{item.price_rub} ₽</b>",
            reply_markup=keyboard,
            parse_mode="HTML",
        )
    elif callback_query.data == Callbacks.PIROZHOK:
        item = get_item('pirozhok')
        keyboard = pay_keyboard('pirozhok')
        await callback_query.message.edit_text(
            f"🧾 Сумма к оплате <b>{item.price_rub} ₽</b>",
            reply_markup=keyboard,
            parse_mode="HTML",
        )
    elif callback_query.data.startswith(f"{Callbacks.PAY}_"):
        item_type = callback_query.data.split('_')[1]
        await send_invoice(bot, callback_query.message.chat.id, item_type)
    elif callback_query.data == Callbacks.CANCEL:
        keyboard = start_keyboard()
        await callback_query.message.edit_text(
            "Привет! Выберите, что бы вы хотели заказать:",
            reply_markup=keyboard
        )
    else:
        await callback_query.message.answer("err")

    await callback_query.answer()

@router.pre_checkout_query()
async def pre_checkout_handler(query: types.PreCheckoutQuery, bot: Bot):
    ok, err = validate(query)
    await bot(query.answer(ok=ok, error_message=err))

@router.message(F.successful_payment)
async def successful_payment_handler(message: types.Message):
    payload = message.successful_payment.invoice_payload
    item_type = parse_payload(payload)
    if not item_type:
        await message.answer("Ошибка: не удалось определить товар.")
        return

    add_user(message.from_user.id, item_type)
    await message.answer("Оплата успешна! Спасибо!")
