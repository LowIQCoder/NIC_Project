import time
from multiprocessing import Process, Queue
from utils.utils import *
from algorithms.DP import DP
from algorithms.ACO import ACO
from algorithms.GA import GA

# =======================
# Configurable Parameters
# =======================
GRAPH_JSON_PATH = './data/nodes.json'
MAX_GRAPH_SIZE = 36
MAX_EXECUTION_TIME = 1 * 60 * 60
ALGORITHMS = {
    'dp': DP,
    'aco': ACO,
    'ga': GA
}

def run_solver(queue, algorithm_class, graph):
    """Execute solver in a separate process and return results through queue."""
    try:
        solver = algorithm_class(graph)
        result = solver.solve()
        queue.put(result)
    except Exception as e:
        queue.put({'error': str(e)})

# =======================
# Solver Function
# =======================
def solver(nodes, algorithm_key):
    algorithm = ALGORITHMS[algorithm_key]
    timed_counter = 0

    for graph_size in range(3, MAX_GRAPH_SIZE + 1):
        graph = get_distances(nodes, graph_size)
        result = None
        timed_out = False
        
        queue = Queue()
        process = Process(target=run_solver, args=(queue, algorithm, graph))
        
        start_time = time.time()
        process.start()
        process.join(timeout=MAX_EXECUTION_TIME)
        exec_time = time.time() - start_time

        if process.is_alive():
            process.terminate()
            process.join()
            print(f"{algorithm_key.upper()} timed out ({MAX_EXECUTION_TIME}s) | Size: {graph_size}")
            timed_out = True
        else:
            result = queue.get()
            if 'error' in result:
                print(f"{algorithm_key.upper()} error | Size: {graph_size}: {result['error']}")
                continue

        if timed_out:
            timed_counter += 1
            if timed_counter >= 3:
                return 0
            continue

        print(f"\nTest #{graph_size-1} ============== {algorithm_key.upper()} ==============")
        print(f"Graph size:\t\t{graph_size}")
        print(f"Execution time:\t\t{exec_time:.3f}s")
        print(f"Iterations:\t\t{result.get('iterations', 'N/A')}")
        print(f"Memory used:\t\t{result.get('memory_bytes', 'N/A')} bytes")
        print(f"Path length:\t\t{result.get('cost', 'N/A'):.2f}m")
        path = result.get('path', [])
        print(f"Optimal path:\t\t{' -> '.join(map(str, path)) if path else 'N/A'}")

        to_file(f'./results/results_{algorithm_key}.csv', {
            "Graph Size": graph_size,
            "Execution Time (s)": round(exec_time, 3),
            "Iterations": result.get('iterations', ''),
            "Memory (bytes)": result.get('memory_bytes', ''),
            "Shortest Path": ' -> '.join(map(str, path)) if path else '',
            "Path Length (m)": round(result.get('cost', 0), 2)
        })

# ========================
# Main Execution
# ========================
def main():
    nodes = get_data(GRAPH_JSON_PATH)
    for algorithm in ['ga', 'aco', 'dp']:
        solver(nodes, algorithm)

if __name__ == '__main__':
    main()
