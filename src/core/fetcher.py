# src/core/fetcher.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import requests
from bs4 import BeautifulSoup
from src.config import PRODUCT_LIST


def get_amazon_price_selenium(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in background
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)

    # Give the page some time to load
    time.sleep(3)

    try:
        price_element = driver.find_element(By.CLASS_NAME, "a-offscreen")
        price = float(price_element.text.strip().replace("$", "").replace(",", ""))
    except Exception as e:
        print("Price not found:", e)
        price = None
    finally:
        driver.quit()
    return price


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
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    if "amazon.com" in url:
        return get_amazon_price_selenium(url)
    elif "ippodo-tea.co.jp" in url:
        return parse_ippodo_price(soup)
    else:
        return None