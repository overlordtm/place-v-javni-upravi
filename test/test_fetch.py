import unittest
import pju.fetch
import pandas as pd

class TestFetch(unittest.TestCase):

    def test_fetch(self):
        data = pju.fetch.fetch_payout_types()
        self.assertIsInstance(data, pd.DataFrame)
        print(data.head())

    def test_fetch_subsum(self):
        data = pju.fetch.fetch_payout_subsum(2018, 1)
        self.assertIsInstance(data, pd.DataFrame)
        print(data.head())

    def test_fetch_averages(self):
        data = pju.fetch.fetch_payout_averages(2018, 1)
        self.assertIsInstance(data, pd.DataFrame)
        print(data.head())

    def test_fetch_by_position(self):
        data = pju.fetch.fetch_payouts_by_position(2018, 1)
        self.assertIsInstance(data, pd.DataFrame)
        print(data.head())