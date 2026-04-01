from __future__ import annotations

import numpy as np
import pandas as pd


def add_log_returns(df: pd.DataFrame, price_column: str = "adj_close") -> pd.DataFrame:
    if price_column not in df.columns:
        price_column = "close"
    if price_column not in df.columns:
        raise KeyError(f"Price column '{price_column}' was not found.")

    result = df.copy()
    result["log_return"] = np.log(result[price_column] / result[price_column].shift(1))
    return result
