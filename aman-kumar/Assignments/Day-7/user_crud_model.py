import sqlite3
from sqlite3 import Connection
from db import get_connection
from security import hash_password, verify_password

def create_user(username: str, password: str) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    hashed_pw = hash_password(password)
    try:
        cursor.execute(
            "INSERT INTO users (username, hashed_password) VALUES (?, ?)",
            (username, hashed_pw),
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def update_user_password(username: str, new_password: str) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    hashed_pw = hash_password(new_password)
    try:
        cursor.execute(
            "UPDATE users SET hashed_password = ? WHERE username = ?",
            (hashed_pw, username),
        )
        conn.commit()
        return cursor.rowcount > 0
    except Exception:
        return False
    finally:
        conn.close()

def delete_user(username: str) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "DELETE FROM users WHERE username = ?",
            (username,),
        )
        conn.commit()
        return cursor.rowcount > 0
    except Exception:
        return False
    finally:
        conn.close()

def get_user(username: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, hashed_password FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"id": row[0], "username": row[1], "hashed_password": row[2]}
    return None

def authenticate_user(username: str, password: str) -> bool:
    user = get_user(username)
    if not user:
        return False
    return verify_password(password, user["hashed_password"])

def get_all_users(skip: int = 0, limit: int = 10):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username FROM users LIMIT ? OFFSET ?", (limit, skip))
    rows = cursor.fetchall()
    conn.close()
    users = [{"id": row[0], "username": row[1]} for row in rows]
    return users
