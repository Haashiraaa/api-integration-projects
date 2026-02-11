

# bootstrap.py

"""Main bot orchestration - fetch crypto prices and send to Telegram."""

import sys
import logging
import time
from typing import Optional
from pathlib import Path

from haashi_pkg.utility import Logger, FileHandler
from request import RequestData, get_live_rates, make_request
from config import configure_credentials
from telegram import TelegramClient
from cli import currency_codes, auto_update, debug_mode


def load_storage(
    credentials_path: Path,
    logger: Optional[Logger] = None
) -> dict[str, str]:
    """Load credentials from JSON file."""
    if logger is None:
        logger = Logger(level=logging.INFO)

    try:
        logger.debug(f"Loading credentials from {credentials_path}")
        file_handler = FileHandler(logger=logger)
        return file_handler.read_json(path=credentials_path)

    except Exception as e:
        logger.error(f"Failed to load credentials from {credentials_path}")
        logger.error(exception=e, save_to_json=True)
        sys.exit(1)


def fetch_and_format_prices(
    req: RequestData,
    curr_code: str,
    logger: Optional[Logger] = None
) -> str:
    """Fetch live crypto prices and format for Telegram."""
    if logger is None:
        logger = Logger(level=logging.INFO)

    logger.debug(f"Fetching prices for {curr_code}")
    data = make_request(req, logger=logger)
    messages = get_live_rates(data, curr_code, logger=logger)

    output = "📊 Live Crypto Rates\n\n" + "\n\n".join(messages)
    return output


def bootstrap() -> None:
    """Run the crypto tracker bot."""

    # Initialize logger
    logger = Logger(level=logging.INFO)

    # Parse CLI arguments
    delay: float = float(300)
    if delay < 60:
        logger.warning("Delay is less than 60 seconds - setting to 60")
        delay = 60

    CURR_CODE = currency_codes()
    AUTO_UPDATE = auto_update()
    DEBUG = debug_mode()
    if DEBUG:
        logger = Logger(level=logging.DEBUG)

    logger.info("=" * 60)
    logger.info("Live Crypto Tracker Bot")
    logger.info("=" * 60)

    # Configuration
    ENDPOINTS = "/v1/cryptocurrency/quotes/latest"
    BASE_URL = "https://pro-api.coinmarketcap.com"
    CREDENTIALS_PATH = Path("user_data/credentials.json")

    logger.info(f"Currency codes: {CURR_CODE}")
    logger.info(f"Auto-update mode: {AUTO_UPDATE}")

    # Load or configure credentials
    if not CREDENTIALS_PATH.exists():
        logger.info("Credentials not found - starting setup...")
        configure_credentials(str(CREDENTIALS_PATH), logger=logger)

    storage = load_storage(CREDENTIALS_PATH, logger=logger)

    # Extract credentials
    API_KEY = storage.get("CMC_API_KEY")
    BOT_TOKEN = storage.get("Telegram_Bot_Token")
    CHAT_ID = storage.get("Telegram_Chat_ID")

    if not all([API_KEY, BOT_TOKEN, CHAT_ID]):
        raise ValueError(
            "Missing credentials in storage file! " +
            "Key, Token, Chat ID required."
        )

    logger.info("✓ Credentials loaded successfully")

    # Create request data object
    req = RequestData(
        base_url=BASE_URL,
        endpoints=ENDPOINTS,
        api_key=API_KEY,
        currency_code=CURR_CODE
    )

    # Initialize Telegram client
    telegram = TelegramClient(TOKEN=BOT_TOKEN, CHAT_ID=CHAT_ID, logger=logger)

    # Run bot
    if AUTO_UPDATE:

        formatted_delay = f"{delay / 60:.0f}"
        iteration = 0

        logger.info("\n" + "=" * 60)
        logger.info(
            f"Running in AUTO-UPDATE mode ({formatted_delay}-minute intervals))"
        )
        logger.info("Press Ctrl+C to stop")
        logger.info("=" * 60 + "\n")

        while True:
            iteration += 1
            logger.info(f"[Update #{iteration}] Fetching live rates...")

            try:
                output = fetch_and_format_prices(req, CURR_CODE, logger=logger)
                logger.debug(f"Formatted message:\n{output}")

                telegram.send(message=output)
                logger.info("✓ Message sent to Telegram")

                logger.info(
                    f"Waiting {formatted_delay} minutes for next update...\n")
                time.sleep(300)

            except Exception as e:
                logger.error("Failed to fetch/send update")
                logger.error(exception=e, save_to_json=True)
                logger.info("Retrying in 5 minutes...")
                time.sleep(300)

    else:
        logger.info("\nRunning in SINGLE-RUN mode")
        logger.info("Fetching live rates...")

        output = fetch_and_format_prices(req, CURR_CODE, logger=logger)
        logger.debug(f"Formatted message:\n{output}")

        telegram.send(message=output)
        logger.info("✓ Message sent to Telegram")
        logger.info("\nBot completed successfully")


def main() -> None:
    """Entry point with error handling."""
    try:
        bootstrap()

    except KeyboardInterrupt:
        print("\n\n✓ Bot stopped by user")
        sys.exit(0)

    except Exception as e:
        logger = Logger(level=logging.ERROR)
        logger.error("\nBot crashed:")
        logger.error(exception=e, save_to_json=True)
        sys.exit(1)


if __name__ == "__main__":
    main()

