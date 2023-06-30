import unittest
import pandas as pd
import nbformat

class TestCompute(unittest.TestCase):
    def setUp(self) -> None:
        self.test_df =  pd.read_pickle('data/minimal_paths/spotify.pickle.bz2')

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

        pd.testing.assert_frame_equal(result1, result2)

    def test_invalid_input(self):
        pass

    def test_cumsum(self):
        pass

    def test_negative(self):
        df = self.test_df.copy(deep=True)

        df["fastest"] = - df["fastest"]

        result = self.compute(df)

        num_columns = result.shape[1]
        expected_columns = 3

        self.assertTrue(isinstance(result, pd.DataFrame))
        self.assertEqual(num_columns, expected_columns)


    def test_same(self):
        df = self.test_df.copy(deep=True)

        df["fastest"] = df["fastest"][1]

        result = self.compute(df)

        num_columns = result.shape[1]
        expected_columns = 3

        self.assertTrue(isinstance(result, pd.DataFrame))
        self.assertEqual(num_columns, expected_columns)

    def test_missing(self):
        df = self.test_df.copy(deep=True)

        df["fastest"] = None
        result = self.compute(df)

        num_columns = result.shape[1]
        expected_columns = 3

        self.assertTrue(isinstance(result, pd.DataFrame))
        self.assertEqual(num_columns, expected_columns)
