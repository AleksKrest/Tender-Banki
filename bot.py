import os
import time
import requests

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    response = requests.post(
        url,
        json={"chat_id": CHAT_ID, "text": text},
        timeout=20
    )
    response.raise_for_status()

send_message("🦉 Бот мониторинга банковских тендеров запущен!")

while True:
    time.sleep(180)

