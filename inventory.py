import json
import typing
from datetime import datetime

inventory_file = 'data/inventory.json'

def load_inventory() -> dict:
    try:
        with open(inventory_file, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_inventory(inventory: dict) -> None:
    with open(inventory_file, 'w') as f:
        json.dump(inventory, f, indent=4)

def get_inventory(username: str) -> dict:
    inventory = load_inventory()
    return inventory.get(username, {})

def add_item(username: str, name: str, quantity: int, price: float, Code: str, expiry_date: str) -> bool:
    inventory = load_inventory()
    user_inventory = inventory.get(username, {})
    if name in user_inventory:
        return False
    item_id = len(user_inventory) + 1
    user_inventory[name] = [{
        "id": item_id,
        "name": name,
        "quantity": quantity,
        "price": price,
        "Code": Code,
        "expiry_date": expiry_date,
        "created_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }]
    inventory[username] = user_inventory
    save_inventory(inventory)
    return True

def update_item(username: str, name: str, quantity: int, price: float, Code: str, expiry_date: str) -> bool:
    inventory = load_inventory()
    user_inventory = inventory.get(username, {})
    if name not in user_inventory:
        return False
    user_inventory[name] = [{
        "id": user_inventory[name][0]['id'],
        "name": name,
        "quantity": quantity,
        "price": price,
        "Code": Code,
        "expiry_date": expiry_date,
        "created_at": user_inventory[name][0]['created_at'],
        "updated_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }]
    inventory[username] = user_inventory
    save_inventory(inventory)
    return True

def delete_item(username: str, name: str) -> bool:
    inventory = load_inventory()
    user_inventory = inventory.get(username, {})
    if name not in user_inventory:
        return False
    del user_inventory[name]
    inventory[username] = user_inventory
    save_inventory(inventory)
    return True
