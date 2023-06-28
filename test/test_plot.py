import unittest
import pandas as pd
from notebooks.plot import compute

class TestCompute(unittest.TestCase):
    def setUp(self) -> None:
        self.test_df =  pd.read_pickle('../data/minimal_paths/spotify.pickle.bz2')

    def test_reproducability(self):
        df1 = self.test_df.copy(deep=True)
        df2 = self.test_df.copy(deep=True)

        result1 = compute(df1)
        result2 = compute(df2)

        pd.testing.assert_frame_equal(result1, result2)

    def test_invalid_input(self):
        pass

    def test_cumsum(self):
        pass

    def test_missing(self):
        pass

    def test_negative(self):
        pass

    def test_same(self):
        pass
