import numpy as np
from memory_profiler import memory_usage

class ACO:
    def __init__(self, distances, n_ants = 10, n_iterations = 100, decay = 0.5, alpha=1, beta=1):
        """
        Initialize the Ant Colony Optimization algorithm.

        Parameters:
        - distances: A 2D numpy array where distances[i][j] represents the distance between cities i and j.
        - n_ants: The number of ants used in the algorithm.
        - n_iterations: The number of iterations to run the algorithm.
        - decay: The rate at which pheromone trails evaporate over time.
        - alpha: The influence of pheromone strength on the probability of selecting the next city.
        - beta: The influence of heuristic value (inverse of distance) on the probability of selecting the next city.
        """
        self.distances = np.array(distances)
        self.pheromones = np.ones(self.distances.shape) / len(self.distances)
        self.n_ants = n_ants
        self.n_iterations = n_iterations
        self.decay = decay
        self.alpha = alpha
        self.beta = beta

    def run(self):
        """
        Run the ACO algorithm to find the shortest path for the TSP.

        Returns:
        - shortest_path: The shortest path found by the algorithm.
        - shortest_distance: The distance of the shortest path.
        """
        shortest_path = None
        shortest_distance = float('inf')
        for i in range(self.n_iterations):
            paths = self._construct_solutions()
            distances = [self._path_distance(path) for path in paths]
            self._update_pheromones(paths, distances)
            best_idx = np.argmin(distances)
            if distances[best_idx] < shortest_distance:
                shortest_distance = distances[best_idx]
                shortest_path = paths[best_idx]
            self.pheromones *= self.decay
        
        return shortest_path, shortest_distance

    def solve(self):
        self.run()
        mem = memory_usage(self.run)
        return {'memory' : sum(mem), 'iter_no' : self.n_iterations}
    
    def _construct_solutions(self):
        """
        Construct solutions for each ant in the colony.

        Returns:
        - paths: A list of paths, one for each ant.
        """
        paths = []
        for _ in range(self.n_ants):
            path = self._construct_path()
            paths.append(path)
        return paths

    def _construct_path(self):
        """
        Construct a path for an ant based on pheromone trails and distances.

        Returns:
        - path: The constructed path.
        """
        path = [0]  # Start from city 0
        remaining = set(range(1, self.distances.shape[0]))
        while remaining:
            current = path[-1]
            next_city = self._select_next(current, remaining)
            path.append(next_city)
            remaining.remove(next_city)
        return path

    def _select_next(self, current, remaining):
        """
        Select the next city to visit based on pheromone trails and heuristic.

        Parameters:
        - current: The current city.
        - remaining: The set of cities that have not yet been visited.

        Returns:
        - The next city to visit.
        """
        choices = list(remaining)
        probs = [
            (self.pheromones[current][j] ** self.alpha) * 
            (self._distance_heuristic(current, j) ** self.beta) 
            for j in choices
        ]
        total_prob = sum(probs)
        normalized_probs = [p / total_prob for p in probs]
        next_city = np.random.choice(choices, p=normalized_probs)
        return next_city

    def _distance_heuristic(self, i, j):
        """
        Calculate the heuristic value for moving from city i to city j.

        Parameters:
        - i: The current city.
        - j: The next city.

        Returns:
        - The heuristic value for moving from city i to city j.
        """
        return 1 / self.distances[i][j]

    def _path_distance(self, path):
        """
        Calculate the total distance of a given path.

        Parameters:
        - path: The path of cities.

        Returns:
        - The total distance of the path.
        """
        return sum([self.distances[path[i]][path[i+1]] for i in range(len(path)-1)]) + self.distances[path[-1]][path[0]]

    def _update_pheromones(self, paths, distances):
        """
        Update the pheromones on the paths based on the distances of the paths.

        Parameters:
        - paths: The paths taken by the ants.
        - distances: The distances of these paths.
        """
        for path, distance in zip(paths, distances):
            delta = 1 / distance
            for i in range(len(path) - 1):
                current_city = path[i]
                next_city = path[i + 1]
                self.pheromones[current_city][next_city] += delta
                self.pheromones[next_city][current_city] += delta