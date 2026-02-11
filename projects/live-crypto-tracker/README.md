# Live Crypto Price Tracker 📊

**Real-time cryptocurrency price monitoring with Telegram notifications**

A production-grade crypto price tracker that fetches live cryptocurrency prices from CoinMarketCap and sends formatted updates to your Telegram. Features CLI interface, auto-update mode, and secure credential management.

---

## What This Does

-  Fetches live cryptocurrency prices from CoinMarketCap API
-  Sends formatted price updates to your Telegram
-  Supports custom crypto selections via CLI
-  Auto-update mode (sends updates every 5 minutes)
-  Secure credential storage (no hardcoded API keys)
-  Error handling with automatic retries
-  Professional formatting with emojis and timestamps

---

## Example Output

Your Telegram will receive messages like this:

```
📊Live Crypto Rates

Name: Bitcoin
Price: $77,160.97
Last updated: February 01, 2026 — 02:23 PM

Name: Ethereum
Price: $2,367.46
Last updated: February 01, 2026 — 02:23 PM

Name: BNB
Price: $760.79
Last updated: February 01, 2026 — 02:23 PM
```

---

## Quick Start

### Prerequisites

- Python 3.x
- CoinMarketCap API key (free tier: 10,000 calls/month)
- Telegram Bot Token and Chat ID
- [haashi_pkg](https://github.com/Haashiraaa/my-packages) (custom utility package)

### Installation

```bash
# Clone the repository
git clone https://github.com/Haashiraaa/api-integration-projects.git
cd api-integration-projects/projects/live-crypto-tracker

# Install haashi_pkg (custom package)
pip install git+https://github.com/Haashiraaa/my-packages.git

# Install dependencies
pip install -r requirements.txt
```

---

## Setup Guide

### Step 1: Get CoinMarketCap API Key

1. Go to https://coinmarketcap.com/api/
2. Click "Get Your Free API Key Now"
3. Sign up for a free account
4. Copy your API key from the dashboard

**⚠️ IMPORTANT:** Never commit your API key to GitHub or share it publicly!

---

### Step 2: Create Telegram Bot

**Quick Setup (1 minute):**

1. Open Telegram and search for `@BotFather`
2. Start the bot and send: `/newbot`
3. Choose a name (e.g., "MyCryptoBot")
4. Choose a username ending in `bot` (e.g., "my_crypto_alert_bot")
5. **Copy the Bot Token** you receive (looks like `123456789:AAHsdjskdlsjdksjdsjdksjds`)

**⚠️ SECURITY WARNING:** Treat your bot token like a password. Never share it or commit it to version control!

---

### Step 3: Get Your Telegram Chat ID

**Easy Method:**

1. In Telegram, search for `@userinfobot`
2. Start the bot
3. It will reply with your **Chat ID** (e.g., `987654321`)

**For Group Chats:**
- Add your bot to the group
- Search for `@RawDataBot` and add it to the group
- It will show the group's Chat ID (negative number like `-1001234567890`)

---

### Step 4: First Run (Credential Setup)

Run the script for the first time:

```bash
cd bot/
python bootstrap.py
```

The script will prompt you to enter:
- **CMC API Key** (from Step 1)
- **Telegram Bot Token** (from Step 2)
- **Telegram Chat ID** (from Step 3)

These credentials are saved securely in `user_data/credentials.json` and will be loaded automatically on future runs.

**⚠️ SECURITY:** The `user_data/` folder should be in your `.gitignore` to prevent credential exposure!

---

## Usage

### Basic Usage (Default Cryptos)

```bash
python bootstrap.py
```

Tracks default cryptocurrencies: **BTC, ETH, BNB, SOL, XRP**

---

### Custom Cryptocurrencies

```bash
python bootstrap.py BTC,ETH,DOGE
```

Track any cryptos you want (comma-separated, no spaces)

**Supported Cryptocurrencies:**
- Bitcoin (BTC)
- Ethereum (ETH)
- Binance Coin (BNB)
- Solana (SOL)
- XRP (XRP)
- Cardano (ADA)
- Dogecoin (DOGE)
- And 2.4M+ other cryptos supported by CoinMarketCap

**⚠️ Note:** Only use cryptocurrency symbols, NOT fiat currencies (e.g., use BTC, not USD or NGN)

---

### Auto-Update Mode

```bash
python bootstrap.py -a
# or
python bootstrap.py --auto
```

Runs in background mode and sends updates **every 5 minutes**.

Press `Ctrl+C` to stop.

---

### Combine Options

```bash
# Track BTC and ETH with auto-updates
python bootstrap.py BTC,ETH -a

# Track top 5 cryptos with auto-updates
python bootstrap.py BTC,ETH,BNB,SOL,XRP --auto
```

---

## Project Structure

```
live-crypto-tracker/
├── bootstrap.py          # Main application entry point
├── cli.py                # Command-line argument parsing
├── config.py             # Credential setup and management
├── request.py            # CoinMarketCap API integration
├── telegram.py           # Telegram bot client
├── requirements.txt      # Python dependencies
├── user_data/
│   └── credentials.json  # Stored credentials (auto-created)
└── README.md
```

---

## Tech Stack

- **Python 3.x** - Core language
- **requests** - HTTP requests for API calls
- **CoinMarketCap API** - Cryptocurrency price data
- **Telegram Bot API** - Message delivery
- **[haashi_pkg](https://github.com/Haashiraaa/my-packages)** - Custom utility toolkit

---

## What This Demonstrates

### API Integration Skills
- Multi-API integration (CoinMarketCap + Telegram)
- Secure authentication handling
- HTTP request management with retry logic
- Error handling for network failures
- Rate limiting awareness (10K calls/month free tier)

### Backend Development
- CLI argument parsing
- Configuration management
- Credential storage (JSON)
- Background service implementation
- Auto-update loop with proper exit handling

### Data Processing
- JSON data parsing
- Datetime formatting
- Data validation
- Error handling for missing/malformed data

### Software Engineering
- Modular architecture (separation of concerns)
- Dataclass usage for type safety
- Clean code organization
- Production-ready error handling
- User-friendly output formatting

---

## 🔒 Security Best Practices

### DO 
- Store credentials in `user_data/credentials.json` (gitignored)
- Use environment variables for sensitive data
- Keep your API keys private
- Regularly rotate your bot token if exposed

### DON'T 
- Hardcode API keys in your code
- Commit `user_data/` folder to Git
- Share your bot token publicly
- Push credentials to GitHub

**Add to `.gitignore`:**
```
user_data/
*.json
__pycache__/
*.pyc
```

---

## Configuration

### Changing Update Frequency

Edit line 64 in `bootstrap.py`:

```python
time.sleep(300)  # 300 seconds = 5 minutes
```

Change `300` to your desired interval (in seconds):
- `60` = 1 minute
- `300` = 5 minutes (default)
- `600` = 10 minutes
- `3600` = 1 hour

**⚠️ Warning:** CoinMarketCap free tier has a limit of 10,000 calls/month (~333/day). Don't set updates too frequently!

---

## Troubleshooting

### "Credentials not found!"
**Solution:** Run the script once to configure credentials. The prompt will guide you.

### "Error: No data found for [CRYPTO]"
**Solution:** You might be using:
- Invalid crypto symbol (check spelling)
- Fiat currency instead of crypto (use BTC, not USD/NGN)

### "Request Failed!"
**Solutions:**
- Check your internet connection
- Verify your CoinMarketCap API key is valid
- Check if you exceeded API rate limits (10K/month)

### "Telegram message not received"
**Solutions:**
- Verify your bot token and chat ID are correct
- Make sure you started your bot in Telegram (@YourBotName)
- Check if bot has permission to send messages

---

## Use Cases

This project structure can be adapted for:
- Stock price monitoring
- Forex rate tracking
- Server monitoring with Telegram alerts
- Scheduled report delivery
- IoT sensor data notifications
- Any automated notification system

**The pattern is universal: Fetch data → Process → Notify**

---

## Future Enhancements

Potential additions (not required, but possible):
- [ ] Price alerts (notify when BTC hits $X)
- [ ] Portfolio tracking (track investment value)
- [ ] Historical price comparison
- [ ] Chart generation and image sending
- [ ] Multiple notification channels (Email, Discord, Slack)
- [ ] Web dashboard interface

---

## API Credits & Limits

**CoinMarketCap Free Tier:**
- 10,000 API calls per month (~333 per day)
- Updates every 5 minutes = 288 calls/day
- Approximately 34 days of continuous auto-updates

**Monitor your usage** at https://pro.coinmarketcap.com/account

---

## Contributing

This is a personal portfolio project, but feedback and suggestions are welcome!

---

## License

This project is for portfolio and educational purposes.

---

## ⚠️ Disclaimer

This tool is for informational purposes only. Cryptocurrency prices are volatile and this tool does not provide financial advice. Always do your own research before making investment decisions.

---

**Built as a portfolio project demonstrating API integration, backend service development, and production-quality code.**

---

## Acknowledgments

- **CoinMarketCap** - For providing free cryptocurrency data API
- **Telegram** - For simple and powerful bot API
- **Python Community** - For excellent libraries and tools
