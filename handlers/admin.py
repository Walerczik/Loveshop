from aiogram import Dispatcher, types
from config import ADMIN_IDS

async def start_admin(message: types.Message):
    await message.answer("👑 Привет, админ! Вебхук подключен и всё работает!")

def register_admin(dp: Dispatcher):
    dp.register_message_handler(start_admin, commands=["start"], user_id=ADMIN_IDS)
