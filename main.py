import json
import os
from datetime import datetime

from algorithms.ACO import ACO
from algorithms.GA import GA
from algorithms.DP import DP


def get_data(path: str) -> tuple:
    """ Extracts nodes and graph information from given json file

    Args:
        path (str): Path to file

    Returns:
        tuple:
            - List of nodes
            - Distance matrix
    """
    PATH = os.path.abspath(path)

    with open(PATH, 'r') as file:
        data = json.load(file)
        nodes = data['nodes']
        graph = data['graph']

        return nodes, graph
    
def main():
    nodes, graph = get_data('./data/graph.json')

    # TODO: Finish ACO, GA, and DP
    aco = ACO(distances=graph)
    ga = GA()
    dp = DP()

    aco_start_time = datetime.now()
    aco_results = aco.solve()
    aco_end_time = datetime.now()
    
    ga_start_time = datetime.now()
    ga_results = ga.solve()
    ga_end_time = datetime.now()

    dp_start_time = datetime.now()
    dp_results = dp.solve()
    dp_end_time = datetime.now()
    
    # TODO: Add new metrics
    print("Testing finished:")
    print("========== ACO ==========")
    print(f"Execution time:\t\t{aco_end_time - aco_start_time}")
    print(f"Number of iterations\t{aco_results['iter_no']}")
    print(f"Used memory:\t\t{aco_results['memory']}")


if __name__ == '__main__':
    main()