from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from models import get_items

def get_shop_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    for key, name in get_items().items():
        keyboard.add(InlineKeyboardButton(name, callback_data=f"order_{key}"))
    return keyboard