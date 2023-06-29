import unittest
from collections import defaultdict
import os
import sys
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from simulation.model import TimeVaryingHypergraph, CommunicationNetwork
#:))
class TestTimeVaryHypergraph(unittest.TestCase):
    """Tests for `model.py` module"""
    def test_class_creation(self):
        """Test that the class(TimeVaryingHypergraph) can be instantiated"""
        hedges = {'hedge1': ['v1', 'v2'], 'hedge2': ['v2', 'v3']}
        timings = {'v1': [1, 2, 3], 'v2': [2, 3, 4], 'v3': [3, 4, 5]}
        cls = TimeVaryingHypergraph(hedges=hedges, timings=timings)
        self.assertEqual(cls._hedges, hedges)
        self.assertEqual(cls._timings, timings)
        self.assertIsInstance(cls, TimeVaryingHypergraph)
    def test_timings(self):
        """Test that the timings method works and returns the correct values"""
        timings = {'v1': [1, 2, 3], 'v2': [2, 3, 4], 'v3': [3, 4, 5]}
        tvh = TimeVaryingHypergraph(hedges={}, timings=timings)
        timings_returned = tvh.timings()
        self.assertIsInstance(timings_returned, dict)
    def test_vertices(self):
        """ Test that the vertices method works and returns the correct values without hedge"""
        hedges = {'hedge1': ['v1', 'v2'], 'hedge2': ['v2', 'v3']}
        tvh = TimeVaryingHypergraph(hedges=hedges, timings={})
        vertices_returned = tvh.vertices()
        self.assertIsInstance(vertices_returned, set)
        self.assertEqual(vertices_returned, {'v1', 'v2', 'v3'})

    def test_vertices_hedge(self):
        """Test that the vertices method works and returns the correct values with hedge"""
        hedges = {'hedge1': ['v1', 'v2'], 'hedge2': ['v2', 'v3']}
        tvh = TimeVaryingHypergraph(hedges=hedges, timings={})
        vertices_returned = tvh.vertices(hedge='hedge1')
        self.assertIsInstance(vertices_returned, set)
        self.assertEqual(vertices_returned, {'v1', 'v2'})

    def test_hyperedges(self):
        """Test that the hyperedges method works and returns the correct values without vertex"""
        hedges = {'hedge1': ['v1', 'v2'], 'hedge2': ['v2', 'v3']}
        tvh = TimeVaryingHypergraph(hedges=hedges, timings={})
        hyperedges_returned = tvh.hyperedges()
        self.assertIsInstance(hyperedges_returned, set)
        self.assertEqual(hyperedges_returned, {'hedge1', 'hedge2'})

    def test_hyperedges_hedge(self):
        """Test that the hyperedges method works and returns the correct values"""
        hedges = {'hedge1': ['v1', 'v2'], 'hedge2': ['v2', 'v3']}
        tvh = TimeVaryingHypergraph(hedges=hedges, timings={})
        hyperedges_returned = tvh.hyperedges(vertex='v1')
        self.assertIsInstance(hyperedges_returned, set)
        self.assertEqual(hyperedges_returned, {'hedge1'})



class TestCommunicationNetwork(unittest.TestCase):
    def test_class_creation(self):
        """Test that the class(CommunicationNetwork) can be instantiated"""
        pass



if __name__ == '__main__':
    unittest.main()
