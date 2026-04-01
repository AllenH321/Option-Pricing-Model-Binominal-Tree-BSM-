from __future__ import annotations

import pandas as pd

from .returns import add_log_returns


def rolling_volatility(
    df: pd.DataFrame,
    window: int = 21,
    price_column: str = "adj_close",
    trading_days: int = 252,
) -> pd.DataFrame:
    result = add_log_returns(df, price_column=price_column)
    result["rolling_volatility"] = result["log_return"].rolling(window=window).std() * (trading_days ** 0.5)
    return result
