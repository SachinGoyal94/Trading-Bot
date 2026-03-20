import sys
import os

# Ensure the current directory is in sys.path so we can import trading_bot
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from trading_bot.cli import app

if __name__ == "__main__":
    app()

