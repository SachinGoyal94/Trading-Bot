from .client import BinanceClientWrapper
from .validators import validate_side, validate_order_type, validate_quantity, validate_price, validate_stop_price
import logging

logger = logging.getLogger("trading_bot.orders")

class OrderManager:
    """
    High-level order management.
    """
    def __init__(self, client: BinanceClientWrapper):
        self.client = client

    def place_order(self, symbol: str, side: str, order_type: str, quantity: float, price: float = None, stop_price: float = None):
        """
        Validates input and places an order via the client.
        """
        # Validate inputs
        s_side = validate_side(side)
        s_type = validate_order_type(order_type)
        s_qty = validate_quantity(quantity)
        s_price = validate_price(price, s_type)
        s_stop_price = validate_stop_price(stop_price, s_type)

        logger.info(f"Validator checks passed for {s_side} {s_type} {symbol}")

        # Place order via client
        return self.client.place_order(symbol, s_side, s_type, s_qty, s_price, s_stop_price)
    
    def get_account_summary(self):
        """
        Get a summary of account balances.
        """
        info = self.client.get_account_info()
        # Filter for non-zero balances or just return relevant info
        assets = info.get('assets', [])
        summary = [a for a in assets if float(a.get('walletBalance', 0)) > 0]
        return summary

