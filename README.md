# Futures Trading Bot (Testnet)

A Python-based command-line interface (CLI) for trading on Binance Futures Testnet (USDT-M). This bot allows you to place Market, Limit, and Stop-Market orders, check balances, and logs all activities.

## Features
- **Place Orders**: Supports MARKET, LIMIT, and STOP_MARKET orders.
- **Order Validation**: Validates inputs before sending to the API.
- **Logging**: Detailed logs in `logs/trading_bot.log` and concise console output.
- **Account Info**: View wallet balance and unrealized PNL.
- **CLI**: Interactive CLI built with `typer` and `rich`.

## Project Structure
```
trading_bot/
  bot/
    __init__.py
    client.py        # Binance API wrapper
    orders.py        # Order logic and validation flow
    validators.py    # Input validation
    logging_config.py # Logging setup
  cli.py             # CLI Entry point
run_bot.py           # Main Entry point
run.bat              # Convenience script for Windows
requirements.txt     # Dependencies
README.md            # Documentation
.env                 # Environment variables (API Keys)
```

## Prerequisites
- Python 3.8+
- Binance Futures Testnet Account (https://testnet.binancefuture.com)
  - Get API Key and Secret from the testnet dashboard.

## Installation

1.  Clone the repository (if applicable) or unzip the folder.
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1.  Copy `.env.example` to `.env`:
    ```bash
    cp .env.example .env
    # On Windows: copy .env.example .env
    ```
2.  Edit `.env` and add your Binance Testnet API Key and Secret:
    ```
    BINANCE_API_KEY=your_key
    BINANCE_API_SECRET=your_secret
    ```

## Usage

You can run the bot using `run_bot.py` or the provided `run.bat` script.

### Main Help
```bash
python run_bot.py --help
# Or on Windows:
.\run.bat --help
```

### Place an Order (Interactive Mode)
If you run the command without arguments, it will prompt you for details:
```bash
python run_bot.py trade
```

### Place a MARKET Order
```bash
python run_bot.py trade --symbol BTCUSDT --side BUY --order-type MARKET --quantity 0.001
```

### Place a LIMIT Order
```bash
python run_bot.py trade --symbol BTCUSDT --side BUY --order-type LIMIT --quantity 0.001 --price 25000
```

### Place a STOP_MARKET Order 
```bash
python run_bot.py trade --symbol BTCUSDT --side SELL --order-type STOP_MARKET --quantity 0.001 --stop-price 24000
```

### Check Balance
```bash
python run_bot.py balance
```

## Logs
Logs are stored in `logs/trading_bot.log`. This file contains detailed request/response data and any errors.

## Assumptions
- The bot operates on USDT-M Futures.
- The user has sufficient margin in USDT on the testnet account.
- `STOP_MARKET` uses `stopPrice` as the trigger.

## Notes
- Ensure your API Key has Futures Trading permissions enabled (default on Testnet).

