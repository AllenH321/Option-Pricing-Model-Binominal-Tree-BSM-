from __future__ import annotations

import pandas as pd

from .utils import ensure_datetime_column, standardize_columns
from .validation import validate_price_data


def clean_price_data(df: pd.DataFrame) -> pd.DataFrame:
    clean = standardize_columns(df)
    clean = ensure_datetime_column(clean, "date")

    if "adj_close" not in clean.columns:
        for source in ["adjclose", "adjusted_close", "adj_close"]:
            if source in clean.columns:
                clean = clean.rename(columns={source: "adj_close"})
                break

    validate_price_data(clean)
    numeric_columns = [col for col in ["open", "high", "low", "close", "adj_close", "volume"] if col in clean.columns]
    for column in numeric_columns:
        clean[column] = pd.to_numeric(clean[column], errors="coerce")

    clean = clean.dropna(subset=["date", "close"]).sort_values("date").drop_duplicates(subset=["date"])
    return clean.reset_index(drop=True)
