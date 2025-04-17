from src.core.db import init_db, insert_price, fetch_price_history

# Initialize DB
init_db()

# After getting the price
insert_price(selected_product, price)

# Show price history (optional)
with st.expander("📊 Price History"):
    history = fetch_price_history(selected_product)
    for p, t in history:
        st.write(f"{t} → ${p:.2f}")
