"""Calculate straight-line depreciation and book value per asset.

Usage: python3 main.py assets.csv [--as-of 2026-11-08]
CSV columns: asset,purchase_date (ISO),purchase_price,useful_life_years.
Annual depreciation = price / useful life. Book value at the
reference date = price - annual * whole years since purchase,
never below 0. FULLY DEPRECIATED when the book value reaches 0,
otherwise ACTIVE. Lowest book value first.
"""
import argparse, csv, sys
from datetime import date

def calculate(rows, as_of=None):
    as_of = as_of or date.today()
    out = []
    for row in rows:
        purchased = date.fromisoformat(row["purchase_date"].strip())
        price = float(row["purchase_price"])
        life = int(row["useful_life_years"])
        years = max(0, (as_of - purchased).days // 365)
        annual = round(price / life, 2)
        book_value = max(0.0, round(price - annual * years, 2))
        verdict = "FULLY DEPRECIATED" if book_value == 0 else "ACTIVE"
        out.append((row["asset"].strip(), purchased.isoformat(), price,
                    annual, book_value, verdict))
    return sorted(out, key=lambda r: r[4])

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path")
    parser.add_argument("--as-of", default=None, help="reference date YYYY-MM-DD (default: today)")
    args = parser.parse_args(argv)
    as_of = date.fromisoformat(args.as_of) if args.as_of else None
    with open(args.path, newline="", encoding="utf-8") as f:
        results = calculate(list(csv.DictReader(f)), as_of)
    for asset, purchased, price, annual, book_value, verdict in results:
        print(f"{asset}: {verdict} (bought {purchased} for {price:.2f}, "
              f"{annual:.2f}/year, book value {book_value:.2f})")
    print(f"{sum(1 for *_, v in results if v == 'FULLY DEPRECIATED')} fully depreciated asset(s).")
    return 0

if __name__ == "__main__":
    sys.exit(main())
