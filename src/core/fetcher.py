# src/core/fetcher.py

import requests
from bs4 import BeautifulSoup
from src.config import PRODUCT_LIST

def get_current_price(product_name):
    url = PRODUCT_LIST[product_name]
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "lxml")

    # NOTE: Amazon changes structure often — this is a placeholder
    price_tag = soup.select_one("span.a-price > span.a-offscreen")
    if price_tag:
        try:
            return float(price_tag.text.replace("$", "").replace(",", ""))
        except ValueError:
            pass
    return 0.0