

# cli.py

import sys


def currency_codes() -> str:

    default_codes: str = 'BTC,ETH,BNB,SOL,XRP'  # default currency codes

    # try to get currency codes from command line arguments
    for arg in sys.argv[1:]:
        if arg.startswith("-"):
            continue
        return arg.strip().upper()

    return default_codes


def auto_update() -> bool:

    return "-a" in sys.argv or "--auto" in sys.argv
