from typing import Dict, List
from passlib.context import CryptContext
from core.security import hash_password

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

fake_users_db = {
    "aman": {
        "username": "aman",
        "hashed_password": hash_password("test")
    }
}

user_tasks: Dict[str, List[str]] = {}