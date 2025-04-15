import json
import os
import csv
from geopy.distance import geodesic
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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

# ========================
# Graph Plotting
# ========================

def plot_graph(nodes: list, paths:list = None) -> None:
    """ Plots graph and paths if needed

    Args:
        nodes (list): List of nodes
        paths (list): List of paths 
    """
    
    df = pd.DataFrame(nodes)

    fig = px.scatter_map(df,
                        lat="atd",
                        lon="lng",
                        hover_name="name",
                        color="id",
                        color_continuous_scale=px.colors.sequential.Viridis,
                        zoom=14,
                        height=800,
                        width=800)
    
    if paths is not None:
        coord_map = {row['id']: (row['atd'], row['lng']) for _, row in df.iterrows()}
        
        path_colors = px.colors.qualitative.Plotly
        
        for i, path in enumerate(paths):
            lats, lons = [], []
            for node_id in path:
                lat, lon = coord_map[node_id]
                lats.append(lat)
                lons.append(lon)
            
            fig.add_trace(go.Scattermap(
                mode="lines+markers",
                lon=lons,
                lat=lats,
                line=dict(width=3, color=path_colors[i % len(path_colors)]),
                name=f"Path {i+1}",
                marker=dict(size=8, color=path_colors[i % len(path_colors)]),
                hoverinfo="none"
            ))

    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                    coloraxis_showscale=False)
    fig.show()
