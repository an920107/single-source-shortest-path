import math
import unittest

from main import Graph, GraphType


class TestGraph(unittest.TestCase):
    def test_init(self):
        cut = Graph(3)
        self.assertEqual(cut[0][0], 0)
        self.assertEqual(cut[0][1], math.inf)
        self.assertEqual(cut[0][2], math.inf)
        self.assertEqual(cut[1][0], math.inf)
        self.assertEqual(cut[1][1], 0)
        self.assertEqual(cut[1][2], math.inf)
        self.assertEqual(cut[2][0], math.inf)
        self.assertEqual(cut[2][1], math.inf)
        self.assertEqual(cut[2][2], 0)

    def test_add_edge(self):
        cut = Graph(3)
        cut.add_edge(0, 1, 1)
        self.assertEqual(cut[0][0], 0)
        self.assertEqual(cut[0][1], 1)
        self.assertEqual(cut[0][2], math.inf)
        self.assertEqual(cut[1][0], math.inf)
        self.assertRaises(ValueError, lambda: cut.add_edge(0, 1, 1))

    def test_evaluate_type(self):
        for testcase in TESTCASES:
            cut = Graph(testcase.vertex_count)
            for from_vertex, to_vertex, weight in testcase.edges:
                cut.add_edge(from_vertex, to_vertex, weight)
            self.assertEqual(cut.evaluate_type(), testcase.ans_type)

    def test_evaluate_distances(self):
        for testcase in TESTCASES:
            cut = Graph(testcase.vertex_count)
            for from_vertex, to_vertex, weight in testcase.edges:
                cut.add_edge(from_vertex, to_vertex, weight)
            distances = cut.evaluate_distances()
            if testcase.ans_distances is None:
                self.assertIsNone(distances)
            else:
                self.assertListEqual(distances, testcase.ans_distances)


class Testcase:
    def __init__(
        self,
        vertex_count: int,
        edges: list[tuple[int]],
        ans_type: GraphType,
        ans_distances: list[int],
    ) -> None:
        self.vertex_count = vertex_count
        self.edges = edges
        self.ans_type = ans_type
        self.ans_distances = ans_distances


TESTCASES = [
    Testcase(
        5,
        [
            (0, 1, 1),
            (1, 2, 1),
            (2, 3, 1),
            (3, 1, -4),
            (0, 3, 10),
        ],
        GraphType.NEG_CYCLE,
        None,
    ),
    Testcase(
        4,
        [
            (0, 1, 2),
            (0, 2, 4),
            (1, 2, -3),
            (1, 3, 2),
            (2, 3, 3),
        ],
        GraphType.NEG_EDGE,
        [0, 2, -1, 2],
    ),
    Testcase(
        4,
        [
            (0, 1, 5),
            (0, 2, 2),
            (0, 3, 7),
            (1, 2, 1),
            (1, 3, 3),
            (2, 0, 6),
        ],
        GraphType.ALL_POS,
        [0, 5, 2, 7],
    ),
    Testcase(
        4,
        [
            (0, 1, 1),
            (0, 2, 2),
            (1, 3, 4),
            (2, 3, 3),
        ],
        GraphType.DAG,
        [0, 1, 2, 5],
    ),
]

if __name__ == "__main__":
    unittest.main()
