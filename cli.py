import os
import typer
from rich.console import Console
from rich.table import Table
from dotenv import load_dotenv
from bot.client import BinanceClient
from bot.validators import validate
from bot.orders import place_market, place_limit, place_stop_limit
from bot.logging_config import get_logger

load_dotenv()
log = get_logger(__name__)
app = typer.Typer()
console = Console()

def get_client() -> BinanceClient:
    api_key = os.getenv("API_KEY")
    secret = os.getenv("API_SECRET")
    if not api_key or not secret:
        raise EnvironmentError("API_KEY and API_SECRET must be set in .env")
    return BinanceClient(api_key, secret)

def print_response(response: dict):
    table = Table(title="Order Response", show_header=True, header_style="bold green")
    table.add_column("Field")
    table.add_column("Value")
    for k, v in response.items():
        table.add_row(str(k), str(v))
    console.print(table)

@app.command()
def place_order(
    symbol: str = typer.Option(..., help="e.g. BTCUSDT"),
    side: str = typer.Option(..., help="BUY or SELL"),
    order_type: str = typer.Option(..., "--order-type", help="MARKET / LIMIT / STOP"),
    qty: float = typer.Option(..., help="Quantity"),
    price: float = typer.Option(None, help="Required for LIMIT and STOP"),
):
    try:
        validate(symbol, side, order_type, qty, price)
        client = get_client()
        t = order_type.upper()
        if t == "MARKET":
            response = place_market(client, symbol, side, qty)
        elif t == "LIMIT":
            response = place_limit(client, symbol, side, qty, price)
        elif t == "STOP":
            response = place_stop_limit(client, symbol, side, qty, price)
        console.print("[bold green]Order placed successfully![/bold green]")
        print_response(response)
        log.info(f"Order success | response: {response}")
    except ValueError as e:
        console.print(f"[bold red]Validation Error:[/bold red] {e}")
        log.error(f"Validation error: {e}")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        log.error(f"Unexpected error: {e}")
        raise typer.Exit(1)

if __name__ == "__main__":
    app()
