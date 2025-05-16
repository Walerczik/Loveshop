from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import register_handlers

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

register_handlers(dp)