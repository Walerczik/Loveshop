import os
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import Update

from config import BOT_TOKEN, WEBHOOK_URL, WEBAPP_HOST, WEBHOOK_PATH
from handlers import register_handlers  # ваш модуль с хендлерами

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())
register_handlers(dp)

# Установка webhook при запуске
async def on_startup(app):
    await bot.set_webhook(WEBHOOK_URL)

# Удаление webhook при остановке
async def on_shutdown(app):
    await bot.delete_webhook()
    await dp.storage.close()
    await dp.storage.wait_closed()

# Обработка входящих обновлений от Telegram
async def handle(request):
    request_data = await request.json()
    update = Update.to_object(request_data)
    await dp.process_update(update)
    return web.Response()

# Настройка приложения aiohttp
app = web.Application()
app.router.add_post(WEBHOOK_PATH, handle)
app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)

if __name__ == '__main__':
    port = int(os.getenv("PORT", 10000))  # Render задаёт PORT как переменную окружения
    web.run_app(app, host=WEBAPP_HOST, port=port)