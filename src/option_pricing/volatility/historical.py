from __future__ import annotations

import math

import pandas as pd

from .returns import add_log_returns
from .transforms import annualize_volatility


def realized_volatility(df: pd.DataFrame, price_column: str = "adj_close", trading_days: int = 252) -> float:
    returns = add_log_returns(df, price_column=price_column)["log_return"].dropna()
    return annualize_volatility(returns.std(ddof=1), trading_days=trading_days)


def build_horizon_volatility_table(
    df: pd.DataFrame,
    ticker: str,
    price_column: str = "adj_close",
    horizons: range = range(1, 6),
    trading_days: int = 252,
) -> pd.DataFrame:
    annualized = realized_volatility(df, price_column=price_column, trading_days=trading_days)
    rows = []
    for horizon in horizons:
        sigma_h = annualized * math.sqrt(horizon / trading_days)
        rows.append(
            {
                "ticker": ticker.upper(),
                "model": "historical",
                "horizon_days": int(horizon),
                "sigma": float(sigma_h),
                "annualized_sigma": float(annualized),
            }
        )
    return pd.DataFrame(rows)
