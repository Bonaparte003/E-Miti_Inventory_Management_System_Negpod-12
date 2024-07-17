import json
import hashlib
import typing

USERS_DB = "data/users.json"

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    try:
        with open(USERS_DB, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_users(users):
    with open(USERS_DB, "w") as f:
        json.dump(users, f)

def register_user(username: str, password: str, role: str) -> bool:
    users = load_users()
    if any(user['username'] == username for user in users):
        return False
    users.append({"username": username, "password": hash_password(password), "role": role})
    save_users(users)
    return True

def authenticate_user(username: str, password: str, role_required: typing.Optional[str] = None) -> typing.Tuple[bool, str]:
    users = load_users()
    hashed_password = hash_password(password)
    for user in users:
        if user['username'] == username and user['password'] == hashed_password:
            if role_required is None or user['role'] == role_required:
                return True, user['role']
            else:
                return False, None
    return False, None
