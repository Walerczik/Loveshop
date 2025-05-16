import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

# ВАЖНО: здесь ключ — это строка-переменная, а не сам ID
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))  # по умолчанию 0