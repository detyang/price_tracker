# app.py

import streamlit as st
st.set_page_config(page_title="Price Tracker", layout="centered")
from src.config import PRODUCT_LIST
from src.ui import render_sidebar
from src.core.fetcher import get_current_price
from src.core.notifier import send_price_alert, get_email_credentials
SENDER_EMAIL, SENDER_PASS = get_email_credentials()
from src.core.db import init_db, insert_price, fetch_price_history

# Setup
st.title("🛒 Price Tracker")
init_db()

tab1, tab2, tab3 = st.tabs(["📈 Track Price", "🔕 Manage Alerts", "📋 Alert Status"])

with tab1:
    # Sidebar UI
    selected_product = render_sidebar(PRODUCT_LIST)

    # Fetch and display price
    price, in_stock = get_current_price(selected_product)
    if price is not None:
        st.metric(label="Current Price", value=f"¥{price:,.0f}")
        if in_stock:
            st.success("✅ In stock")
        else:
            st.warning("❌ Out of stock")
    else:
        st.error("Failed to fetch price.")

    insert_price(selected_product, price)

    st.subheader("🔔 Register Price Alert")
    with st.form("price_alert_form"):
        email = st.text_input("Your email address")
        alert_price = st.number_input("Alert me when price drops below", min_value=0.0, value=price or 0.0)
        in_stock_required = st.checkbox("Only notify me if in stock")
        submitted = st.form_submit_button("Register Alert")

    if submitted:
        from src.core.db import register_alert
        register_alert(selected_product, alert_price, in_stock_required, email)
        st.success("✅ Alert registered successfully!")

    threshold = st.number_input("Set price drop alert threshold", value=price)
    if price < threshold:
        send_price_alert(selected_product, price, email)
        st.success("✅ Alert triggered! Price is below your threshold.")

    with st.expander("📊 Price History"):
        history = fetch_price_history(selected_product)
        for p, t in history:
            st.write(f"{t} → ¥{p:,.0f}")

with tab2:
    st.subheader("🔕 Manage My Alerts")

    from src.core.db import get_alerts_by_email, delete_alert, delete_all_alerts_by_email

    with st.form("cancel_alerts_form"):
        user_email = st.text_input("Enter your email to view or cancel alerts")
        submitted = st.form_submit_button("Show My Alerts")

    if submitted and user_email:
        alerts = get_alerts_by_email(user_email)

        if not alerts:
            st.info("No active alerts found for this email.")
        else:
            for alert_id, product, threshold, in_stock in alerts:
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(f"- **{product}** under ¥{threshold:,.0f} {'(In stock only)' if in_stock else ''}")
                with col2:
                    if st.button("❌ Cancel", key=f"cancel_{alert_id}"):
                        delete_alert(alert_id)
                        st.success(f"Alert for {product} canceled.")

            if st.button("❌ Cancel All Alerts"):
                delete_all_alerts_by_email(user_email)
                st.success("All alerts for this email have been canceled.")

with tab3:
    st.subheader("📋 Current Active Alerts")

    from src.core.db import get_all_active_alerts
    active_alerts = get_all_active_alerts()

    if not active_alerts:
        st.info("No active alerts currently set.")
    else:
        # Optional: mask user email for privacy
        def mask_email(email):
            name, domain = email.split("@")
            return name[:2] + "***@" + domain

        import pandas as pd
        df = pd.DataFrame([
            {
                "Product": product,
                "Price Threshold": f"¥{threshold:,.0f}",
                "In Stock Only": "✅" if stock else "❌",
                "Tracking By": mask_email(email)
            }
            for product, threshold, stock, email in active_alerts
        ])
        st.dataframe(df, use_container_width=True)
