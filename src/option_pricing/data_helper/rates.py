from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import date

import pandas as pd


SOFR_FRED_CSV_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=SOFR"


@dataclass(frozen=True)
class SofrRate:
    observation_date: str
    rate_percent: float
    rate_decimal: float
    series: str = "SOFR"
    source: str = "FRED (Federal Reserve Bank of St. Louis), source data from the Federal Reserve Bank of New York"

    def to_frame(self) -> pd.DataFrame:
        return pd.DataFrame([asdict(self)])


def fetch_latest_sofr_rate(url: str = SOFR_FRED_CSV_URL) -> SofrRate:
    sofr = fetch_sofr_history(url=url)
    latest = sofr.iloc[-1]
    return SofrRate(
        observation_date=latest["observation_date"].date().isoformat(),
        rate_percent=float(latest["sofr"]),
        rate_decimal=float(latest["sofr"]) / 100.0,
    )


def fetch_sofr_history(url: str = SOFR_FRED_CSV_URL) -> pd.DataFrame:
    sofr = pd.read_csv(url)
    sofr.columns = [str(column).strip().upper() for column in sofr.columns]

    date_column = "DATE" if "DATE" in sofr.columns else "OBSERVATION_DATE" if "OBSERVATION_DATE" in sofr.columns else None
    if date_column is None or "SOFR" not in sofr.columns:
        raise ValueError(f"Unexpected SOFR columns: {list(sofr.columns)}")

    sofr = sofr.rename(columns={date_column: "observation_date", "SOFR": "sofr"})
    sofr["observation_date"] = pd.to_datetime(sofr["observation_date"], errors="coerce")
    sofr["sofr"] = pd.to_numeric(sofr["sofr"], errors="coerce")
    sofr = sofr.dropna(subset=["observation_date", "sofr"]).sort_values("observation_date").reset_index(drop=True)
    if sofr.empty:
        raise ValueError("SOFR series is empty after cleaning.")
    return sofr


def fetch_sofr_rate_on_or_before(as_of_date: str | date | pd.Timestamp, url: str = SOFR_FRED_CSV_URL) -> SofrRate:
    sofr = fetch_sofr_history(url=url)
    as_of_ts = pd.Timestamp(as_of_date)
    eligible = sofr[sofr["observation_date"] <= as_of_ts]
    if eligible.empty:
        raise ValueError(f"No SOFR observation available on or before {as_of_ts.date().isoformat()}.")

    row = eligible.iloc[-1]
    rate_percent = float(row["sofr"])
    return SofrRate(
        observation_date=row["observation_date"].date().isoformat(),
        rate_percent=rate_percent,
        rate_decimal=rate_percent / 100.0,
    )
