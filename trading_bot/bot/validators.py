from typing import Optional

def validate_side(side: str) -> str:
    """
    Validates order side (BUY/SELL).
    Returns uppercase side or raises ValueError.
    """
    if not side:
        raise ValueError("Side cannot be empty.")
    s = side.upper()
    if s not in ["BUY", "SELL"]:
        raise ValueError(f"Invalid side: {side}. Must be BUY or SELL.")
    return s

def validate_order_type(order_type: str) -> str:
    """
    Validates order type (MARKET/LIMIT).
    Returns uppercase type or raises ValueError.
    """
    if not order_type:
        raise ValueError("Order type cannot be empty.")
    ot = order_type.upper()
    if ot not in ["MARKET", "LIMIT", "STOP_MARKET", "STOP"]:
        raise ValueError(f"Invalid order type: {order_type}. Must be MARKET, LIMIT, or STOP_MARKET.")
    return ot

def validate_quantity(quantity: float) -> float:
    """
    Validates quantity is positive.
    """
    if quantity <= 0:
        raise ValueError(f"Quantity must be greater than 0. Got {quantity}.")
    return quantity

def validate_price(price: Optional[float], order_type: str) -> Optional[float]:
    """
    Validates price for LIMIT orders.
    """
    if order_type.upper() == "LIMIT":
        if price is None or price <= 0:
            raise ValueError("Price must be greater than 0 for LIMIT orders.")
    return price

def validate_stop_price(stop_price: Optional[float], order_type: str) -> Optional[float]:
    """
    Validates stop price for STOP_MARKET orders.
    """
    if order_type.upper() in ["STOP_MARKET", "STOP", "TAKE_PROFIT_MARKET"]:
        if stop_price is None or stop_price <= 0:
            raise ValueError(f"Stop Price must be greater than 0 for {order_type} orders.")
    return stop_price
