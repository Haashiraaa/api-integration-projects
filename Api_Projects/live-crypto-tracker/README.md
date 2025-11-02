# Live Crypto Tracker

A small Python script that fetches live cryptocurrency rates from the Coinlayer API and prints them to the console every 2 minutes.

Key features
- Fetches rates for BTC, ETH, BNB, SOL, USDT (default)
- Prints human-readable live rates to stdout
- Saves the first successful API response to `crypto_data.json`
- Retries automatically on network failures

Requirements
- Python 3.8+
- See requirements.txt for third‑party dependencies

Installation
1. Clone the repository:
   git clone https://github.com/Haashiraaa/live-crypto-tracker.git
2. Install dependencies (recommended in a venv):
   pip install -r requirements.txt

Configuration
- The script currently contains an ACCESS_KEY constant in `get_crypto_rate.py`. Replace the value of `ACCESS_KEY` with your Coinlayer API key.
- Alternatively, you can modify the script to read the key from an environment variable (recommended for production).

Usage
- Run the script:
  python get_crypto_rate.py

- To stop the script press Ctrl+C.

Notes
- The script uses a 5-second HTTP timeout and waits 2 minutes between updates.
- The first successful API response is saved to `crypto_data.json`; subsequent runs will keep that file unless you remove it.

Contributing
- Small fixes and improvements are welcome — open issues or PRs on the repository.

License
- No license specified. Add a LICENSE file if you want to set one explicitly.