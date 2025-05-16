import os
import json

from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("API_TOKEN")
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"https://loveshop.onrender.com{WEBHOOK_PATH}"
ADMIN_ID = int(os.getenv("ADMIN_ID"))
GIRL_ID = int(os.getenv("GIRL_ID"))

db_path = "data/db.json"

def load_db():
    if not os.path.exists(db_path):
        return {"balances": {}, "products": {}}
    with open(db_path, "r") as f:
        return json.load(f)

def save_db(data):
    with open(db_path, "w") as f:
        json.dump(data, f, indent=2)
