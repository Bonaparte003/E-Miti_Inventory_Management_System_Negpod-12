import typing
from datetime import datetime

class InventoryManagement:
    def __init__(self, db):
        self.db = db

    def add_item(self, user_id: int, name: str, quantity: int, price: float, code: str, expiry_date: str, flag: bool = False) -> bool:
        item = {
            "user_id": user_id,
            "name": name,
            "quantity": quantity,
            "price": price,
            "code": code,
            "expiry_date": expiry_date,
            "created_at": datetime.now(),
            "flag": flag
        }
        return self.db.save_item(item)

    def update_item(self, item_id: int, name: str, quantity: int, price: float, code: str, expiry_date: str) -> bool:
        item = {
            "id": item_id,
            "name": name,
            "quantity": quantity,
            "price": price,
            "code": code,
            "expiry_date": expiry_date
        }
        return self.db.update_item(item)

    def delete_item(self, item_id: int) -> bool:
        return self.db.delete_item(item_id)

    def flag_item(self, item_id: int) -> bool:
        return self.db.flag_item(item_id)

    def get_inventory(self, user_id: int) -> typing.List[dict]:
        return self.db.load_inventory(user_id)

    def get_top_users_for_item(self, item_name: str) -> typing.List[typing.Tuple[str, int]]:
        return self.db.load_top_users_for_item(item_name)
