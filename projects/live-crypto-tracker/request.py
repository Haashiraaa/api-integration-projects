

# request.py

from requests import Session
from requests.exceptions import (
    ConnectionError, Timeout, TooManyRedirects
)
from datetime import datetime
from haashi_pkg.utility.utils import Utility
from typing import Any
from dataclasses import dataclass
import json
import os
import sys
import logging
import time


@dataclass
class RequestData:
    base_url: str
    endpoints: str
    api_key: str
    currency_code: str


def get_live_rates(data: dict[str, Any], curr_code: str) -> list[str]:

    if data["status"]["error_code"] != 0:
        print(f"\n\nError: {data['status']['error_message']}")
        sys.exit(1)

    if not data["data"]:
        print(f"\n\nError: No data found for {curr_code}")
        sys.exit(1)

    key = data['data']

    messages: list[str] = []

    for code in curr_code.strip().upper().split(","):
        name = key[code]['name']
        price = key[code]['quote']['USD']['price']
        raw_time = key[code]['quote']['USD']['last_updated']

        dt = datetime.strptime(raw_time, "%Y-%m-%dT%H:%M:%S.%fZ")
        readable_time = dt.strftime("%B %d, %Y — %I:%M %p")

        msg = (
            f"Name: {name}\n"
            f"Price: ${price:,.2f}\n"
            f"Last updated: {readable_time}"
        )

        messages.append(msg)

    return messages


def make_request(req: RequestData, max_retries: int = 3) -> dict[str, Any]:

    failed_requests = 0

    while failed_requests != max_retries:

        url: str = f'{req.base_url}{req.endpoints}'

        parameters: dict[str, str] = {
            'symbol': req.currency_code.upper(),
            'convert': 'USD'
        }

        headers: dict[str, str] = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': req.api_key,
        }

        try:
            session = Session()
            session.headers.update(headers)

            response = session.get(url, params=parameters)

            response.raise_for_status()

            data = json.loads(response.text)
            Utility(logging.INFO).debug(json.dumps(data, indent=4))

            return data

        except (ConnectionError, Timeout, TooManyRedirects, Exception) as e:
            print("\n\nOops! Something went wrong...")
            Utility(logging.INFO).debug(e)
            print("Retrying request...")
            failed_requests += 1
            time.sleep(failed_requests)

    print("\n\nRequest Failed!")
    sys.exit(1)
