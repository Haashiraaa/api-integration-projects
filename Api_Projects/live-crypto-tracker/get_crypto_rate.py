import requests
import json
import os
from pathlib import Path
from icecream import ic
import time
import sys

# Toggle debug mode for IceCream logging
DEBUG = False
if not DEBUG:
    ic.disable()
else:
    ic.enable()

# API access configuration
ACCESS_KEY = "1ea346481ac66ed542c958ade52afaaa"
CURRENCIES = "BTC,ETH,BNB,SOL,USDT"


def request_rate(access_key=ACCESS_KEY, currency=CURRENCIES):
    """
    Fetch live cryptocurrency rates from the Coinlayer API.

    Args:
        access_key (str): API access key for authentication.
        currency (str): Comma-separated list of currency symbols to fetch.

    Returns:
        dict | None: JSON data containing currency rates if successful,
        None if the request fails or times out.
    """
    try:
        base = "http://api.coinlayer.com/live"
        params = {"access_key": access_key, "symbols": currency}

        # Send GET request with a 5-second timeout
        r = requests.get(base, params=params, timeout=5)
        ic(f"Status code: {r.status_code}")

        # Raise an error if status code is not 200 (OK)
        r.raise_for_status()

        return r.json()

    except requests.exceptions.RequestException as e:
        ic(f"API Request Failed: {e}")
        return None


def save_json(arg):
    """
    Save the API response data to a JSON file if it doesn't already exist.

    Args:
        arg (dict): The cryptocurrency data to save.
    """
    path = Path("crypto_data.json")

    if not os.path.exists(path):
        # Serialize JSON data with indentation for readability
        file_content = json.dumps(arg, indent=4)
        path.write_text(file_content, encoding="UTF-8")
        print("Saved!")
    else:
        # Skip saving if the file already exists
        pass


def show_live_rates(arg):
    """
    Display live cryptocurrency rates in a readable format.

    Args:
        arg (dict): JSON response containing 'rates' data.
    """
    rates = arg["rates"]

    print("\nLive Crypto Rates (Updates every 2 minutes)")
    for crypto, price in rates.items():
        print(f"\nCryptocurrency: {crypto}\nPrice: ${price}")


def main():
    """
    Continuously fetch, display, and optionally save live crypto rates.
    Retries automatically if the API request fails.
    """
    while True:
        crypto_data = request_rate()

        if crypto_data is None:
            print("Failed to fetch crypto data. Retrying in 2 minutes...")
            time.sleep(120)
            continue

        save_json(arg=crypto_data)
        show_live_rates(arg=crypto_data)
        time.sleep(120)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram finished.")
        sys.exit()
