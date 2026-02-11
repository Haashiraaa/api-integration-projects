

# telegram.py


"""Telegram Bot API client."""

import logging
from typing import Optional

import requests
from haashi_pkg.utility import Logger


class TelegramClient:
    """Client for sending messages via Telegram Bot API."""

    def __init__(
        self,
        TOKEN: str,
        CHAT_ID: str,
        logger: Optional[Logger] = None
    ) -> None:
        """
        Initialize Telegram client.

        Args:
            TOKEN: Telegram Bot Token from @BotFather
            CHAT_ID: Telegram Chat ID (user or group)
            logger: Optional Logger instance
        """
        self.url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        self.chat_id = CHAT_ID
        self.logger = logger or Logger(level=logging.INFO)

    def send(self, message: str) -> None:
        """
        Send message to Telegram chat.

        Args:
            message: Text message to send (supports Markdown)
        """
        try:
            self.logger.debug(
                f"Sending message to Telegram (chat_id: {self.chat_id})")

            response = requests.post(
                self.url,
                data={
                    "chat_id": self.chat_id,
                    "text": message,
                    "parse_mode": "Markdown"
                },
                timeout=10
            )

            response.raise_for_status()
            self.logger.debug("Message sent successfully")

        except requests.exceptions.RequestException as e:
            self.logger.error("Failed to send Telegram message")
            self.logger.error(exception=e, save_to_json=True)
            raise

