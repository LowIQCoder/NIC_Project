import random
import numgit py as np

# Example: distance matrix between 5 buildings (cities)
distance_matrix = [
    [0, 2, 9, 10, 7],
    [1, 0, 6, 4, 3],
    [15, 7, 0, 8, 3],
    [6, 3, 12, 0, 11],
    [9, 5, 4, 2, 0]
]

NUM_BUILDINGS = len(distance_matrix)       # Number of buildings/cities
POPULATION_SIZE = 1000                     # Number of routes per generation
MUTATION_RATE = 0.2                        # Probability of mutation
GENERATIONS = 200                          # Total number of generations

# Create a random route (a shuffled list of building indices)
def create_route():
    route = list(range(NUM_BUILDINGS))
    random.shuffle(route)
    return route

# Calculate the total distance of the route (looping back to the start)
def calculate_distance(route):
    dist = 0
    for i in range(len(route)):
        from_city = route[i]
        to_city = route[(i + 1) % NUM_BUILDINGS]  # Circular route
        dist += distance_matrix[from_city][to_city]
    return dist

# Perform ordered crossover between two parent routes
def crossover(parent1, parent2):
    start = random.randint(0, NUM_BUILDINGS - 2)
    end = random.randint(start + 1, NUM_BUILDINGS - 1)
    child = [-1] * NUM_BUILDINGS

    # Copy a slice from parent1 into the child
    child[start:end + 1] = parent1[start:end + 1]

    # Fill remaining positions with cities from parent2
    fill_pos = 0
    for city in parent2:
        if city not in child:
            while child[fill_pos] != -1:
                fill_pos += 1
            child[fill_pos] = city
    return child

# Mutate a route by swapping cities with a certain probability
def mutate(route):
    for i in range(NUM_BUILDINGS):
        if random.random() < MUTATION_RATE:
            j = random.randint(0, NUM_BUILDINGS - 1)
            route[i], route[j] = route[j], route[i]

# Select the top-performing half of the population based on fitness (shorter distance is better)
def select_parents(population):
    population.sort(key=lambda r: calculate_distance(r))
    return population[:POPULATION_SIZE // 2]

# Initialize the population with random routes
population = [create_route() for _ in range(POPULATION_SIZE)]

# Main loop of the genetic algorithm
for generation in range(GENERATIONS):
    # Select best-performing routes as parents
    parents = select_parents(population)

    # Create a new generation
    next_generation = parents[:]
    while len(next_generation) < POPULATION_SIZE:
        parent1, parent2 = random.sample(parents, 2)
        child = crossover(parent1, parent2)
        mutate(child)
        next_generation.append(child)

    population = next_generation

# Find the best route in the final population
best_route = min(population, key=calculate_distance)
print("bestPath", best_route)
print("distance:", calculate_distance(best_route))
