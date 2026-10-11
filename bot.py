import os
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone
from urllib.parse import quote

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

BANK_WORDS = [
    "сбербанк", "сбер", "втб", "альфа-банк",
    "тинькофф", "т-банк", "газпромбанк",
    "россельхозбанк", "совкомбанк",
    "промсвязьбанк", "псб", "мкб",
    "райффайзенбанк", "банк"
]

PRODUCT_WORDS = [
    "футболк", "поло", "худи", "толстовк",
    "свитшот", "куртк", "жилет",
    "униформ", "спецодежд", "одежд",
    "рюкзак", "сумк", "зонт",
    "мерч", "сувенир", "брендирован",
    "логотип", "вышивк"
]

SEARCH_WORDS = [
    "футболки",
    "худи",
    "поло",
    "брендированная одежда",
    "рюкзаки",
    "мерч"
]


def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    response = requests.post(
        url,
        json={
            "chat_id": CHAT_ID,
            "text": text[:4000]
        },
        timeout=30
    )

    response.raise_for_status()


def download_page(url):
    response = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0"
        },
        timeout=30
    )

    response.raise_for_status()

    return BeautifulSoup(
        response.text,
        "html.parser"
    )


def find_matches():
    results = []

    for word in SEARCH_WORDS:
        url = (
            "https://zakupki.gov.ru/epz/order/extendedsearch/results.html"
            "?searchString=" + quote(word)
        )

        try:
            soup = download_page(url)

            cards = soup.select(
                ".search-registry-entry-block"
            )

            for card in cards:
                text = card.get_text(
                    " ", strip=True
                ).lower()

                has_bank = any(
                    x in text for x in BANK_WORDS
                )

                has_product = any(
                    x in text for x in PRODUCT_WORDS
                )

                if not (has_bank and has_product):
                    continue

                link = card.find(
                    "a", href=True
                )

                if not link:
                    continue

                href = link["href"]

                if href.startswith("/"):
                    href = (
                        "https://zakupki.gov.ru"
                        + href
                    )

                results.append(
                    (text[:250], href)
                )

        except requests.RequestException as error:
            print(
                "Ошибка поиска:",
                word,
                error
            )

    return list(dict.fromkeys(results))


def main():
    print("Запуск проверки закупок")

    results = find_matches()

    if not results:
        send_message(
            "🦉 Проверка завершена.\n\n"
            "Подходящих записей не обнаружено "
            "или сайт не предоставил результаты "
            "автоматическому поиску.\n\n"
            "Это не означает, что тендеров нет."
        )
        return

    send_message(
        "🦉 Найдены предварительные "
        f"совпадения: {len(results)}.\n"
        "Проверь заказчика и срок подачи "
        "заявок по каждой ссылке."
    )

    for description, link in results[:10]:
        send_message(
            "Возможная закупка:\n\n"
            f"{description}\n\n{link}"
        )


if __name__ == "__main__":
    main()
