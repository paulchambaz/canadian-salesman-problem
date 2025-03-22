from typing import List, Tuple
import networkx as nx
import numpy as np


def create_complete_graph_from_points(
    coordinate_points: List[Tuple[float, float]],
) -> nx.Graph:
    complete_graph = nx.Graph()

    # Add nodes
    for point_index, point_coordinates in enumerate(coordinate_points):
        complete_graph.add_node(point_index, pos=point_coordinates)

    # Add edges with Euclidean distance weights
    for i in range(len(coordinate_points)):
        for j in range(i + 1, len(coordinate_points)):
            distance_weight = euclidean_distance(
                coordinate_points[i], coordinate_points[j]
            )
            complete_graph.add_edge(i, j, weight=distance_weight)

    return complete_graph


def euclidean_distance(
    point1: Tuple[float, float], point2: Tuple[float, float]
) -> float:
    return np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)
