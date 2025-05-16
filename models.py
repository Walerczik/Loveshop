import json
import os

DATA_FILE = "data.json"

# Структура JSON:
# {
#   "balance": {
#       "123456789": 100
#   },
#   "items": {
#       "order_cinema": "🎬 Сходить в кино — 10 поцелуйчиков"
#   }
# }

def load_data():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump({"balance": {}, "items": {}}, f)
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def get_balance(user_id):
    data = load_data()
    return data["balance"].get(str(user_id), 0)

def add_balance(user_id, amount):
    data = load_data()
    user_id = str(user_id)
    data["balance"][user_id] = data["balance"].get(user_id, 0) + amount
    save_data(data)

def subtract_balance(user_id, amount):
    data = load_data()
    user_id = str(user_id)
    current = data["balance"].get(user_id, 0)
    if current >= amount:
        data["balance"][user_id] = current - amount
        save_data(data)
        return True
    return False

def get_items():
    return load_data()["items"]

def add_item(item_id, description):
    data = load_data()
    data["items"][item_id] = description
    save_data(data)

def remove_item(item_id):
    data = load_data()
    if item_id in data["items"]:
        del data["items"][item_id]
        save_data(data)
        return True
    return False