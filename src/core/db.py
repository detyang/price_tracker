import os
import sqlite3
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "..", "price_tracker.db")  # adjust if needed


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

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product TEXT NOT NULL,
                price_threshold REAL NOT NULL,
                in_stock_required BOOLEAN,
                email TEXT NOT NULL,
                triggered BOOLEAN DEFAULT 0
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


def register_alert(product, price_threshold, in_stock_required, email):
    with sqlite3.connect(DB_PATH, timeout=10) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO alerts (product, price_threshold, in_stock_required, email) VALUES (?, ?, ?, ?)",
            (product, price_threshold, int(in_stock_required), email)
        )
        conn.commit()


def get_pending_alerts():
    with sqlite3.connect(DB_PATH, timeout=10) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT product, price_threshold, in_stock_required, email, id
            FROM alerts
            WHERE triggered = 0
        """)
        return cursor.fetchall()


def mark_alert_triggered(alert_id):
    with sqlite3.connect(DB_PATH, timeout=10) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE alerts SET triggered = 1 WHERE id = ?", (alert_id,))
        conn.commit()


def get_all_active_alerts():
    with sqlite3.connect(DB_PATH, timeout=10) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT product, price_threshold, in_stock_required, email
            FROM alerts
            WHERE triggered = 0
            ORDER BY product, price_threshold
        """)
        return cursor.fetchall()


def get_alerts_by_email(email):
    with sqlite3.connect(DB_PATH, timeout=10) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, product, price_threshold, in_stock_required
            FROM alerts
            WHERE email = ? AND triggered = 0
        """, (email,))
        return cursor.fetchall()


def delete_alert(alert_id):
    with sqlite3.connect(DB_PATH, timeout=10) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM alerts WHERE id = ?", (alert_id,))
        conn.commit()


def delete_all_alerts_by_email(email):
    with sqlite3.connect(DB_PATH, timeout=10) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM alerts WHERE email = ?", (email,))
        conn.commit()