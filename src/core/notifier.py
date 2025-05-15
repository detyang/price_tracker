# src/core/notifier.py

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


try:
    import streamlit as st
    USE_STREAMLIT = True
except ImportError:
    USE_STREAMLIT = False

# Load local .env if not on Streamlit Cloud
if not USE_STREAMLIT:
    from dotenv import load_dotenv
    load_dotenv()


def get_email_credentials():
    if USE_STREAMLIT:
        sender_email = st.secrets.get("EMAIL_USER")
        sender_password = st.secrets.get("EMAIL_PASS")
    else:
        sender_email = os.getenv("EMAIL_USER")
        sender_password = os.getenv("EMAIL_PASS")

    if not sender_email or not sender_password:
        warning = "⚠️ Email credentials are not set. Email functionality will be disabled."
        if USE_STREAMLIT:
            st.warning(warning)
        else:
            print(f"[WARN] {warning}")
        return None, None

    return sender_email, sender_password


def send_price_alert(product_name, price, receiver_email, sender_email, sender_password, product_url):
    if not sender_email or not sender_password:
        print("[ERROR] Email credentials not provided.")
        return

    subject = f"[Price Alert] {product_name} dropped to ¥{price:,.0f}"
    body = f"""Hi there,

📢 Good news!

The product **{product_name}** is now priced at ¥{price:,.0f}.
🔗 View Product: {product_url}

-- Your Price Tracker Bot"""

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print(f"[INFO] Alert sent to {receiver_email}")
    except Exception as e:
        print(f"[ERROR] Failed to send alert: {e}")