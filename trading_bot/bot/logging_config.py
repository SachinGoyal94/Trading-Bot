import logging
import os
from logging.handlers import RotatingFileHandler
from rich.logging import RichHandler

def setup_logging(log_file="trading_bot.log", verbose=False):
    """
    Sets up logging configuration.
    Logs to a file and to the console.
    """
    # Create a custom logger
    logger = logging.getLogger("trading_bot")
    logger.setLevel(logging.DEBUG)  # Capture everything

    # Create handlers
    
    # File Handler - detailed logs
    if not os.path.exists("logs"):
        os.makedirs("logs")
    
    file_path = os.path.join("logs", log_file)
    file_handler = RotatingFileHandler(file_path, maxBytes=5*1024*1024, backupCount=5)
    file_handler.setLevel(logging.DEBUG)
    
    # Console Handler - cleaner output
    console_handler = RichHandler(rich_tracebacks=True)
    console_handler.setLevel(logging.INFO if not verbose else logging.DEBUG)

    # Create formatters and add it to handlers
    file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_format)
    
    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # Also capture python-binance logs to file
    binance_logger = logging.getLogger("binance")
    binance_logger.setLevel(logging.DEBUG)
    binance_logger.addHandler(file_handler)

    return logger

