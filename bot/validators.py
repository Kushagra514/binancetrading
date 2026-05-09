from bot.logging_config import get_logger

# Initialize a logger for this module
log = get_logger(__name__)

# Allowed values for order side
VALID_SIDES = {"BUY", "SELL"}

# Allowed values for order type
VALID_TYPES = {"MARKET", "LIMIT", "STOP"}  # STOP = stop-limit (bonus)

def validate(symbol: str, side: str, order_type: str, qty: float, price: float = None):
    # Ensure the trading symbol is provided (e.g., BTCUSDT)
    if not symbol:
        raise ValueError("Symbol cannot be empty")

    # Validate that side is either BUY or SELL (case-insensitive)
    if side.upper() not in VALID_SIDES:
        raise ValueError(f"Side must be BUY or SELL, got: {side}")

    # Validate that order type is one of MARKET, LIMIT, or STOP
    if order_type.upper() not in VALID_TYPES:
        raise ValueError(f"Order type must be MARKET/LIMIT/STOP, got: {order_type}")

    # Quantity must be positive (you can’t trade 0 or negative amounts)
    if qty <= 0:
        raise ValueError(f"Quantity must be > 0, got: {qty}")

    # For LIMIT and STOP orders, a price must be specified
    if order_type.upper() in {"LIMIT", "STOP"} and price is None:
        raise ValueError(f"Price is required for {order_type} orders")

    # If a price is provided, it must be positive
    if price is not None and price <= 0:
        raise ValueError(f"Price must be > 0, got: {price}")

    # If all checks pass, log the validated order details at DEBUG level
    log.debug(f"Validation passed | {symbol} {side} {order_type} qty={qty} price={price}")
