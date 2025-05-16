import os
import json
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiohttp import web
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
GIRL_ID = int(os.getenv("GIRL_ID"))
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

WEBHOOK_PATH = '/webhook'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

DATA_FILE = 'data.json'

def load_data():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except:
        return {"balances": {}, "items": [], "orders": []}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def main_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("💋 Баланс"), KeyboardButton("🛍 Заказать"))
    return keyboard

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if message.from_user.id == GIRL_ID:
        await message.answer("Привет, любимая ❤️", reply_markup=main_keyboard())
    elif message.from_user.id == ADMIN_ID:
        await message.answer("Админ режим включен. Используй команды.")

@dp.message_handler(lambda m: m.text == "💋 Баланс")
async def balance(message: types.Message):
    data = load_data()
    bal = data["balances"].get(str(message.from_user.id), 0)
    await message.answer(f"У тебя {bal} поцелуйчиков 💋")

@dp.message_handler(lambda m: m.text == "🛍 Заказать")
async def show_items(message: types.Message):
    data = load_data()
    items = data["items"]
    if not items:
        await message.answer("Сейчас нет доступных заказов.")
        return
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for item in items:
        keyboard.add(KeyboardButton(f'{item["name"]} ({item["price"]}💋)'))
    keyboard.add(KeyboardButton("🔙 Назад"))
    await message.answer("Выбери, что хочешь заказать:", reply_markup=keyboard)

@dp.message_handler(lambda m: m.text == "🔙 Назад")
async def go_back(message: types.Message):
    await message.answer("Главное меню", reply_markup=main_keyboard())

@dp.message_handler(lambda m: m.from_user.id == GIRL_ID)
async def handle_order(message: types.Message):
    data = load_data()
    for item in data["items"]:
        if item["name"] in message.text:
            uid = str(message.from_user.id)
            balance = data["balances"].get(uid, 0)
            if balance >= item["price"]:
                data["balances"][uid] = balance - item["price"]
                data["orders"].append({"user": uid, "item": item["name"]})
                save_data(data)
                await message.answer(f"Ты заказала: {item['name']} 😘", reply_markup=main_keyboard())
                await bot.send_message(ADMIN_ID, f"👩‍❤️‍👨 Она заказала: {item['name']} ({item['price']}💋)")
            else:
                await message.answer("Недостаточно поцелуев 😢", reply_markup=main_keyboard())
            return
    await message.answer("Не понимаю. Попробуй снова.", reply_markup=main_keyboard())

@dp.message_handler(commands=['additem'])
async def add_item(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    try:
        _, name, price = message.text.split(maxsplit=2)
        price = int(price)
        data = load_data()
        data["items"].append({"name": name, "price": price})
        save_data(data)
        await message.answer(f"Добавлено: {name} за {price}💋")
    except:
        await message.answer("Формат: /additem Название 10")

@dp.message_handler(commands=['give'])
async def give_kisses(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    try:
        _, uid, amount = message.text.split()
        amount = int(amount)
        data = load_data()
        data["balances"][uid] = data["balances"].get(uid, 0) + amount
        save_data(data)
        await message.answer(f"Начислено {amount}💋 пользователю {uid}")
    except:
        await message.answer("Формат: /give user_id amount")

@dp.message_handler(commands=['orders'])
async def show_orders(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    data = load_data()
    if not data["orders"]:
        await message.answer("Нет заказов.")
    else:
        msg = "\n".join([f"{o['user']} → {o['item']}" for o in data["orders"]])
        await message.answer(f"📦 Заказы:\n{msg}")

# Webhook
async def on_startup(app):
    await bot.set_webhook(WEBHOOK_URL)

async def on_shutdown(app):
    await bot.delete_webhook()
    await bot.close()

app = web.Application()
app.router.add_post(WEBHOOK_PATH, dp.webhook_handler)
app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)

if __name__ == '__main__':
    web.run_app(app, port=3000)