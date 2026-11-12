import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import unittest
from main import calculate

import datetime
AS_OF = datetime.date(2026, 11, 8)

def row(asset, purchased, price, life):
    return {"asset": asset, "purchase_date": purchased,
            "purchase_price": str(price), "useful_life_years": str(life)}

class TestDepreciation(unittest.TestCase):
    def test_annual_depreciation(self):
        self.assertEqual(calculate([row("Laptop", "2025-11-08", 100000, 4)], AS_OF)[0][3], 25000.0)
    def test_book_value_after_one_year(self):
        self.assertEqual(calculate([row("Laptop", "2025-11-08", 100000, 4)], AS_OF)[0][4], 75000.0)
    def test_fully_depreciated(self):
        r = calculate([row("Old-PC", "2020-01-01", 60000, 3)], AS_OF)[0]
        self.assertEqual((r[4], r[5]), (0.0, "FULLY DEPRECIATED"))
    def test_book_value_never_negative(self):
        self.assertGreaterEqual(calculate([row("Old-PC", "2010-01-01", 60000, 3)], AS_OF)[0][4], 0.0)
    def test_future_purchase_full_value(self):
        r = calculate([row("New-PC", "2027-01-01", 80000, 4)], AS_OF)[0]
        self.assertEqual((r[4], r[5]), (80000.0, "ACTIVE"))
    def test_lowest_book_value_first(self):
        r = calculate([row("A", "2025-11-08", 100000, 4), row("B", "2020-01-01", 60000, 3)], AS_OF)
        self.assertEqual(r[0][0], "B")
