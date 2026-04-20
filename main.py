"""Simple stock portfolio tracker.

Tracks a small portfolio of stocks, fetches current prices using yfinance,
and calculates the total portfolio value.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

import yfinance as yf


@dataclass
class Holding:
    symbol: str
    shares: float


PORTFOLIO = [
    Holding("NVDA", 10),
    Holding("MSFT", 5),
    Holding("PLTR", 20),
    Holding("TSLA", 4),
]


def get_current_price(symbol: str) -> float:
    """Fetch the latest available market price for a stock symbol."""
    ticker = yf.Ticker(symbol)
    history = ticker.history(period="1d")

    if history.empty:
        fast_info = getattr(ticker, "fast_info", {})
        price = fast_info.get("lastPrice")
        if price is None:
            raise ValueError(f"Could not fetch price for {symbol}")
        return float(price)

    return float(history["Close"].iloc[-1])


def build_portfolio_snapshot() -> Dict[str, Dict[str, float]]:
    """Build a snapshot with price and position value for each holding."""
    snapshot: Dict[str, Dict[str, float]] = {}

    for holding in PORTFOLIO:
        price = get_current_price(holding.symbol)
        value = price * holding.shares
        snapshot[holding.symbol] = {
            "shares": holding.shares,
            "price": price,
            "value": value,
        }

    return snapshot


def print_portfolio(snapshot: Dict[str, Dict[str, float]]) -> None:
    """Print the portfolio in a simple table format."""
    print("Simple Stock Portfolio Tracker")
    print("-" * 50)
    print(f"{'Symbol':<10}{'Shares':<10}{'Price ($)':<15}{'Value ($)':<15}")
    print("-" * 50)

    total_value = 0.0
    for symbol, data in snapshot.items():
        total_value += data["value"]
        print(
            f"{symbol:<10}{data['shares']:<10.2f}{data['price']:<15.2f}{data['value']:<15.2f}"
        )

    print("-" * 50)
    print(f"Total Portfolio Value: ${total_value:,.2f}")


if __name__ == "__main__":
    portfolio_snapshot = build_portfolio_snapshot()
    print_portfolio(portfolio_snapshot)
