import unittest

from simulation.model import CommunicationNetwork
from simulation.minimal_paths import single_source_dijkstra_vertices, single_source_dijkstra_hyperedges, DistanceType


class MinimalPath(unittest.TestCase):
    cn = CommunicationNetwork({'h1': ['v1', 'v2'], 'h2': ['v2', 'v3'], 'h3': ['v3', 'v4']}, {'h1': 1, 'h2': 2, 'h3': 3})

    def test_1(self):
        self.assertEqual(single_source_dijkstra_vertices(MinimalPath.cn, 'v1', DistanceType.SHORTEST, min_timing=0), {'v2': 1, 'v3': 2, 'v4': 3})

    def test_2(self):
        result_1 = single_source_dijkstra_vertices(MinimalPath.cn, 'v1', DistanceType.SHORTEST, min_timing=0)
        result_2 = single_source_dijkstra_hyperedges(MinimalPath.cn, 'v1', DistanceType.SHORTEST, min_timing=0)
        self.assertEqual(result_1, result_2, 'Single-source Dijkstra implementations are not equivalent')

    def test_3(self):
        result_1 = single_source_dijkstra_vertices(MinimalPath.cn, 'v1', DistanceType.FASTEST, min_timing=0)
        result_2 = single_source_dijkstra_hyperedges(MinimalPath.cn, 'v1', DistanceType.FASTEST, min_timing=0)
        self.assertEqual(result_1, result_2, 'Single-source Dijkstra implementations are not equivalent')

    def test_4(self):
        result_1 = single_source_dijkstra_vertices(MinimalPath.cn, 'v1', DistanceType.FOREMOST, min_timing=0)
        result_2 = single_source_dijkstra_hyperedges(MinimalPath.cn, 'v1', DistanceType.FOREMOST, min_timing=0)
        self.assertEqual(result_1, result_2, 'Single-source Dijkstra implementations are not equivalent')


    def test_5(self):
        # Test what happens when the hypergraph is empty
        empty_cn = CommunicationNetwork({}, {})
        result_vertices = single_source_dijkstra_vertices(empty_cn, 'v1', DistanceType.SHORTEST, min_timing=0)
        result_hyperedges = single_source_dijkstra_hyperedges(empty_cn, 'v1', DistanceType.SHORTEST, min_timing=0)
        self.assertEqual(result_vertices, {}, 'Empty hypergraph vertices test failed')
        self.assertEqual(result_hyperedges, {}, 'Empty hypergraph hyperedges test failed')
        self.assertEqual(result_vertices, result_hyperedges, 'Single-source Dijkstra implementations are not equivalent for empty hypergraph')

    #def test_6(self):
        # Test what happens when a hypergraph only has one vertex
       # single_vertex_cn = CommunicationNetwork({'h1': ['v1']}, {'h1': 1})
      #  result_vertices = single_source_dijkstra_vertices(single_vertex_cn, 'v1', DistanceType.SHORTEST, min_timing=0)
       # result_hyperedges = single_source_dijkstra_hyperedges(single_vertex_cn, 'v1', DistanceType.SHORTEST, min_timing=0)
       # self.assertEqual(result_vertices, {}, 'Single vertex hypergraph vertices test failed')
       # self.assertEqual(result_hyperedges, {}, 'Single vertex hypergraph hyperedges test failed')
       # self.assertEqual(result_vertices, result_hyperedges, 'Single-source Dijkstra implementations are not equivalent for single vertex hypergraph')

    def test_7(self):
        # Test what happens when all hypergraphs are connected to all other hypergraphs
        full_cn = CommunicationNetwork({'h1': ['v1', 'v2', 'v3', 'v4'], 'h2': ['v1', 'v2', 'v3', 'v4'], 'h3': ['v1', 'v2', 'v3', 'v4']}, {'h1': 1, 'h2': 2, 'h3': 3})
        expected_result = {'v2': 1, 'v3': 1, 'v4': 1}
        result_vertices = single_source_dijkstra_vertices(full_cn, 'v1', DistanceType.SHORTEST, min_timing=0)
        result_hyperedges = single_source_dijkstra_hyperedges(full_cn, 'v1', DistanceType.SHORTEST, min_timing=0)
        self.assertEqual(result_vertices, expected_result, 'Fully connected hypergraph vertices test failed')
        self.assertEqual(result_hyperedges, expected_result, 'Fully connected hypergraph hyperedges test failed')
        self.assertEqual(result_vertices, result_hyperedges, 'Single-source Dijkstra implementations are not equivalent for fully connected hypergraph')

    def test_8(self):
        # Test what happens when not all nodes have a path to some other nodes
        partial_cn = CommunicationNetwork({'h1': ['v1', 'v2'], 'h2': ['v3', 'v4']}, {'h1': 1, 'h2': 2})
        expected_result = {'v2': 1}
        result_vertices = single_source_dijkstra_vertices(partial_cn, 'v1', DistanceType.SHORTEST, min_timing=0)
        result_hyperedges = single_source_dijkstra_hyperedges(partial_cn, 'v1', DistanceType.SHORTEST, min_timing=0)
        self.assertEqual(result_vertices, expected_result, 'Partially connected hypergraph vertices test failed')
        self.assertEqual(result_hyperedges, expected_result, 'Partially connected hypergraph hyperedges test failed')
        self.assertEqual(result_vertices, result_hyperedges, 'Single-source Dijkstra implementations are not equivalent for partially connected hypergraph')
