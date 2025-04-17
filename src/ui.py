# src/ui.py

import streamlit as st

def render_sidebar(product_list):
    st.sidebar.header("🔍 Track a Product")
    return st.sidebar.selectbox("Choose a product", list(product_list.keys()))