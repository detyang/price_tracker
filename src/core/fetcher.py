# src/core/fetcher.py

import time
import requests
from bs4 import BeautifulSoup
from src.config import PRODUCT_LIST

import os


def parse_ippodo_price(soup):
    price_tag = soup.find("div", class_="p-product-meta__price-large")
    if price_tag:
        try:
            return float(price_tag.text.replace("¥", "").replace(",", "").strip())
        except ValueError:
            return None
    return None


def get_current_price(product_name):
    url = PRODUCT_LIST[product_name]
    if not url:
        print(f"[ERROR] Unknown product: {product_name}")
        return None
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"[ERROR] Failed to fetch {url}: {e}")
        return None
    
    soup = BeautifulSoup(response.content, "html.parser")

    if "ippodo-tea.co.jp" in url:
        return parse_ippodo_price(soup)
    else:
        return None