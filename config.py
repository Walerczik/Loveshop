import os
from dotenv import load_dotenv

load_dotenv()

ADMIN_ID = os.getenv("ADMIN_ID")
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBAPP_HOST = os.getenv("WEBAPP_HOST", "0.0.0.0")
WEBHOOK_PATH = "/webhook"
BASE_WEBHOOK_URL = os.getenv("BASE_WEBHOOK_URL")  # например: https://your-render-url.onrender.com
WEBHOOK_URL = f"{BASE_WEBHOOK_URL}{WEBHOOK_PATH}"