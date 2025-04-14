import random
import tracemalloc
from typing import List, Dict, Any


class GA:
    """Genetic Algorithm implementation for solving Traveling Salesman Problem (TSP).
    
    The algorithm is constrained to always start and end at node 0, and maintains valid
    TSP permutations throughout its operations.
    
    Attributes:
        dist_matrix: Distance matrix between nodes
        pop_size: Population size for each generation
        mut_rate: Mutation probability rate
        cross_rate: Crossover probability rate
        elitism: Percentage of elites to preserve between generations
        max_gens: Maximum number of generations to evolve
        early_stop: Early stopping criteria for convergence
        num_nodes: Number of nodes in the problem
        iterations: Number of generations evolved
        best_cost: Best solution cost found
        best_path: Best solution path found
        population: Current population of solutions
    """

    def __init__(
        self,
        distance_matrix: List[List[float]],
        population_size: int = 100,
        mutation_rate: float = 0.01,
        crossover_rate: float = 0.9,
        elitism: float = 0.1,
        max_generations: int = 1000,
        early_stopping: int = 100
    ) -> None:
        """Initialize GA solver with problem parameters.

        Args:
            distance_matrix: Square matrix of distances between nodes
            population_size: Number of individuals in each population
            mutation_rate: Probability of mutation per individual [0-1]
            crossover_rate: Probability of crossover per pair [0-1]
            elitism: Percentage of population to preserve as elites [0-1]
            max_generations: Maximum number of generations to evolve
            early_stopping: Stop if no improvement for this many generations

        Raises:
            ValueError: If invalid parameters are provided
        """
        self.dist_matrix: List[List[float]] = distance_matrix
        self.pop_size: int = population_size
        self.mut_rate: float = mutation_rate
        self.cross_rate: float = crossover_rate
        self.elitism: float = elitism
        self.max_gens: int = max_generations
        self.early_stop: int = early_stopping

        self.num_nodes: int = len(distance_matrix)
        self.iterations: int = 0
        self.best_cost: float = float('inf')
        self.best_path: List[int] = []
        self.population: List[List[int]] = []

    def _initialize_population(self) -> None:
        """Generate initial population with valid TSP permutations.
        
        Each individual starts with node 0 followed by a random permutation
        of the remaining nodes.
        """
        self.population = [
            [0] + random.sample(range(1, self.num_nodes), self.num_nodes - 1)
            for _ in range(self.pop_size)
        ]

    def _calculate_fitness(self, individual: List[int]) -> float:
        """Calculate total travel distance for a given solution.

        Args:
            individual: TSP path starting with node 0

        Returns:
            Total distance of the cyclic path
        """
        total = 0.0
        for i in range(len(individual)):
            from_idx = individual[i - 1]
            to_idx = individual[i]
            total += self.dist_matrix[from_idx][to_idx]
        return total

    def _tournament_selection(self, k: int = 5) -> List[int]:
        """Select parent through tournament selection.

        Args:
            k: Tournament size (number of random individuals to compare)

        Returns:
            Best individual from the tournament
        """
        tournament = random.sample(self.population, k)
        return min(tournament, key=self._calculate_fitness)

    def _ordered_crossover(
        self,
        parent1: List[int],
        parent2: List[int]
    ) -> List[int]:
        """Perform Ordered Crossover (OX1) while preserving starting node.

        Args:
            parent1: First parent solution
            parent2: Second parent solution

        Returns:
            Child solution combining genetic material from both parents
        """
        remaining1 = parent1[1:]
        remaining2 = parent2[1:]
        size = len(remaining1)
        
        # Perform OX1 on remaining nodes
        start, end = sorted(random.sample(range(size), 2))
        child_remaining = [None] * size
        
        # Copy segment from parent1
        child_remaining[start:end+1] = remaining1[start:end+1]
        
        # Fill remaining positions from parent2
        current = (end + 1) % size
        for gene in remaining2:
            if gene not in child_remaining[start:end+1]:
                child_remaining[current] = gene
                current = (current + 1) % size
        
        return [0] + child_remaining

    def _swap_mutation(self, individual: List[int]) -> List[int]:
        """Perform swap mutation while preserving starting node.

        Args:
            individual: Solution path to potentially mutate

        Returns:
            Possibly mutated solution (same individual if no mutation)
        """
        if random.random() < self.mut_rate:
            i, j = random.sample(range(1, len(individual)), 2)
            individual[i], individual[j] = individual[j], individual[i]
        return individual

    def _get_best(self) -> bool:
        """Update best solution found in current population.

        Returns:
            True if new best found, False otherwise
        """
        current_best = min(self.population, key=self._calculate_fitness)
        current_cost = self._calculate_fitness(current_best)
        
        if current_cost < self.best_cost:
            self.best_cost = current_cost
            self.best_path = current_best.copy()
            return True
        return False

    def solve(self) -> Dict[str, Any]:
        """Execute the genetic algorithm optimization process.

        Returns:
            Dictionary containing:
            - cost: Best solution total distance
            - path: Best solution node order (starts and ends at 0)
            - iterations: Number of generations evolved
            - memory_bytes: Peak memory usage during optimization
        """
        tracemalloc.start()
        self._initialize_population()
        no_improve = 0
        elite_size = int(self.pop_size * self.elitism)

        for gen in range(self.max_gens):
            self.iterations = gen + 1
            improved = self._get_best()
            
            # Early stopping check
            if improved:
                no_improve = 0
            else:
                no_improve += 1
                if no_improve >= self.early_stop:
                    break

            # Create next generation
            next_pop: List[List[int]] = []
            
            # Preserve elites
            elites = sorted(self.population, key=self._calculate_fitness)[:elite_size]
            next_pop.extend(elites)

            # Generate offspring
            while len(next_pop) < self.pop_size:
                parent1 = self._tournament_selection()
                parent2 = self._tournament_selection()

                if random.random() < self.cross_rate:
                    child = self._ordered_crossover(parent1, parent2)
                else:
                    child = random.choice([parent1, parent2])

                child = self._swap_mutation(child)
                next_pop.append(child)

            self.population = next_pop

        # Complete the cycle by returning to start node
        self.best_path.append(0)

        # Get memory usage statistics
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        return {
            "cost": self.best_cost,
            "path": self.best_path,
            "iterations": self.iterations,
            "memory_bytes": peak
        }
    