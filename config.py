import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))  # Твой Telegram ID
USER_ID = int(os.getenv("USER_ID"))    # Telegram ID девушки