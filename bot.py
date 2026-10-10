import os
import requests

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

response = requests.post(
    url,
    json={
        "chat_id": CHAT_ID,
        "text": "🦉 Привет! Tender-Banki успешно подключён к Telegram."
    },
    timeout=20
)

response.raise_for_status()
print("Test message sent successfully")
