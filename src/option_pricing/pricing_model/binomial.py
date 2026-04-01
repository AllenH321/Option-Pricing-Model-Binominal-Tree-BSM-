from __future__ import annotations

import numpy as np
import pandas as pd

from option_pricing.volatility.transforms import horizon_to_annualized


def crr_binomial_price(
    spot_price: float,
    strike: float,
    risk_free_rate: float,
    sigma_annual: float,
    maturity_days: int,
    option_type: str = "call",
    exercise_style: str = "american",
    steps: int | None = None,
    trading_days: int = 252,
) -> float:
    if spot_price <= 0 or strike <= 0:
        raise ValueError("spot_price and strike must be positive.")
    if maturity_days <= 0:
        raise ValueError("maturity_days must be positive.")
    steps = steps or maturity_days
    if steps <= 0:
        raise ValueError("steps must be positive.")

    option_type = option_type.lower()
    if option_type not in {"call", "put"}:
        raise ValueError("option_type must be 'call' or 'put'.")
    exercise_style = exercise_style.lower()
    if exercise_style not in {"american", "european"}:
        raise ValueError("exercise_style must be 'american' or 'european'.")

    maturity = maturity_days / trading_days
    if sigma_annual == 0:
        forward = spot_price * np.exp(risk_free_rate * maturity)
        discounted = np.exp(-risk_free_rate * maturity)
        payoff = max(forward - strike, 0.0) if option_type == "call" else max(strike - forward, 0.0)
        return float(discounted * payoff)

    dt = maturity / steps
    up = np.exp(sigma_annual * np.sqrt(dt))
    down = 1.0 / up
    discount = np.exp(-risk_free_rate * dt)
    prob = (np.exp(risk_free_rate * dt) - down) / (up - down)
    prob = float(np.clip(prob, 0.0, 1.0))

    idx = np.arange(steps + 1)
    prices = spot_price * (up ** idx) * (down ** (steps - idx))
    if option_type == "call":
        values = np.maximum(prices - strike, 0.0)
    else:
        values = np.maximum(strike - prices, 0.0)

    for step in range(steps - 1, -1, -1):
        values = discount * (prob * values[1:] + (1.0 - prob) * values[:-1])
        if exercise_style == "american":
            idx = np.arange(step + 1)
            prices = spot_price * (up ** idx) * (down ** (step - idx))
            intrinsic = np.maximum(prices - strike, 0.0) if option_type == "call" else np.maximum(strike - prices, 0.0)
            values = np.maximum(values, intrinsic)

    return float(values[0])


def crr_price_grid(
    ticker: str,
    spot_price: float,
    risk_free_rate: float,
    strike_grid,
    volatility_table: pd.DataFrame,
    exercise_style: str = "american",
    trading_days: int = 252,
) -> pd.DataFrame:
    suffix = f"crr_{exercise_style.lower()}"
    rows = []
    for _, row in volatility_table.iterrows():
        sigma_h = float(row["sigma"])
        maturity_days = int(row["horizon_days"])
        sigma_annual = horizon_to_annualized(sigma_h, maturity_days, trading_days=trading_days)
        for strike in strike_grid:
            rows.append(
                {
                    "ticker": ticker.upper(),
                    "spot_price": float(spot_price),
                    "strike": float(strike),
                    "maturity_days": maturity_days,
                    "vol_model": row["model"],
                    "sigma_h": sigma_h,
                    "sigma_annual": sigma_annual,
                    "risk_free_rate": float(risk_free_rate),
                    "exercise_style": exercise_style.lower(),
                    f"call_{suffix}": crr_binomial_price(
                        spot_price,
                        float(strike),
                        risk_free_rate,
                        sigma_annual,
                        maturity_days,
                        "call",
                        exercise_style=exercise_style,
                    ),
                    f"put_{suffix}": crr_binomial_price(
                        spot_price,
                        float(strike),
                        risk_free_rate,
                        sigma_annual,
                        maturity_days,
                        "put",
                        exercise_style=exercise_style,
                    ),
                }
            )
    return pd.DataFrame(rows).sort_values(["vol_model", "maturity_days", "strike"]).reset_index(drop=True)
