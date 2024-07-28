import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

class InventoryDatabase:
    def __init__(self, host, user, password, database):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.conn.cursor(dictionary=True)

    def save_item(self, item: dict) -> bool:
        try:
            self.cursor.execute(
                "INSERT INTO inventory (user_id, name, quantity, price, code, expiry_date, created_at, flag) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (item['user_id'], item['name'], item['quantity'], item['price'], item['code'], item['expiry_date'], item['created_at'], item['flag'])
            )
            self.conn.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False

    def update_item(self, item: dict) -> bool:
        try:
            self.cursor.execute(
                "UPDATE inventory SET name=%s, quantity=%s, price=%s, code=%s, expiry_date=%s WHERE id=%s",
                (item['name'], item['quantity'], item['price'], item['code'], item['expiry_date'], item['id'])
            )
            self.conn.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False

    def delete_item(self, item_id: int) -> bool:
        try:
            self.cursor.execute("DELETE FROM inventory WHERE id=%s", (item_id,))
            self.conn.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False

    def flag_item(self, item_id: int) -> bool:
        try:
            self.cursor.execute("UPDATE inventory SET flag=1 WHERE id=%s", (item_id,))
            self.conn.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False

    def load_inventory(self, user_id: int) -> list:
        try:
            self.cursor.execute("SELECT * FROM inventory WHERE user_id=%s", (user_id,))
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []

    def load_top_users_for_item(self, item_name: str) -> list:
        try:
            self.cursor.execute("""
                SELECT u.username, SUM(i.quantity) as total_quantity
                FROM inventory i
                JOIN users u ON i.user_id = u.id
                WHERE i.name = %s
                GROUP BY u.username
                ORDER BY total_quantity DESC
                LIMIT 5
            """, (item_name,))
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []
