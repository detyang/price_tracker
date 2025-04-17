# src/core/fetcher.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import requests
from bs4 import BeautifulSoup
from src.config import PRODUCT_LIST


def get_amazon_price_selenium(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get(url)

        # Wait up to 10 seconds for price element to be present
        price_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "a-offscreen"))
        )

        price_text = price_element.text.strip().replace("$", "").replace(",", "")
        if price_text:
            return float(price_text)
        else:
            print("Amazon price element found but text is empty")
            return None

    except Exception as e:
        print("Price not found:", e)
        return None

    finally:
        driver.quit()


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