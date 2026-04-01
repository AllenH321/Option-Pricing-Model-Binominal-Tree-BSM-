# Option Pricing Model

This project builds an option pricing workflow around three core components:

- `data_helper`: market data retrieval, validation, cleaning, and file management
- `volatility`: return construction and volatility estimation
- `pricing_model`: Cox-Ross-Rubinstein (CRR) and Black-Scholes-Merton (BSM) pricing models

The project is organized as a notebook-driven analysis supported by a reusable Python package in `src/`.

## Authorship

`Version 1` of this project was originally developed as a group project.

`Version 2`, including the package redesign, notebook restructuring, workflow rewrite, market-validation notebook, and updated documentation, was completed independently by `Changhao He`.

## Project Objective

The goal of this project is to study option pricing from both a modeling and a market-validation perspective.

The workflow notebook estimates stock volatility, builds pricing inputs, and generates option values using:

- `CRR` for American and European options
- `BSM` for European options

The testing notebook performs a cross-sectional validation using current option market quotes from `yfinance`, so the model prices can be compared directly with observed market prices.

## Repository Structure

```text
.
├─ data/
│  ├─ raw/
│  └─ processed/
├─ docs/
│  ├─ figures/
│  ├─ tables/
│  ├─ project-summary.md
│  └─ v2-design.md
├─ notebooks/
│  ├─ 01_workflow.ipynb
│  └─ 02_testing.ipynb
├─ src/
│  └─ option_pricing/
│     ├─ data_helper/
│     ├─ volatility/
│     └─ pricing_model/
├─ pyproject.toml
└─ README.md
```

## Main Notebooks

### `notebooks/01_workflow.ipynb`

This notebook contains the main pricing workflow:

- download and clean stock-price data
- compute volatility inputs
- fetch the daily SOFR risk-free rate
- build strike and maturity inputs
- generate CRR and BSM prices
- save tables and figures

### `notebooks/02_testing.ipynb`

This notebook contains the market validation workflow:

- fetch the current option chain from `yfinance`
- estimate volatility using the past 3 years of stock-price history
- compare market prices with:
  - `CRR American`
  - `CRR European`
  - `BSM European`
- visualize pricing error by model, option type, maturity, and strike

## Models Used

### Cox-Ross-Rubinstein (CRR)

The CRR binomial tree model is used for:

- American option pricing
- European option pricing

### Black-Scholes-Merton (BSM)

The BSM model is used only for:

- European option pricing

## Data Sources

- Stock prices: `yfinance`
- Option market quotes: `yfinance`
- Risk-free rate: daily SOFR series

## Outputs

Generated outputs are written to:

- `docs/figures/` for charts
- `docs/tables/` for pricing and validation tables
- `data/processed/` for intermediate processed datasets

## Setup

Install the package in editable mode:

```bash
pip install -e .
```

Then open the notebooks in JupyterLab and run them from top to bottom.

## Versioning

The original pre-rewrite version of the project is preserved in git with the `v1` tag.

- `v1`: original group-project baseline
- `v2`: independently rewritten and restructured by `Changhao He`
