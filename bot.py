from aiogram import Bot, Dispatcher, executor
from config import BOT_TOKEN
from handlers import register_handlers

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

register_handlers(dp)

if __name__ == '__main__':
    from models import load_data  # чтобы создать файл при первом запуске
    load_data()
    executor.start_polling(dp, skip_updates=True)