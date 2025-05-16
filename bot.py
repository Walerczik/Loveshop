import os
import json
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiohttp import web
from config import (
    TOKEN, ADMIN_ID, GIRL_ID, WEBHOOK_URL, WEBHOOK_PATH,
    db_path, load_db, save_db
)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

db = load_db()

main_kb = ReplyKeyboardMarkup(resize_keyboard=True)
main_kb.add(KeyboardButton("🌸 Посмотреть баланс"))
main_kb.add(KeyboardButton("🎁 Магазин"))

# Команды админа
@dp.message_handler(lambda m: m.from_user.id == ADMIN_ID and m.text.startswith("/начислить"))
async def handle_add_kisses(message: types.Message):
    try:
        _, user_id, amount = message.text.split()
        user_id = int(user_id)
        amount = int(amount)
        db["balances"].setdefault(str(user_id), 0)
        db["balances"][str(user_id)] += amount
        save_db(db)
        await message.answer(f"Начислено {amount} поцелуев пользователю {user_id}")
    except Exception:
        await message.answer("Используй формат:\n/начислить <user_id> <amount>")

@dp.message_handler(lambda m: m.from_user.id == ADMIN_ID and m.text.startswith("/добавить_товар"))
async def handle_add_product(message: types.Message):
    try:
        _, title, price = message.text.split(maxsplit=2)
        product_id = str(len(db["products"]) + 1)
        db["products"][product_id] = {"title": title, "price": int(price)}
        save_db(db)
        await message.answer(f"Товар '{title}' добавлен за {price} поцелуев.")
    except Exception:
        await message.answer("Формат: /добавить_товар <название> <цена>")

# Старт
@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    if message.from_user.id == GIRL_ID:
        await message.answer("Добро пожаловать в магазин поцелуев 💋", reply_markup=main_kb)
    else:
        await message.answer("Привет! Ты админ 😎")

# Баланс
@dp.message_handler(lambda m: m.text == "🌸 Посмотреть баланс" and m.from_user.id == GIRL_ID)
async def handle_balance(message: types.Message):
    balance = db["balances"].get(str(message.from_user.id), 0)
    await message.answer(f"У тебя {balance} поцелуев 💋")

# Магазин
@dp.message_handler(lambda m: m.text == "🎁 Магазин" and m.from_user.id == GIRL_ID)
async def handle_shop(message: types.Message):
    text = "Выбери, что хочешь:\n\n"
    for pid, product in db["products"].items():
        text += f"{pid}. {product['title']} — {product['price']} поцелуев\n"
    text += "\nНапиши номер товара, чтобы заказать."
    await message.answer(text)

@dp.message_handler(lambda m: m.text.isdigit() and m.from_user.id == GIRL_ID)
async def handle_purchase(message: types.Message):
    pid = message.text.strip()
    user_id = str(message.from_user.id)
    if pid in db["products"]:
        product = db["products"][pid]
        price = product["price"]
        balance = db["balances"].get(user_id, 0)
        if balance >= price:
            db["balances"][user_id] -= price
            save_db(db)
            await message.answer(f"Ты заказала: {product['title']} 💌")
            await bot.send_message(ADMIN_ID, f"Заказ: {product['title']} от девушки!")
        else:
            await message.answer("Не хватает поцелуев 😢")
    else:
        await message.answer("Такого товара нет.")

# Вебхук
from aiogram.utils.executor import start_webhook

WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = int(os.environ.get("PORT", 10000))  # Render сам задаёт порт

async def on_startup(app):
    await bot.set_webhook(WEBHOOK_URL)

async def on_shutdown(app):
    await bot.delete_webhook()

# ⚠️ исправленный webhook handler
async def webhook_handler(request):
    try:
        data = await request.json()
        update = types.Update(**data)
        await dp.process_update(update)
    except Exception as e:
        print(f"Ошибка обработки webhook: {e}")
    return web.Response()

app = web.Application()
app.router.add_post(WEBHOOK_PATH, webhook_handler)
app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)

if __name__ == "__main__":
    web.run_app(app, host=WEBAPP_HOST, port=WEBAPP_PORT)