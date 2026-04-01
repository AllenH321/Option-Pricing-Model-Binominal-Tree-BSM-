from __future__ import annotations

from pathlib import Path

import pandas as pd

from .utils import ensure_parent, slugify_filename


def save_csv(df: pd.DataFrame, path: str | Path) -> Path:
    output_path = ensure_parent(Path(path))
    df.to_csv(output_path, index=False)
    return output_path


def remove_existing_files(directory: str | Path, pattern: str | list[str] | tuple[str, ...]) -> list[Path]:
    target_dir = Path(directory)
    if not target_dir.exists():
        return []

    patterns = [pattern] if isinstance(pattern, str) else list(pattern)
    removed: list[Path] = []
    seen: set[Path] = set()
    for current_pattern in patterns:
        for path in target_dir.glob(current_pattern):
            if path.is_file() and path not in seen:
                path.unlink()
                removed.append(path)
                seen.add(path)
    return removed


def load_csv(path: str | Path) -> pd.DataFrame:
    return pd.read_csv(Path(path))


def build_price_filename(ticker: str, start: str, end: str, provider: str = "yfinance") -> str:
    return slugify_filename(f"{ticker.upper()}_{provider}_daily_{start}_{end}.csv")
