import sys
import os

# Add parent directory to path so absolute imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import typer
from rich.console import Console
from rich.table import Table
from trading_bot.bot.client import BinanceClientWrapper
from trading_bot.bot.orders import OrderManager
from trading_bot.bot.logging_config import setup_logging
import logging

app = typer.Typer()
console = Console()

# Setup logging
setup_logging()
logger = logging.getLogger("trading_bot.cli")

def get_manager():
    try:
        client = BinanceClientWrapper()
        return OrderManager(client)
    except Exception as e:
        console.print(f"[bold red]Error initializing client:[/bold red] {e}")
        raise typer.Exit(code=1)

@app.command()
def trade(
    symbol: str = typer.Option(..., prompt="Symbol (e.g. BTCUSDT)"),
    side: str = typer.Option(..., prompt="Side (BUY/SELL)"),
    order_type: str = typer.Option(..., prompt="Order Type (MARKET/LIMIT/STOP_MARKET)"),
    quantity: float = typer.Option(..., prompt="Quantity"),
    price: float = typer.Option(None, help="Price for LIMIT orders"),
    stop_price: float = typer.Option(None, help="Stop Price for STOP orders"),
):
    """
    Place an order on Binance Futures Testnet.
    """
    manager = get_manager()
    try:
        # If type is LIMIT but price not provided, ask for it
        if order_type.upper() == "LIMIT" and price is None:
            price = typer.prompt("Price", type=float)
        
        if order_type.upper() in ["STOP_MARKET", "STOP"] and stop_price is None:
            stop_price = typer.prompt("Stop Price", type=float)

        console.print(f"[bold blue]Placing order...[/bold blue] {side} {symbol}")
        response = manager.place_order(symbol, side, order_type, quantity, price, stop_price)
        
        console.print("[bold green]Order Placed Successfully![/bold green]")
        
        # Print details nicely
        table = Table(title="Order Details")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="magenta")
        
        for k, v in response.items():
            table.add_row(str(k), str(v))
        
        console.print(table)

    except Exception as e:
        console.print(f"[bold red]Order Failed:[/bold red] {e}")
        logger.exception("Order failed")

@app.command()
def balance():
    """
    Show account balance.
    """
    manager = get_manager()
    try:
        summary = manager.get_account_summary()
        if not summary:
            console.print("[yellow]No positive balance found.[/yellow]")
            return

        table = Table(title="Account Balance")
        table.add_column("Asset", style="cyan")
        table.add_column("Wallet Balance", style="green")
        table.add_column("Unrealized PNL", style="red")

        for asset in summary:
            table.add_row(
                asset.get('asset'),
                str(asset.get('walletBalance')),
                str(asset.get('crossUnPnl'))
            )
        console.print(table)

    except Exception as e:
         console.print(f"[bold red]Failed to fetch balance:[/bold red] {e}")

if __name__ == "__main__":
    app()
