# src/core/notifier.py

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")


def send_price_alert(product_name, price, receiver_email, sender_email, sender_password):
    if not sender_email or not sender_password:
        print("[ERROR] Email credentials not provided.")
        return

    subject = f"[Price Alert] {product_name} dropped to ¥{price:,.0f}"
    body = f"""\
        Hi there,

        📢 Good news!

        The product **{product_name}** is now priced at ¥{price:,.0f}.
        Visit your price tracker to view more details.

        -- Your Price Tracker Bot
    """

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