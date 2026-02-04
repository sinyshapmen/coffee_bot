import os
from dataclasses import dataclass
from typing import Optional, Tuple

from aiogram import Bot
from aiogram.types import LabeledPrice, PreCheckoutQuery

PROVIDER_TOKEN = os.getenv("API_UMONEY")

@dataclass(frozen=True)
class Item:
    code: str
    title: str
    description: str
    price_rub: int


ITEMS = {
    "coffee": Item(code="coffee", title="Кофе", description="Свежесваренный кофе", price_rub=135),
    "pirozhok": Item(code="pirozhok", title="Пирожок", description="Домашний пирожок", price_rub=80),
}


def okrug(rub: int) -> int:
    return rub * 100


def get_item(item_type: str) -> Item:
    if item_type not in ITEMS:
        raise ValueError(f"Неизвестный товар")
    return ITEMS[item_type]


def build_payload(item_type: str) -> str:
    item = get_item(item_type)
    return f"order:{item.code}:{item.price_rub}"


def parse_payload(payload: str) -> Optional[str]:
    try:
        prefix, code, price = payload.split(":")
    except ValueError:
        return None
    if prefix != "order":
        return None
    if code not in ITEMS:
        return None
    if str(ITEMS[code].price_rub) != price:
        return None
    return code


def build_prices(item_type: str) -> list[LabeledPrice]:
    item = get_item(item_type)
    return [LabeledPrice(label=item.title, amount=okrug(item.price_rub))]


async def send_invoice(bot: Bot, chat_id: int, item_type: str) -> None:
    if not PROVIDER_TOKEN:
        raise RuntimeError("Нет провайдера")

    item = get_item(item_type)

    await bot.send_invoice(
        chat_id=chat_id,
        title=item.title,
        description=item.description,
        payload=build_payload(item_type),
        provider_token=PROVIDER_TOKEN,
        currency="RUB",
        prices=build_prices(item_type),
        start_parameter=f"buy_{item_type}",
    )


def validate(query: PreCheckoutQuery) -> Tuple[bool, Optional[str]]:
    item_type = parse_payload(query.invoice_payload)
    if not item_type:
        return False, "Некорректный товар."
    if query.currency != "RUB":
        return False, "Неверная валюта."
    expected = okrug(get_item(item_type).price_rub)
    if query.total_amount != expected:
        return False, "Неверная сумма."
    return True, None