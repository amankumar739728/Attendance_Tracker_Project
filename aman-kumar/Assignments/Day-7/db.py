import sqlite3
from sqlite3 import Connection

DATABASE_NAME = "users.db"

def get_connection() -> Connection:
    conn = sqlite3.connect(DATABASE_NAME)
    return conn

def create_user_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            hashed_password TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()

# Initialize the database and create the user table on module import
create_user_table()
