

# cli.py

"""Command-line interface argument parsing."""

import sys


def currency_codes() -> str:
    """
    Get currency codes from CLI arguments or return default.

    Usage:
        python bootstrap.py BTC,ETH,SOL
        python bootstrap.py -a BTC,ETH

    Returns default if no codes provided: BTC,ETH,BNB,SOL,XRP
    """
    default_codes = 'BTC,ETH,BNB,SOL,XRP'

    # Check CLI arguments (skip flags)
    for arg in sys.argv[1:]:
        if arg.startswith("-"):
            continue
        return arg.strip().upper()

    return default_codes


def auto_update() -> bool:
    """
    Check if auto-update mode is enabled.

    Usage:
        python bootstrap.py -a          # Auto-update enabled
        python bootstrap.py --auto      # Auto-update enabled
        python bootstrap.py             # Single run

    Returns True if -a or --auto flag is present.
    """
    return "-a" in sys.argv or "--auto" in sys.argv


def debug_mode() -> bool:
    """
    Check if debug mode is enabled.

    Usage:
        python bootstrap.py -d          # Debug mode enabled
        python bootstrap.py --debug     # Debug mode enabled
        python bootstrap.py             # Normal mode

    Returns True if -d or --debug flag is present.
    """
    return "-d" in sys.argv or "--debug" in sys.argv

