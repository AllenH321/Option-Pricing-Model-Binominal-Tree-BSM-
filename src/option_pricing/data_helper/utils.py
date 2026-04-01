from __future__ import annotations

from pathlib import Path
import re

import pandas as pd


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    clean = df.copy()
    clean.columns = [str(col).strip().lower().replace(" ", "_") for col in clean.columns]
    return clean


def ensure_datetime_column(df: pd.DataFrame, column: str = "date") -> pd.DataFrame:
    clean = df.copy()
    if column in clean.columns:
        clean[column] = pd.to_datetime(clean[column])
    return clean


def slugify_filename(text: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", text.strip())


def ensure_parent(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    return path
