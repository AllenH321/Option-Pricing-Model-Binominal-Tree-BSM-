from __future__ import annotations

import math

import pandas as pd

from option_pricing.volatility.transforms import horizon_to_annualized


def _norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def bsm_price(
    spot_price: float,
    strike: float,
    risk_free_rate: float,
    sigma_annual: float,
    maturity_days: int,
    option_type: str = "call",
    dividend_yield: float = 0.0,
    trading_days: int = 252,
) -> float:
    if spot_price <= 0 or strike <= 0:
        raise ValueError("spot_price and strike must be positive.")
    if maturity_days <= 0:
        raise ValueError("maturity_days must be positive.")

    option_type = option_type.lower()
    if option_type not in {"call", "put"}:
        raise ValueError("option_type must be 'call' or 'put'.")

    maturity = maturity_days / trading_days
    if sigma_annual == 0:
        forward = spot_price * math.exp((risk_free_rate - dividend_yield) * maturity)
        discounted = math.exp(-risk_free_rate * maturity)
        payoff = max(forward - strike, 0.0) if option_type == "call" else max(strike - forward, 0.0)
        return float(discounted * payoff)

    sqrt_t = math.sqrt(maturity)
    d1 = (
        math.log(spot_price / strike)
        + (risk_free_rate - dividend_yield + 0.5 * sigma_annual ** 2) * maturity
    ) / (sigma_annual * sqrt_t)
    d2 = d1 - sigma_annual * sqrt_t
    disc_r = math.exp(-risk_free_rate * maturity)
    disc_q = math.exp(-dividend_yield * maturity)

    if option_type == "call":
        return float(spot_price * disc_q * _norm_cdf(d1) - strike * disc_r * _norm_cdf(d2))
    return float(strike * disc_r * _norm_cdf(-d2) - spot_price * disc_q * _norm_cdf(-d1))


def bsm_price_grid(
    ticker: str,
    spot_price: float,
    risk_free_rate: float,
    strike_grid,
    volatility_table: pd.DataFrame,
    trading_days: int = 252,
) -> pd.DataFrame:
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
                    "call_bsm": bsm_price(spot_price, float(strike), risk_free_rate, sigma_annual, maturity_days, "call"),
                    "put_bsm": bsm_price(spot_price, float(strike), risk_free_rate, sigma_annual, maturity_days, "put"),
                }
            )
    return pd.DataFrame(rows).sort_values(["vol_model", "maturity_days", "strike"]).reset_index(drop=True)
