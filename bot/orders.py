from bot.client import BinanceClient
from bot.logging_config import get_logger

# Initialize a logger for this module
log = get_logger(__name__)

# Binance Futures endpoint for creating orders
ENDPOINT = "/fapi/v1/order"

def place_market(client: BinanceClient, symbol: str, side: str, qty: float) -> dict:
    # Parameters for a MARKET order (executes immediately at best available price)
    params = {
        "symbol": symbol.upper(),   # Trading pair, e.g., BTCUSDT
        "side": side.upper(),       # BUY or SELL
        "type": "MARKET",           # Order type
        "quantity": qty,            # Amount to trade
    }
    # Log the order attempt at INFO level
    log.info(f"Placing MARKET order | {symbol} {side} qty={qty}")
    # Send the signed request via BinanceClient
    return client.post(ENDPOINT, params)


def place_limit(client: BinanceClient, symbol: str, side: str, qty: float, price: float) -> dict:
    # Parameters for a LIMIT order (executes only at the specified price or better)
    params = {
        "symbol": symbol.upper(),
        "side": side.upper(),
        "type": "LIMIT",
        "quantity": qty,
        "price": price,             # Limit price
        "timeInForce": "GTC",       # Good Till Cancelled — order stays open until filled/cancelled
    }
    log.info(f"Placing LIMIT order | {symbol} {side} qty={qty} price={price}")
    return client.post(ENDPOINT, params)


def place_stop_limit(client: BinanceClient, symbol: str, side: str, qty: float, price: float) -> dict:
    # Parameters for a STOP-LIMIT order (triggered when stopPrice is reached)
    params = {
        "symbol": symbol.upper(),
        "side": side.upper(),
        "type": "STOP",
        "quantity": qty,
        "price": price,             # Limit price — order executes at this price once triggered
        "stopPrice": round(price * 0.99, 2),  # Trigger price — here set 1% below limit
        "timeInForce": "GTC",
    }
    log.info(f"Placing STOP-LIMIT order | {symbol} {side} qty={qty} price={price}")
    return client.post(ENDPOINT, params)
