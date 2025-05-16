import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "7059973966:AAGgfFCEFTkSU37XadpRivPaYKsb3YaARVI")
ADMIN_IDS = [6909254042]
USER_IDS = [436851363]

WEBHOOK_PATH = f"/webhook/{BOT_TOKEN}"
WEBAPP_HOST = os.getenv("WEBAPP_HOST", "0.0.0.0")
WEBAPP_PORT = int(os.getenv("PORT", "10000"))

BASE_URL = os.getenv("RENDER_EXTERNAL_URL") or os.getenv("BASE_URL")
if not BASE_URL:
    raise RuntimeError("BASE_URL или RENDER_EXTERNAL_URL не установлены")

WEBHOOK_URL = f"{BASE_URL}{WEBHOOK_PATH}"
