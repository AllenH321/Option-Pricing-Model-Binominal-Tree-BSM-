from __future__ import annotations

from datetime import date, timedelta

import pandas as pd
import yfinance as yf

from .cleaning import clean_price_data
from .validation import validate_ticker


def download_price_data(
    ticker: str,
    start: str | date,
    end: str | date,
    auto_adjust: bool = False,
) -> pd.DataFrame:
    ticker = ticker.strip().upper()
    if not validate_ticker(ticker):
        raise ValueError(f"Ticker '{ticker}' is invalid or unavailable.")

    start_ts = pd.Timestamp(start)
    end_ts = pd.Timestamp(end)

    raw = yf.download(
        ticker,
        start=start_ts.strftime("%Y-%m-%d"),
        end=(end_ts + timedelta(days=1)).strftime("%Y-%m-%d"),
        auto_adjust=auto_adjust,
        progress=False,
        group_by="column",
    )

    if raw is None or raw.empty:
        raise RuntimeError(f"No price data returned for ticker '{ticker}'.")

    if isinstance(raw.columns, pd.MultiIndex):
        raw.columns = raw.columns.get_level_values(0)

    raw = raw.reset_index()
    return clean_price_data(raw)


def get_price_data(ticker: str, start: str | date, end: str | date) -> pd.DataFrame:
    return download_price_data(ticker=ticker, start=start, end=end)
