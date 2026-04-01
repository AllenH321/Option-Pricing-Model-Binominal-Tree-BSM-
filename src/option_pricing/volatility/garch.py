from __future__ import annotations

import math

import pandas as pd

from .returns import add_log_returns
from .historical import realized_volatility


def forecast_garch_volatility(
    df: pd.DataFrame,
    ticker: str,
    price_column: str = "adj_close",
    horizons: range = range(1, 6),
    trading_days: int = 252,
) -> pd.DataFrame:
    returns = add_log_returns(df, price_column=price_column)["log_return"].dropna() * 100
    try:
        from arch import arch_model
    except ImportError:
        annualized = realized_volatility(df, price_column=price_column, trading_days=trading_days)
        rows = []
        for horizon in horizons:
            rows.append(
                {
                    "ticker": ticker.upper(),
                    "model": "garch_fallback",
                    "horizon_days": int(horizon),
                    "sigma": float(annualized * math.sqrt(horizon / trading_days)),
                    "annualized_sigma": float(annualized),
                }
            )
        return pd.DataFrame(rows)

    model = arch_model(returns, mean="Zero", vol="GARCH", p=1, q=1, rescale=False)
    fit = model.fit(disp="off")
    forecast = fit.forecast(horizon=max(horizons), reindex=False)
    variances = forecast.variance.iloc[-1]

    rows = []
    for horizon in horizons:
        variance = float(variances.iloc[horizon - 1]) / (100.0 ** 2)
        sigma_h = math.sqrt(max(variance, 0.0))
        rows.append(
            {
                "ticker": ticker.upper(),
                "model": "garch",
                "horizon_days": int(horizon),
                "sigma": float(sigma_h),
                "annualized_sigma": float(sigma_h / math.sqrt(horizon / trading_days)),
            }
        )
    return pd.DataFrame(rows)
