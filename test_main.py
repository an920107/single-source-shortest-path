import math
import unittest

from main import Graph, GraphType

TESTCASES = [
    [
        (0, 1, 1),
        (1, 2, 1),
        (2, 3, 1),
        (3, 1, -4),
        (0, 3, 10),
    ],
    [
        (0, 1, 2),
        (0, 2, 4),
        (1, 2, -3),
        (1, 3, 2),
        (2, 3, 3),
    ],
    [
        (0, 1, 5),
        (0, 2, 2),
        (0, 3, 7),
        (1, 2, 1),
        (1, 3, 3),
        (2, 0, 6),
    ],
    [
        (0, 1, 1),
        (0, 2, 2),
        (1, 3, 4),
        (2, 3, 3),
    ],
]


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
        cut = Graph(5)
        vals = TESTCASES[0]
        for from_vertex, to_vertex, weight in vals:
            cut.add_edge(from_vertex, to_vertex, weight)
        self.assertEqual(cut.evaluate_type(), GraphType.NEG_CYCLE)

        cut = Graph(4)
        vals = TESTCASES[1]
        for from_vertex, to_vertex, weight in vals:
            cut.add_edge(from_vertex, to_vertex, weight)
        self.assertEqual(cut.evaluate_type(), GraphType.NEG_EDGE)

        cut = Graph(4)
        vals = TESTCASES[2]
        for from_vertex, to_vertex, weight in vals:
            cut.add_edge(from_vertex, to_vertex, weight)
        self.assertEqual(cut.evaluate_type(), GraphType.ALL_POS)

        cut = Graph(4)
        vals = TESTCASES[3]
        for from_vertex, to_vertex, weight in vals:
            cut.add_edge(from_vertex, to_vertex, weight)
        self.assertEqual(cut.evaluate_type(), GraphType.DAG)


if __name__ == "__main__":
    unittest.main()
