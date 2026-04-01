# Version 2 Design

## Goals

- simplify the package structure
- move core logic out of notebooks
- keep one notebook for workflow and one notebook for testing
- make the code easier to read, maintain, and extend

## Package Domains

### `data_helper`

Responsible for:

- fetching market data
- validating user input
- cleaning price data
- saving and loading csv files

### `volatility`

Responsible for:

- computing returns
- estimating realized and rolling volatility
- transforming volatility between horizon and annualized forms
- supporting optional GARCH forecasting

### `pricing_model`

Responsible for:

- generating strike grids
- pricing European options with BSM
- pricing American options with a CRR binomial tree
- comparing pricing outputs across maturities and strikes

## Notebook Strategy

### `01_workflow.ipynb`

Shows the full project pipeline from raw market data to model outputs.

### `02_testing.ipynb`

Contains lightweight notebook-based tests and sanity checks for the package.

## Output Strategy

- `docs/figures/` stores generated charts
- `docs/tables/` stores generated pricing and validation tables
- `data/processed/` stores intermediate processed datasets
