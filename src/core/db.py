import sqlite3
from datetime import datetime

DB_PATH = "price_tracker.db"

def init_db():
    with sqlite3.connect(DB_PATH, timeout=10) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS price_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product TEXT NOT NULL,
                price REAL NOT NULL,
                timestamp TEXT NOT NULL
            )
        """)
        conn.commit()

def insert_price(product, price):
    timestamp = datetime.utcnow().isoformat()
    with sqlite3.connect(DB_PATH, timeout = 10) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO price_history (product, price, timestamp) VALUES (?, ?, ?)",
            (product, price, timestamp)
        )
        conn.commit()
 
def fetch_price_history(product, limit=10):
    with sqlite3.connect(DB_PATH, timeout = 10) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT price, timestamp FROM price_history WHERE product = ? ORDER BY timestamp DESC LIMIT ?",
            (product, limit)
        )
        rows = cursor.fetchall()
        return rows