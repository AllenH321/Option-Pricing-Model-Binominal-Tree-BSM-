from __future__ import annotations

import math


def annualize_volatility(volatility: float, trading_days: int = 252) -> float:
    return float(volatility) * math.sqrt(trading_days)


def deannualize_volatility(volatility: float, trading_days: int = 252) -> float:
    return float(volatility) / math.sqrt(trading_days)


def horizon_to_annualized(horizon_volatility: float, horizon_days: int, trading_days: int = 252) -> float:
    if horizon_days <= 0:
        raise ValueError("horizon_days must be positive.")
    return float(horizon_volatility) / math.sqrt(horizon_days / trading_days)
