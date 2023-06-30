import unittest
import pandas as pd
import nbformat

class TestCompute(unittest.TestCase):
    def setUp(self) -> None:
        self.test_df =  pd.read_pickle('data/minimal_paths/spotify.pickle.bz2')
        self.expected_shape = (29,1730)
        with open('notebooks/plot.ipynb',encoding="utf-8") as f:
            self.notebook = nbformat.read(f,as_version=4)
        assert 'def compute' in self.notebook.cells[1].source

        import_code = self.notebook.cells[0].source
        necessary_imports = import_code.rfind('\n')
        import_code = import_code[:necessary_imports]
        compute_code = self.notebook.cells[1].source

        exec_globals = {}
        exec(import_code+"\n"+compute_code, exec_globals)
        self.compute = exec_globals['compute']

    def test_reproducability(self):
        result1 = self.compute(self.test_df)
        result2 = self.compute(self.test_df)
        print(result1)
        pd.testing.assert_frame_equal(result1, result2)

    def test_cumsum(self):
        cumsum_df = pd.DataFrame({"a":[1,2,3,4,5],"b":[1,2,3,4,5]})
        calculated_cumsum = pd.DataFrame({"a":[1,3,6,10,15],"b":[1,3,6,10,15]})
        pd.testing.assert_frame_equal(cumsum_df.cumsum(),calculated_cumsum)

    def test_negative(self):
        df = self.test_df.copy(deep=True)
        df["shortest"] = - df["shortest"]
        df["fastest"] = - df["fastest"]
        result = self.compute(df)
        self.assertEqual(result.shape, self.expected_shape)


    def test_same(self):
        df = self.test_df.copy(deep=True)
        df["fastest"] = df["fastest"][0]
        df["shortest"] = 90000000
        result = self.compute(df)
        self.assertEqual(result.shape, self.expected_shape)

    def test_missing(self):
        df = self.test_df.copy(deep=True)

        df["shortest"] = None
        df["target"] = None
        df["source"] = None
        result = self.compute(df)
        self.assertTrue(isinstance(result, pd.DataFrame))
        self.assertEqual(result.shape, self.expected_shape)
