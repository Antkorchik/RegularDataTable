import hashlib
from datetime import datetime
from typing import Optional, Dict


class User:
    def __init__(self, user_id: int, login: str, password: str):
        self.user_id = user_id
        self.login = login
        self.password = password
        self.created_at = datetime.now()
        self.last_active_at = datetime.now()


class Storage:
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.next_user_id = 1
        print("Storage initialized")

    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self, login: str, password: str) -> Optional[User]:
        if login in self.users:
            return None
        hashed_password = self._hash_password(password)
        user = User(self.next_user_id, login, hashed_password)
        self.users[login] = user
        self.next_user_id += 1
        return user

    def update_last_active(self, login: str):
        if login in self.users:
            self.users[login].last_active_at = datetime.now()

    def get_user(self, login: str) -> Optional[User]:
        return self.users.get(login)