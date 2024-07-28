import hashlib
import mysql.connector
import typing

class UserManagement:
    def __init__(self, db):
        self.db = db

    def hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self, username: str, password: str, role: str) -> bool:
        return self.db.save_user(username, self.hash_password(password), role)

    def authenticate_user(self, username: str, password: str) -> typing.Tuple[bool, int, str]:
        hashed_password = self.hash_password(password)
        user = self.db.get_user(username, hashed_password)
        if user:
            return True, user['id'], user['role']
        return False, None, None
