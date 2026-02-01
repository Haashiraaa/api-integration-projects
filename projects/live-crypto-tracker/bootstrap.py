

# bootstrap.py

import sys
import logging
import time
from request import RequestData, get_live_rates, make_request
from config import configure_credentials
from haashi_pkg.utility.utils import Utility
from pathlib import Path
from telegram import TelegramClient
from cli import currency_codes, auto_update


def load_storage(credentials_path: Path) -> dict[str, str]:
    try:
        return Utility().read_json(path=credentials_path)
    except Exception as e:
        print(f"Oops! File missing or corrupted: {credentials_path}")
        Utility(logging.INFO).debug(e)
        sys.exit(1)


def bootstrap() -> None:

    ENDPOINTS: str = "/v1/cryptocurrency/quotes/latest"
    BASE_URL = "https://pro-api.coinmarketcap.com"
    CREDENTIALS_PATH: Path = Path("user_data/credentials.json")
    CURR_CODE: str = currency_codes()
    AUTO_UPDATE: bool = auto_update()

    if not CREDENTIALS_PATH.exists():
        configure_credentials(str(CREDENTIALS_PATH))
    storage = load_storage(CREDENTIALS_PATH)

    API_KEY = storage.get("CMC_API_KEY")
    BOT_TK = storage.get("Telegram_Bot_Token")
    CHAT_ID = storage.get("Telegram_Chat_ID")

    assert API_KEY and BOT_TK and CHAT_ID, "Credentials not found!"

    req = RequestData(
        base_url=BASE_URL,
        endpoints=ENDPOINTS,
        api_key=API_KEY,
        currency_code=CURR_CODE
    )

    data = make_request(req)
    messages = get_live_rates(data, CURR_CODE)
    output = "📊Live Crypto Rates\n\n" + "\n\n".join(messages)

    Utility(logging.INFO).debug(output)

    # Recieve Notification from Telegram

    if AUTO_UPDATE:
        print("\n\nServer is running in background mode.")
        print("Press Ctrl+C to stop.")
        while True:
            TelegramClient(TOKEN=BOT_TK, CHAT_ID=CHAT_ID).send(
                message=output)
            time.sleep(300)

    TelegramClient(TOKEN=BOT_TK, CHAT_ID=CHAT_ID).send(message=output)


if __name__ == "__main__":
    try:
        bootstrap()
    except KeyboardInterrupt:
        print("\n\nExiting...")
        sys.exit(0)
    except Exception as e:
        print("\n\nOops! Something went wrong...")
        Utility(logging.INFO).debug(e)
        sys.exit(1)
