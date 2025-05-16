from aiogram import Dispatcher, types
from config import USER_IDS

async def start_user(message: types.Message):
    await message.answer("👋 Привет, малышка! Давай заказывай.")

def register_user(dp: Dispatcher):
    dp.register_message_handler(start_user, commands=["start"], user_id=USER_IDS)
