import math
import os
from enum import Enum


class GraphType(int, Enum):
    NEG_CYCLE = 0
    NEG_EDGE = 1
    WITHOUT_NEG = 2
    DAG = 3


class Graph(list[list[int]]):
    def __init__(self, vertex_count: int) -> None:
        super().__init__(
            [[math.inf for _ in range(vertex_count)] for _ in range(vertex_count)]
        )
        for i in range(vertex_count):
            self[i][i] = 0

    def __str__(self) -> str:
        return "\n".join("\t".join(map(str, row)) for row in self)

    def _bellman_ford_init(self) -> list[float]:
        distances = [math.inf for _ in range(len(self))]
        distances[0] = 0
        return distances

    def _ballman_ford_determine(
        self, distances: list[float], from_vertex: int, to_vertex: int
    ) -> bool:
        return (
            self[from_vertex][to_vertex] != math.inf
            and distances[from_vertex] != math.inf
            and distances[from_vertex] + self[from_vertex][to_vertex]
            < distances[to_vertex]
        )

    def _bellman_ford_relax(self, distances: list[float]) -> list[float]:
        distances = distances.copy()

        for _ in range(len(self) - 1):
            for from_vertex in range(len(self)):
                for to_vertex in range(len(self)):
                    if self._ballman_ford_determine(distances, from_vertex, to_vertex):
                        distances[to_vertex] = (
                            distances[from_vertex] + self[from_vertex][to_vertex]
                        )
        return distances

    def _is_with_neg_cycle(self) -> bool:
        distances = self._bellman_ford_init()
        distances = self._bellman_ford_relax(distances)

        for from_vertex in range(len(self)):
            for to_vertex in range(len(self)):
                if self._ballman_ford_determine(distances, from_vertex, to_vertex):
                    return True
        return False

    def _is_dag(self) -> bool:
        visited = [False] * len(self)
        recursion_stack = [False] * len(self)

        def dfs(from_vertex: float) -> bool:
            visited[from_vertex] = True
            recursion_stack[from_vertex] = True

            row = self[from_vertex]
            for to_vertex in range(len(row)):
                if row[to_vertex] == math.inf or from_vertex == to_vertex:
                    continue
                if not visited[to_vertex]:
                    if not dfs(to_vertex):
                        return False
                elif recursion_stack[to_vertex]:
                    return False

            recursion_stack[from_vertex] = False
            return True

        return dfs(0)

    def add_edge(self, from_vertex: int, to_vertex: int, weight: int) -> None:
        if self[from_vertex][to_vertex] != math.inf:
            raise ValueError("Edge already exists")
        self[from_vertex][to_vertex] = weight

    def evaluate_type(self) -> GraphType:
        # Check for Negative Weight Cycles
        if self._is_with_neg_cycle():
            return GraphType.NEG_CYCLE

        # Check for Negative Weight Edges
        for row in self:
            for weight in row:
                if weight < 0:
                    return GraphType.NEG_EDGE
        # Check for DAG
        if self._is_dag():
            return GraphType.DAG

        # Other scenario
        return GraphType.WITHOUT_NEG


def main():
    with open(os.path.join("input.txt"), "r") as f:
        vertex_count, edge_count = map(int, f.readline().split())
        graph = Graph(vertex_count)
        for _ in range(edge_count):
            graph.add_edge(*map(int, f.readline().split()))
        match graph.evaluate_type():
            case GraphType.NEG_CYCLE:
                print("A graph with negative weight cycles")
            case GraphType.NEG_EDGE:
                print(
                    "A graph with negative weight edges but no negative weight cycles"
                )
            case GraphType.WITHOUT_NEG:
                print("A graph with no negative weight edges")
            case GraphType.DAG:
                print("A directed acyclic graph")


if __name__ == "__main__":
    main()
