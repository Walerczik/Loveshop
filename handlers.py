from aiogram import types, Dispatcher
from config import ADMIN_ID, USER_ID
from keyboards import get_shop_keyboard
from models import (
    get_balance, add_balance, subtract_balance,
    get_items, add_item, remove_item
)

async def start_cmd(message: types.Message):
    if message.from_user.id == USER_ID:
        balance = get_balance(USER_ID)
        await message.answer(f"Добро пожаловать в магазин любви 💖\nТвой баланс: {balance} поцелуйчиков 💋", reply_markup=get_shop_keyboard())
    elif message.from_user.id == ADMIN_ID:
        await message.answer("Привет, админ! Напиши /help для команд.")

async def handle_order(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    if user_id != USER_ID:
        return await callback_query.answer("Только для твоей девушки 😉", show_alert=True)

    item_key = callback_query.data.replace("order_", "")
    items = get_items()
    item = items.get(item_key)
    if not item:
        return await callback_query.answer("Такого товара нет.")

    # Предполагаем, что цена — последние число из строки
    try:
        price = int(item.split("—")[-1].replace("поцелуйчиков", "").strip())
    except:
        return await callback_query.answer("Ошибка с ценой.")

    if subtract_balance(USER_ID, price):
        await callback_query.answer("Заказ оформлен 💌")
        await callback_query.message.answer(f"Ты заказала: {item}")
        await callback_query.bot.send_message(ADMIN_ID, f"💌 Девушка заказала: {item}")
    else:
        await callback_query.answer("Недостаточно поцелуйчиков 😢", show_alert=True)

# ---------------------
# Админ-команды
# ---------------------

async def help_cmd(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    await message.answer("/add_item id название — добавить товар\n"
                         "/remove_item id — удалить\n"
                         "/add_balance amount — начислить поцелуйчики\n"
                         "/balance — показать баланс девушки")

async def add_item_cmd(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    try:
        _, item_id, *desc = message.text.split()
        description = " ".join(desc)
        add_item(item_id, description)
        await message.answer(f"Товар добавлен: {description}")
    except:
        await message.answer("Ошибка. Пример: /add_item cinema 🎬 Сходить в кино — 10 поцелуйчиков")

async def remove_item_cmd(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    try:
        _, item_id = message.text.split()
        if remove_item(item_id):
            await message.answer(f"Удалено: {item_id}")
        else:
            await message.answer("Не найдено.")
    except:
        await message.answer("Пример: /remove_item cinema")

async def add_balance_cmd(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    try:
        _, amount = message.text.split()
        add_balance(USER_ID, int(amount))
        await message.answer(f"Начислено {amount} поцелуйчиков 💋")
    except:
        await message.answer("Пример: /add_balance 10")

async def balance_cmd(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    bal = get_balance(USER_ID)
    await message.answer(f"Баланс девушки: {bal} поцелуйчиков")

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_cmd, commands=['start'])
    dp.register_callback_query_handler(handle_order, lambda c: c.data.startswith("order_"))

    dp.register_message_handler(help_cmd, commands=["help"])
    dp.register_message_handler(add_item_cmd, commands=["add_item"])
    dp.register_message_handler(remove_item_cmd, commands=["remove_item"])
    dp.register_message_handler(add_balance_cmd, commands=["add_balance"])
    dp.register_message_handler(balance_cmd, commands=["balance"])