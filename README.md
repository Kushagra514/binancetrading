# Binance Futures Testnet Trading Bot

A CLI-based trading bot for Binance Futures Testnet (USDT-M) supporting Market, Limit, and Stop-Limit orders with structured logging and clean error handling.

---

## Project Structure
trading_bot/
├── bot/
│   ├── client.py          # Binance API wrapper (auth + HTTP)
│   ├── orders.py          # Order placement logic
│   ├── validators.py      # Input validation
│   └── logging_config.py  # Rotating file + console logger
├── cli.py                 # CLI entry point (Typer + Rich)
├── .env                   # API credentials (not committed)
├── requirements.txt
└── README.md

---

## Setup

**1. Clone the repo**
```bash
git clone https://github.com/Kushagra514/trading-bot
cd trading-bot
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Get Testnet credentials**
- Register at https://testnet.binancefuture.com
- Generate API Key + Secret from the dashboard

**4. Create `.env` file**
API_KEY=your_api_key_here
API_SECRET=your_secret_here

---

## How to Run

### Market Order
```bash
python cli.py place-order --symbol BTCUSDT --side BUY --type MARKET --qty 0.01
```

### Limit Order
```bash
python cli.py place-order --symbol BTCUSDT --side SELL --type LIMIT --qty 0.01 --price 50000
```

### Stop-Limit Order *(bonus)*
```bash
python cli.py place-order --symbol BTCUSDT --side SELL --type STOP --qty 0.01 --price 48000
```

---

## Output

Every successful order prints a Rich-formatted table:
Order placed successfully!
┌─────────────────┬───────────────┐
│ Field           │ Value         │
├─────────────────┼───────────────┤
│ orderId         │ 123456        │
│ status          │ FILLED        │
│ executedQty     │ 0.01          │
│ avgPrice        │ 49832.5       │
└─────────────────┴───────────────┘

---

## Logging

All activity is logged to `trading.log` (auto-rotates at 5MB, keeps 3 backups).
2024-01-15 10:23:11 | INFO     | orders | Placing MARKET order | BTCUSDT BUY qty=0.01
2024-01-15 10:23:12 | DEBUG    | client | Response: {'orderId': 123456, 'status': 'FILLED', ...}

Log files from a test run are included in the repo (`trading.log`).

---

## Assumptions

- Only USDT-M Futures (not COIN-M)
- Stop-Limit trigger price is set 1% below the limit price automatically
- Testnet only — not intended for live trading

---

## Requirements
typer[all]
rich
requests
python-dotenv

# binancetrading
