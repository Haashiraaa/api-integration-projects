

# telegram.py


import requests


class TelegramClient:
    def __init__(self, TOKEN: str, CHAT_ID: str) -> None:
        self.url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        self.chat_id = CHAT_ID

    def send(self, message: str):
        requests.post(self.url, data={
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "Markdown"
        })
