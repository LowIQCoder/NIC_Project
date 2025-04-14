import numpy as np
from memory_profiler import memory_usage
from typing import List, Tuple, Dict, Set


class ACO:
    """Ant Colony Optimisation for the Traveling Salesman Problem (TSP)."""

    def __init__(
        self,
        distances: List[List[float]],
        n_ants: int = 10,
        n_iterations: int = 100,
        decay: float = 0.5,
        alpha: float = 1.0,
        beta: float = 1.0
    ) -> None:
        """
        Initialize the Ant Colony Optimization algorithm.

        Args:
            distances: A 2D list where distances[i][j] represents the distance between cities i and j.
            n_ants: The number of ants used in the algorithm.
            n_iterations: The number of iterations to run the algorithm.
            decay: The rate at which pheromone trails evaporate over time.
            alpha: Influence of pheromone strength on city selection.
            beta: Influence of heuristic (1/distance) on city selection.
        """
        self.distances: np.ndarray = np.array(distances)
        self.pheromones: np.ndarray = np.ones(self.distances.shape) / len(self.distances)
        self.n_ants: int = n_ants
        self.n_iterations: int = n_iterations
        self.decay: float = decay
        self.alpha: float = alpha
        self.beta: float = beta

    def run(self) -> Tuple[List[int], float]:
        """
        Run the ACO algorithm to find the shortest path for the TSP.

        Returns:
            Tuple[List[int], float]: The shortest path found and its distance.
        """
        shortest_path: List[int] = []
        shortest_distance: float = float('inf')

        for _ in range(self.n_iterations):
            paths: List[List[int]] = self._construct_solutions()
            distances: List[float] = [self._path_distance(path) for path in paths]
            self._update_pheromones(paths, distances)
            best_idx: int = int(np.argmin(distances))

            if distances[best_idx] < shortest_distance:
                shortest_distance = distances[best_idx]
                shortest_path = paths[best_idx]

            self.pheromones *= self.decay

        shortest_path.append(0)
        return shortest_path, shortest_distance

    def solve(self) -> Dict[str, float | int | List[int]]:
        """
        Solve the TSP using the ACO algorithm and track memory usage.

        Returns:
            dict: Contains cost, path, number of iterations, and memory usage in bytes.
        """
        shortest_path, shortest_distance = self.run()
        mem: List[float] = memory_usage(self.run)

        return {
            "cost": shortest_distance,
            "path": shortest_path,
            "iterations": self.n_iterations,
            "memory_bytes": sum(mem)
        }

    def _construct_solutions(self) -> List[List[int]]:
        """
        Construct solutions (paths) for all ants.

        Returns:
            List[List[int]]: A list of paths, one per ant.
        """
        return [self._construct_path() for _ in range(self.n_ants)]

    def _construct_path(self) -> List[int]:
        """
        Construct a path for an individual ant.

        Returns:
            List[int]: The constructed path.
        """
        path: List[int] = [0]
        remaining: Set[int] = set(range(1, self.distances.shape[0]))

        while remaining:
            current: int = path[-1]
            next_city: int = self._select_next(current, remaining)
            path.append(next_city)
            remaining.remove(next_city)

        return path

    def _select_next(self, current: int, remaining: Set[int]) -> int:
        """
        Select the next city for an ant to visit based on probabilities.

        Args:
            current: Current city.
            remaining: Set of unvisited cities.

        Returns:
            int: The selected next city.
        """
        choices: List[int] = list(remaining)
        probs: List[float] = [
            (self.pheromones[current][j] ** self.alpha) *
            (self._distance_heuristic(current, j) ** self.beta)
            for j in choices
        ]

        total_prob: float = sum(probs)
        normalized_probs: List[float] = [p / total_prob for p in probs]
        next_city: int = int(np.random.choice(choices, p=normalized_probs))
        return next_city

    def _distance_heuristic(self, i: int, j: int) -> float:
        """
        Calculate the heuristic (1 / distance) between two cities.

        Args:
            i: Source city.
            j: Destination city.

        Returns:
            float: Heuristic value.
        """
        return 1 / self.distances[i][j]

    def _path_distance(self, path: List[int]) -> float:
        """
        Compute the total distance of a given path.

        Args:
            path: Sequence of cities visited.

        Returns:
            float: Total path distance including return to start.
        """
        return sum([
            self.distances[path[i]][path[i + 1]] for i in range(len(path) - 1)
        ]) + self.distances[path[-1]][path[0]]

    def _update_pheromones(self, paths: List[List[int]], distances: List[float]) -> None:
        """
        Update the pheromone trails based on paths and distances.

        Args:
            paths: List of paths from each ant.
            distances: Corresponding distances for each path.
        """
        for path, distance in zip(paths, distances):
            delta: float = 1 / distance
            for i in range(len(path) - 1):
                current_city = path[i]
                next_city = path[i + 1]
                self.pheromones[current_city][next_city] += delta
                self.pheromones[next_city][current_city] += delta
