# asset-depreciation-calculator

Calculate straight-line depreciation and book value per asset from a CSV: annual depreciation is price / useful life, book value is price minus annual depreciation for each whole year since purchase, never below 0 — lowest book value first.

## How to run

```sh
python3 main.py assets.csv --as-of 2026-11-08
```

## Example output

```
Old-PC: FULLY DEPRECIATED (bought 2020-01-01 for 60000.00, 20000.00/year, book value 0.00)
Laptop: ACTIVE (bought 2025-11-08 for 100000.00, 25000.00/year, book value 75000.00)
1 fully depreciated asset(s).
```

Standard library only. Run the tests with `python3 -m unittest discover`.
