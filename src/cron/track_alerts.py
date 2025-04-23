# src/cron/track_alerts.py

import sys
import os

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import time
from dotenv import load_dotenv
load_dotenv()

from src.core.db import fetch_price_history, get_pending_alerts, mark_alert_triggered
from src.core.fetcher import get_current_price
from src.core.notifier import send_price_alert
from src.config import PRODUCT_LIST

SENDER_EMAIL = os.getenv("EMAIL_USER")
SENDER_PASS = os.getenv("EMAIL_PASS")

def check_alerts():
    alerts = get_pending_alerts()
    for alert in alerts:
        product, price_threshold, in_stock_required, email, alert_id = alert
        price, in_stock = get_current_price(product)
        product_url = PRODUCT_LIST.get(product)
        
        if price is None:
            continue

        if price <= price_threshold and (not in_stock_required or in_stock):
            send_price_alert(product, price, email, SENDER_EMAIL, SENDER_PASS, product_url)
            mark_alert_triggered(alert_id)


if __name__ == "__main__":
    check_alerts()