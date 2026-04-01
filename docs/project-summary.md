# Project Summary

## Authorship

`Version 1` was based on the original group project.

`Version 2` was independently redesigned and rewritten by `Changhao He`, including the package structure, notebook organization, pricing workflow, market-validation framework, and project documentation.

## Overview

This project studies option pricing using both theoretical models and current market data. It combines reusable Python modules with notebook-based analysis so that the pricing workflow and the validation workflow are both easy to follow.

The project focuses on three areas:

- market data preparation
- volatility estimation
- option pricing and market validation

## Modeling Framework

### Data Preparation

The project downloads stock-price data with `yfinance`, validates the selected ticker, standardizes the raw data, and stores cleaned outputs for downstream analysis.

### Volatility Estimation

Volatility is estimated from historical stock returns using:

- log-return construction
- realized volatility
- rolling volatility
- optional GARCH-based forecasting

### Pricing Models

The pricing framework uses:

- `CRR` for American options
- `CRR` for European options
- `BSM` for European options

This structure makes it possible to compare binomial and closed-form European prices while still preserving a natural model for American-style contracts.

## Workflow Notebook

The workflow notebook builds the full pricing pipeline:

1. download historical stock prices
2. clean and store the data
3. estimate volatility
4. fetch the daily SOFR risk-free rate
5. generate strike and maturity grids
6. compute option prices using CRR and BSM
7. save final tables and figures

## Market Validation Notebook

The testing notebook performs a cross-sectional market validation using current option quotes from `yfinance`.

For the selected ticker, the notebook:

1. uses the current stock price
2. uses the latest SOFR observation as the risk-free rate
3. estimates annualized volatility from the past 3 years of stock-price history
4. downloads the current option chain
5. selects contracts across nearby strikes and future maturities
6. compares observed market prices with:
   - `CRR American`
   - `CRR European`
   - `BSM European`

## Visualization

The project includes several visual checks:

- stock price and rolling volatility
- market price vs model price
- average absolute error by model
- average absolute error by option type
- error distribution by maturity
- error distribution by strike

All figures are saved to `docs/figures/`, and generated pricing or validation tables are saved to `docs/tables/`.

## Key Takeaway

The project is designed not only to compute option values, but also to test how well standard pricing models align with observed market prices. This makes the project both a modeling exercise and a validation exercise.
