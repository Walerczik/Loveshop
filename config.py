import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

# ВАЖНО: здесь ключ — это строка-переменная, а не сам ID
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))  # по умолчанию 0
USER_ID = int(os.getenv("USER_ID", "0"))
WEBHOOK_HOST = os.getenv("WEBHOOK_HOST")  # например: "https://your-app.onrender.com"
WEBHOOK_PATH = f"/webhook/{BOT_TOKEN}"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = int(os.getenv("PORT", 8000))