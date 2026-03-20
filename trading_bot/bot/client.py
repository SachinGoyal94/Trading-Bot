import os
import logging
from binance.client import Client
# from binance.error import ClientError
from binance.exceptions import BinanceAPIException
from dotenv import load_dotenv

load_dotenv()

class BinanceClientWrapper:
    def __init__(self, api_key: str = None, api_secret: str = None, testnet: bool = True):
        self.logger = logging.getLogger("trading_bot.client")
        
        # If not provided, try to load from environment
        self.api_key = api_key or os.getenv("BINANCE_API_KEY")
        self.api_secret = api_secret or os.getenv("BINANCE_API_SECRET")
        self.testnet = testnet

        if not self.api_key or not self.api_secret:
            self.logger.warning("API Key or Secret missing. Operations will fail unless provided.")

        try:
            # Initialize the client for Futures Testnet
            # python-binance supports testnet=True for futures
            self.client = Client(self.api_key, self.api_secret, testnet=self.testnet)
            self.logger.info(f"Initialized Binance Client (Testnet={self.testnet})")
        except Exception as e:
            self.logger.error(f"Failed to initialize Binance Client: {e}")
            raise e

    def place_order(self, symbol: str, side: str, order_type: str, quantity: float, price: float = None, stop_price: float = None):
        """
        Places an order on Binance Futures.
        Supports MARKET, LIMIT, STOP_MARKET.
        """
        try:
            order_params = {
                'symbol': symbol,
                # side should be uppercase
                'side': side.upper(),
                'type': order_type.upper(),
                'quantity': quantity,
            }

            ot = order_type.upper()
            if ot == 'LIMIT':
                if price is None:
                    raise ValueError("Price is required for LIMIT orders.")
                order_params['price'] = price
                order_params['timeInForce'] = 'GTC'
            
            elif ot == 'STOP_MARKET':
                if stop_price is None:
                    raise ValueError("Stop Price is required for STOP_MARKET orders.")
                order_params['stopPrice'] = stop_price
                # For STOP_MARKET, usually you do not need timeInForce for the trigger, 
                # but might need reduceOnly or other params. We'll keep it simple.
            
            self.logger.info(f"Sending order: {order_params}")
            
            # Using futures_create_order from python-binance
            response = self.client.futures_create_order(**order_params)
            
            self.logger.info(f"Order success: {response}")
            return response

        except BinanceAPIException as e:
            self.logger.error(f"Binance API Exception: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error placing order: {e}")
            raise

    def get_account_info(self):
        """
        Fetch futures account information.
        """
        try:
            return self.client.futures_account()
        except BinanceAPIException as e:
            self.logger.error(f"Error fetching account info: {e}")
            raise
