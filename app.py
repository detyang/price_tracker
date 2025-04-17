# app.py

import streamlit as st
from src.config import PRODUCT_LIST
from src.ui import render_sidebar
from src.core.fetcher import get_current_price
from src.core.notifier import send_price_alert
from src.core.db import init_db, insert_price, fetch_price_history

# Setup
st.set_page_config(page_title="Price Tracker", layout="centered")
st.title("🛒 Price Tracker")
init_db()

# Sidebar UI
selected_product = render_sidebar(PRODUCT_LIST)

# Fetch and display price
price = get_current_price(selected_product)
st.metric(label="Current Price", value=f"${price:.2f}")

# Insert into DB
insert_price(selected_product, price)

# Alert logic
threshold = st.number_input("Set price drop alert threshold", value=price)
if price < threshold:
    send_price_alert(selected_product, price)
    st.success("✅ Alert triggered! Price is below your threshold.")

# Price history display
with st.expander("📊 Price History"):
    history = fetch_price_history(selected_product)
    for p, t in history:
        st.write(f"{t} → ${p:.2f}")