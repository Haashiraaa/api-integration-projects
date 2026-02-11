

# request.py

"""CoinMarketCap API request handler."""

import sys
import json
import time
import logging
from typing import Any, Optional
from datetime import datetime
from dataclasses import dataclass

from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from haashi_pkg.utility import Logger


@dataclass
class RequestData:
    """Configuration for API requests."""
    base_url: str
    endpoints: str
    api_key: str
    currency_code: str


def get_live_rates(
    data: dict[str, Any],
    curr_code: str,
    logger: Optional[Logger] = None
) -> list[str]:
    """
    Extract and format crypto prices from API response.

    Returns list of formatted messages, one per currency.
    """
    if logger is None:
        logger = Logger(level=logging.INFO)

    # Check for API errors
    if data["status"]["error_code"] != 0:
        error_msg = data["status"]["error_message"]
        logger.error(f"API error: {error_msg}")
        sys.exit(1)

    # Check if data exists
    if not data["data"]:
        logger.error(f"No data found for {curr_code}")
        sys.exit(1)

    key = data['data']
    messages = []

    for code in curr_code.strip().upper().split(","):
        logger.debug(f"Processing {code}")

        try:
            name = key[code]['name']
            price = key[code]['quote']['USD']['price']
            raw_time = key[code]['quote']['USD']['last_updated']

            # Format timestamp
            dt = datetime.strptime(raw_time, "%Y-%m-%dT%H:%M:%S.%fZ")
            readable_time = dt.strftime("%B %d, %Y — %I:%M %p")

            # Format message
            msg = (
                f"Name: {name}\n"
                f"Price: ${price:,.2f}\n"
                f"Last updated: {readable_time}"
            )

            messages.append(msg)
            logger.debug(f"✓ {code}: ${price:,.2f}")

        except KeyError:
            logger.error(f"Currency code '{code}' not found in API response")
            continue

    return messages


def make_request(
    req: RequestData,
    max_retries: int = 3,
    retry_delay: float = 7,
    logger: Optional[Logger] = None
) -> dict[str, Any]:
    """
    Make HTTP request to CoinMarketCap API with retry logic.

    Retries up to max_retries times with delay between attempts.
    """
    if logger is None:
        logger = Logger(level=logging.INFO)

    failed_attempts = 0

    while failed_attempts < max_retries:
        url = f'{req.base_url}{req.endpoints}'

        parameters = {
            'symbol': req.currency_code.upper(),
            'convert': 'USD'
        }

        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': req.api_key,
        }

        try:
            logger.debug(f"Making request to {url}")
            logger.debug(f"Parameters: {parameters}")

            session = Session()
            session.headers.update(headers)

            response = session.get(url, params=parameters)
            response.raise_for_status()

            data = json.loads(response.text)
            logger.debug("API response received successfully")

            return data

        except (ConnectionError, Timeout, TooManyRedirects) as e:
            failed_attempts += 1
            print()
            logger.error(
                f"Request failed (attempt {failed_attempts}/{max_retries})")
            # logger.debug(f"Error: {str(e)}")

            if failed_attempts < max_retries:
                logger.info(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                logger.error("Max retries exceeded")
                logger.error(exception=e, save_to_json=True)

        except Exception as e:
            failed_attempts += 1
            logger.error(
                f"Unexpected error (attempt {failed_attempts}/{max_retries})")
            logger.error(exception=e, save_to_json=True)

            if failed_attempts < max_retries:
                logger.info(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)

    logger.error("Request failed after all retry attempts")
    sys.exit(1)

