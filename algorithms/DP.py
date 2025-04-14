import math
import tracemalloc
from typing import List

class DP:
    def __init__(self, distance_matrix: List[List[float]]):
        self.distance = distance_matrix
        self.n = len(distance_matrix)
        self.memo = {}
        self.parent = {}
        self.iterations = 0

    def solve(self):
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

    def _reconstruct_path(self):
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
