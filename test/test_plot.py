import unittest
import time
import pandas as pd
import nbformat

class TestCompute(unittest.TestCase):
    def setUp(self) -> None:
        self.test_df =  pd.read_pickle('data/minimal_paths/spotify.pickle.bz2')
        self.expected_shape = (29,1730)
        with open('notebooks/plot.ipynb',encoding="utf-8") as f:
            self.notebook = nbformat.read(f,as_version=4)
        assert 'def compute' in self.notebook.cells[1].source

        #Gets code from the cells which contain compute and all necessary imports
        import_code = self.notebook.cells[0].source
        necessary_imports = import_code.rfind('from tqdm.notebook import tqdm')
        import_code = import_code[:necessary_imports] # the last import causes errors
        compute_code = self.notebook.cells[1].source


        exec_globals = {}
        exec(import_code+"\n"+compute_code, exec_globals)
        self.compute = exec_globals['compute']

        self.normal_result = self.compute(self.test_df)

    def test_reproducability(self):
        result2 = self.compute(self.test_df)
        pd.testing.assert_frame_equal(self.normal_result, result2)

    def test_reproducability_time(self):
        """Test performance consistency"""
        t1 = time.perf_counter()
        self.compute(self.test_df)
        t1 = time.perf_counter() - t1

        t2 = time.perf_counter()
        self.compute(self.test_df)
        t2 = time.perf_counter() - t2

        diff = abs(t2-t1)/t1
        self.assertLess(diff,0.05)

    def test_cumsum(self):
        cumsum_df = pd.DataFrame({"a":[1,2,3,4,5],"b":[1,2,3,4,5]})
        calculated_cumsum = pd.DataFrame({"a":[1,3,6,10,15],"b":[1,3,6,10,15]})
        pd.testing.assert_frame_equal(cumsum_df.cumsum(),calculated_cumsum)

    # def test_same(self):
    #     """FAILED, should be a dataframe of 0s up until number days"""
    #     number_days = 19
    #     df = self.test_df.copy(deep=True)
    #     df["fastest"] = pd.Timedelta(days=number_days)
    #     result = self.compute(df)
    #
    #     self.assertEqual(result.shape, self.expected_shape)
    #     self.assertTrue(result.iloc[number_days:].duplicated(keep=False).all())
    #     self.assertTrue((result.iloc[:number_days-1] == 0).all().all(),"Assertion failed, nodes reached before fastest day")

    def test_missing(self):

        stored_val = self.test_df["fastest"]["0063ea80576f47764e075f3ed99090de"]["3bc5fbfb1e502db2169558785b6f0a7d"] #saving the value is faster than deepcopy
        self.test_df["fastest"]["0063ea80576f47764e075f3ed99090de"]["3bc5fbfb1e502db2169558785b6f0a7d"] = None
        result = self.compute(self.test_df)
        self.test_df["fastest"]["0063ea80576f47764e075f3ed99090de"]["3bc5fbfb1e502db2169558785b6f0a7d"] = stored_val

        self.assertEqual(result.shape, self.expected_shape)
        try:
            pd.testing.assert_frame_equal(self.normal_result,result, check_exact=False)
            self.fail('DataFrames are equal, but they should not be.')
        except AssertionError:
            pass  # Produces different dataframes which should be expected.

    def test_negative_shortest(self):
        """Should not have any effect on the results as shortest is not used"""
        self.test_df["shortest"] = -self.test_df["shortest"]
        result = self.compute(self.test_df)
        self.test_df["shortest"] = -self.test_df["shortest"]
        self.assertEqual(result.shape, self.expected_shape)
        pd.testing.assert_frame_equal(self.normal_result,result)

    def test_negative_fastest (self):
        """Setting a time to be a negative value can have unforseen consequences,
        but it should produce differing results than the positive version"""

        self.test_df["fastest"] = -self.test_df["fastest"]
        neg_result = self.compute(self.test_df)
        self.test_df["fastest"] = -self.test_df["fastest"]

        self.assertEqual(neg_result.shape, self.expected_shape)
        try:
            pd.testing.assert_frame_equal(self.normal_result,neg_result, check_exact=False)
            self.fail('DataFrames are equal, but they should not be.')
        except AssertionError:
            pass  # Produces different dataframes which should be expected.
