# smtp_test.py
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

load_dotenv()

sender = os.getenv("EMAIL_USER")
password = os.getenv("EMAIL_PASS")
receiver = "detyang22@gmail.com"
msg = MIMEText("This is a test message from Price Tracker.")
msg["Subject"] = "Test Email"
msg["From"] = sender
msg["To"] = receiver

try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.sendmail(sender, receiver, msg.as_string())
    print(f"[INFO] Sent test email from {sender} to {receiver}")
except Exception as e:
    print(f"[ERROR] SMTP failed: {e}")