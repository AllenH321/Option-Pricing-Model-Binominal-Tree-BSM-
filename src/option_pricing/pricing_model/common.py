from __future__ import annotations

import numpy as np
import pandas as pd


def make_strike_grid(
    spot_price: float,
    offsets: tuple[int, ...] = (-2, -1, 0, 1, 2),
    step: float = 1.0,
    round_to: float = 0.01,
) -> np.ndarray:
    strikes = [max(spot_price + offset * step, round_to) for offset in offsets]
    strikes = [round(strike / round_to) * round_to for strike in strikes]
    return np.array(sorted(set(strikes)), dtype=float)


def build_pricing_inputs(
    ticker: str,
    spot_price: float,
    volatility_table: pd.DataFrame,
    risk_free_rate: float,
    horizons: range = range(1, 6),
    offsets: tuple[int, ...] = (-2, -1, 0, 1, 2),
    strike_step: float = 1.0,
) -> tuple[np.ndarray, pd.DataFrame]:
    strikes = make_strike_grid(spot_price, offsets=offsets, step=strike_step)
    subset = volatility_table[volatility_table["horizon_days"].isin(list(horizons))].copy()
    subset["ticker"] = ticker.upper()
    subset["spot_price"] = float(spot_price)
    subset["risk_free_rate"] = float(risk_free_rate)
    return strikes, subset.reset_index(drop=True)
