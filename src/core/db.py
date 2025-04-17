import sqlite3
from datetime import datetime

DB_PATH = "price_tracker.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
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
    conn.close()

def insert_price(product, price):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    timestamp = datetime.utcnow().isoformat()
    cursor.execute(
        "INSERT INTO price_history (product, price, timestamp) VALUES (?, ?, ?)",
        (product, price, timestamp)
    )
    conn.commit()
    conn.close()

def fetch_price_history(product, limit=10):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT price, timestamp FROM price_history WHERE product = ? ORDER BY timestamp DESC LIMIT ?",
        (product, limit)
    )
    rows = cursor.fetchall()
    conn.close()
    return rows