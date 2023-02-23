import unittest
import pju.fetch
import pandas as pd
import vcr
from pandas.api.types import is_integer_dtype

class TestFetch(unittest.TestCase):

    @vcr.use_cassette('test/fixtures/vcr_cassettes/test_fetch_payouts.yaml')
    def test_fetch_payouts(self):
        df = pju.fetch.fetch_payouts()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertIsInstance(df.index, pd.PeriodIndex)
        self.assertIsInstance(df.index.freq, pd.offsets.MonthEnd)
        self.assertEqual(len(df), 155)

        for col in df.columns:
            self.assertTrue(is_integer_dtype(df[col]), f'{col} is not an integer dtype')


    @vcr.use_cassette('test/fixtures/vcr_cassettes/test_fetch_payout_by_budget_user_group.yaml')
    def test_fetch_payout_by_budget_user_group(self):
        data = pju.fetch.fetch_payout_by_budget_user_group(2018, 1)
        self.assertIsInstance(data, pd.DataFrame)
        print(data.head())

    @vcr.use_cassette('test/fixtures/vcr_cassettes/test_fetch_payout_by_budget_user.yaml')
    def test_fetch_payout_by_budget_user(self):
        data = pju.fetch.fetch_payout_by_budget_user(2018, 1)
        self.assertIsInstance(data, pd.DataFrame)
        print(data.head())

    @vcr.use_cassette('test/fixtures/vcr_cassettes/test_fetch_payouts_job_title.yaml')
    def test_fetch_payouts_job_title(self):
        data = pju.fetch.fetch_payouts_job_title(2018, 1)
        self.assertIsInstance(data, pd.DataFrame)
        print(data.head())