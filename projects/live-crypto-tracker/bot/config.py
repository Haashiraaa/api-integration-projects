

# config.py


"""Credential configuration setup."""

import logging
from typing import Optional, Iterable

from haashi_pkg.utility import Logger, FileHandler, DateTimeUtil


def is_valid(user_responses: Iterable[str]) -> bool:
    """Check if all user inputs are non-empty."""
    return all(response.strip() for response in user_responses)


def configure_credentials(
    path: str = "user_data/credentials.json",
    logger: Optional[Logger] = None
) -> None:
    """
    Interactive setup for API credentials.

    Prompts user for:
    - CoinMarketCap API key
    - Telegram Bot Token
    - Telegram Chat ID

    Saves credentials to JSON file.
    """
    if logger is None:
        logger = Logger(level=logging.INFO)

    print("\n" + "=" * 60)
    logger.info("Credential Setup")
    logger.info("=" * 60)
    print("\nYou'll need:")
    logger.info("  1. CoinMarketCap API Key (from coinmarketcap.com/api)")
    logger.info("  2. Telegram Bot Token (from @BotFather)")
    logger.info("  3. Telegram Chat ID (from @userinfobot)")
    print()

    while True:
        # Get user input
        api_key = input("Enter your CMC API Key: ").strip()
        bot_token = input("Enter your Telegram Bot Token: ").strip()
        chat_id = input("Enter your Telegram Chat ID: ").strip()

        # Validate inputs
        if not is_valid([api_key, bot_token, chat_id]):
            logger.warning(
                "\n❌ All fields are required! Please try again.\n"
            )
            continue

        # Create credentials dict
        user_credentials = {
            "CMC_API_KEY": api_key,
            "Telegram_Bot_Token": bot_token,
            "Telegram_Chat_ID": chat_id,
            "": "",
            "Date created": DateTimeUtil.get_current_time(1, False)
        }

        # Save to file
        logger.debug(f"Saving credentials to {path}")
        file_handler = FileHandler(logger=logger)
        file_handler.save_json(data=user_credentials, path=path)

        logger.info("\n✓ Credentials saved successfully!")
        logger.info(f"Credentials saved to {path}")
        break

