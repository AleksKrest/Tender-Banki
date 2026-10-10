import os
import re
import requests
from bs4 import BeautifulSoup

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

KEYWORDS = [
    "мерч",
    "футболки",
    "поло",
    "худи",
    "толстовки",
    "одежда",
    "рюкзаки",
    "сумки",
    "зонты",
    "сувенирная продукция",
]

BANKS = [
    "сбер",
    "втб",
    "альфа-банк",
    "газпромбанк",
    "тинькофф",
    "т-банк",
    "совкомбанк",
    "псб",
    "росбанк",
    "райффайзенбанк",
    "мкб",
    "банк",
]

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    response = requests.post(
        url,
        json={"chat_id": CHAT_ID, "text": text},
        timeout=20,
    )
    response.raise_for_status()

def def check_page(url):
    response = requests.get(
        url,
        timeout=20,
        headers={"User-Agent": "Mozilla/5.0"},
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text(" ", strip=True).lower()

    has_bank = any(word in text for word in BANKS)
    has_product = any(word in text for word in KEYWORDS)

    return has_bank and has_product

def def main():
    send_message(
        "🦉 Tender-Banki: проверка программы выполнена. "
        "Подключение Telegram работает."
    )

if if __name__ == "__main__":
    main()
