from datetime import datetime

from utils.utils import *
from algorithms.DP import DP
from algorithms.ACO import ACO
from algorithms.GA import GA

# =======================
# Configurable Parameters
# =======================
GRAPH_JSON_PATH = './data/graph.json'
MAX_GRAPH_SIZE = 36
MAX_EXECUTION_TIME = 10

ALGORITHMS = {
    'dp': DP,
    'aco': ACO,
    'ga': GA
}

# =======================
# Solver Function
# =======================

def solver(nodes, algorithm_key):
    algorithm = ALGORITHMS[algorithm_key]

    print(f"========== {algorithm_key.upper()} ==========")

    for graph_size in range(2, MAX_GRAPH_SIZE + 1):
        graph = get_distances(nodes, graph_size)
        solver = algorithm(graph)

        start_time = datetime.now()
        result = solver.solve()
        exec_time = (datetime.now() - start_time).total_seconds()

        print(f"\nTest #{graph_size - 1} =============================")
        print(f"Graph size:\t\t{graph_size}")
        print(f"Execution time:\t\t{exec_time:.3f} seconds")
        print(f"Number of iterations:\t{result['iterations']}")
        print(f"Used memory:\t\t{result['memory_bytes']} bytes")
        print(f"Path length (m):\t{result['cost']:.2f}")
        print(f"Path:\t\t\t{' -> '.join(map(str, result['path']))}")

        to_file('./results/results_' + algorithm_key + '.csv', {
            "Graph Size": graph_size,
            "Execution Time (s)": exec_time,
            "Iterations": result['iterations'],
            "Memory (bytes)": result['memory_bytes'],
            "Shortest Path": ' -> '.join(map(str, result['path'])),
            "Path Length (m)": round(result['cost'], 2)
        })

# ========================
# Main Experiment Logic
# ========================
def main():
    nodes = get_data(GRAPH_JSON_PATH)

    solver(nodes, 'dp')
    solver(nodes, 'aco')
    solver(nodes, 'ga')


if __name__ == '__main__':
    main()
