import json
import os
import csv
from geopy.distance import geodesic

# ========================
# Data Loading & Distance
# ========================
def get_data(path: str) -> list:
    """ Extracts nodes from a given json file """
    with open(os.path.abspath(path), 'r') as file:
        return json.load(file)['nodes']


def get_distances(nodes: list, size: int) -> list:
    """ Generates 2D array of distances between nodes """
    graph = [[0.0 for _ in range(size)] for __ in range(size)]

    for i in range(size):
        for j in range(i + 1, size):
            cord1 = (nodes[i]['atd'], nodes[i]['lng'])
            cord2 = (nodes[j]['atd'], nodes[j]['lng'])
            distance = geodesic(cord1, cord2).m
            graph[i][j] = graph[j][i] = distance

    return graph


# ========================
# CSV Writing
# ========================
def to_file(csv_path, data: dict):
    """ Writes a single result row to the CSV file """
    file_exists = os.path.isfile(csv_path)

    with open(csv_path, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)
