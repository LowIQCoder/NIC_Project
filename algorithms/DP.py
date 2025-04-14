import math
import tracemalloc
from typing import List


class DP:
    """Dynamic Programming-based solution for the Traveling Salesman Problem (TSP)."""

    def __init__(self, distance_matrix: List[List[float]]):
        """
        Initializes the DP solver with a distance matrix.

        Args:
            distance_matrix (List[List[float]]): A 2D list representing pairwise distances between nodes.
        """
        self.distance = distance_matrix
        self.n = len(distance_matrix)
        self.memo = {}
        self.parent = {}
        self.iterations = 0

    def solve(self) -> dict:
        """
        Solves the TSP using dynamic programming and memoization.

        Returns:
            dict: A dictionary containing:
                - 'cost' (float): Total cost of the shortest path.
                - 'path' (List[int]): Order of visited nodes (including return to start).
                - 'iterations' (int): Number of recursive calls made.
                - 'memory_bytes' (int): Peak memory usage during execution in bytes.
        """
        tracemalloc.start()

        min_cost = self._tsp(0, 1)
        path = self._reconstruct_path()

        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        return {
            "cost": min_cost,
            "path": path,
            "iterations": self.iterations,
            "memory_bytes": peak
        }

    def _tsp(self, pos: int, visited: int) -> float:
        """
        Recursive helper method that computes the minimum cost using DP.

        Args:
            pos (int): Current node index.
            visited (int): Bitmask representing visited nodes.

        Returns:
            float: Minimum cost to complete the tour from the current state.
        """
        self.iterations += 1
        key = (pos, visited)

        if visited == (1 << self.n) - 1:
            return self.distance[pos][0] or math.inf

        if key in self.memo:
            return self.memo[key]

        min_cost = math.inf
        for city in range(self.n):
            if visited & (1 << city) == 0 and self.distance[pos][city] != 0:
                cost = self.distance[pos][city] + self._tsp(city, visited | (1 << city))
                if cost < min_cost:
                    min_cost = cost
                    self.parent[key] = city

        self.memo[key] = min_cost
        return min_cost

    def _reconstruct_path(self) -> List[int]:
        """
        Reconstructs the shortest path from the memoization and parent tracking.

        Returns:
            List[int]: The sequence of nodes representing the shortest path including return to the start.
        """
        path = [0]
        visited = 1
        current = 0

        while (current, visited) in self.parent:
            next_city = self.parent[(current, visited)]
            path.append(next_city)
            visited |= (1 << next_city)
            current = next_city

        path.append(0)
        return path
