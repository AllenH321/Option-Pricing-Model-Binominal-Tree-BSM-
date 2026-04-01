from __future__ import annotations

import pandas as pd
import yfinance as yf


REQUIRED_PRICE_COLUMNS = ["date", "open", "high", "low", "close", "volume"]


def validate_ticker(ticker: str) -> bool:
    ticker = ticker.strip().upper()
    if not ticker:
        return False
    try:
        history = yf.Ticker(ticker).history(period="5d")
        return not history.empty
    except Exception:
        return False


def validate_price_data(df: pd.DataFrame) -> None:
    missing = [column for column in REQUIRED_PRICE_COLUMNS if column not in df.columns]
    if missing:
        raise ValueError(f"Price data is missing required columns: {missing}")
    if df.empty:
        raise ValueError("Price data is empty.")
