"""Streamlit dashboard for a simple stock portfolio tracker."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

import pandas as pd
import streamlit as st
import yfinance as yf


@dataclass
class Holding:
    symbol: str
    shares: float


PORTFOLIO: List[Holding] = [
    Holding("NVDA", 10),
    Holding("MSFT", 5),
    Holding("PLTR", 20),
    Holding("TSLA", 4),
]


@st.cache_data(ttl=300)
def get_current_price(symbol: str) -> float:
    ticker = yf.Ticker(symbol)
    history = ticker.history(period="1d")

    if history.empty:
        fast_info = getattr(ticker, "fast_info", {})
        price = fast_info.get("lastPrice")
        if price is None:
            raise ValueError(f"Could not fetch price for {symbol}")
        return float(price)

    return float(history["Close"].iloc[-1])


def build_portfolio_dataframe() -> pd.DataFrame:
    rows = []
    for holding in PORTFOLIO:
        price = get_current_price(holding.symbol)
        value = price * holding.shares
        rows.append(
            {
                "Symbol": holding.symbol,
                "Shares": holding.shares,
                "Price ($)": round(price, 2),
                "Value ($)": round(value, 2),
            }
        )
    return pd.DataFrame(rows)


def main() -> None:
    st.set_page_config(page_title="Portfolio Tracker", page_icon="📈", layout="wide")
    st.title("📈 Stock Portfolio Dashboard")
    st.caption("Tracks NVDA, MSFT, PLTR, and TSLA using live Yahoo Finance data.")

    if st.button("Refresh prices"):
        st.cache_data.clear()

    try:
        df = build_portfolio_dataframe()
    except Exception as exc:
        st.error(f"Could not load prices: {exc}")
        return

    total_value = float(df["Value ($)"].sum())

    c1, c2 = st.columns(2)
    c1.metric("Total Portfolio Value", f"${total_value:,.2f}")
    c2.metric("Number of Holdings", str(len(df)))

    st.dataframe(df, use_container_width=True, hide_index=True)

    st.subheader("Portfolio allocation")
    chart_df = df.set_index("Symbol")[["Value ($)"]]
    st.bar_chart(chart_df)


if __name__ == "__main__":
    main()
