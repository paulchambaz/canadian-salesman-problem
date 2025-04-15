"""Utility functions for TSP algorithm implementations and experiments.

This module provides helper functions for graph creation, distance calculation,
path evaluation, and performance measurement for TSP algorithms.
"""

import math
import random

import networkx as nx
import numpy as np

from .types import Edge, Path, Weight


def create_polygon_graph(
    n: int, low: float = -5.0, high: float = 5.0
) -> nx.Graph:
    """Create a complete graph with nodes arranged in a regular polygon.

    Places n nodes on a circle and connects all nodes with edges weighted by
    their Euclidean distance. The nodes are mapped from polar coordinates to the
    range specified by low and high parameters.

    Args:
        n: Number of nodes in the graph
        low: Minimum coordinate value in the output range
        high: Maximum coordinate value in the output range

    Returns:
        Complete graph with n nodes arranged in a regular polygon
    """
    points = []
    for i in range(n):
        angle = 2.0 * math.pi * i / n
        x = (high - low) * (math.sin(angle) + 1.0) / 2.0 + low
        y = (high - low) * (math.cos(angle) + 1.0) / 2.0 + low
        points.append((x, y))

    return create_complete_graph_from_points(points)


def create_random_graph(
    n: int, low: float = -5.0, high: float = 5.0
) -> nx.Graph:
    """Create a complete graph with randomly positioned nodes.

    Generates n nodes with random x,y coordinates within the specified range and
    connects all nodes with edges weighted by their Euclidean distance.

    Args:
        n: Number of nodes in the graph
        low: Lower bound for random coordinate generation
        high: Upper bound for random coordinate generation

    Returns:
        Complete graph with n randomly positioned nodes
    """
    points = [
        (random.uniform(low, high), random.uniform(low, high)) for _ in range(n)
    ]
    return create_complete_graph_from_points(points)


def create_random_blocks(n: int, graph: nx.Graph) -> set[Edge]:
    """Select n random edges to block from the graph.

    Randomly selects n edges from the graph to be marked as blocked.

    Args:
        n: Number of edges to block
        graph: Graph from which to select edges

    Returns:
        Set of edges (formatted as ordered node pairs) that are blocked
    """
    edges = list(graph.edges())
    blocked_edges = set()
    for _ in range(n):
        u, v = random.choice(edges)
        blocked_edges.add(edge(u, v))
        edges.remove((u, v))
    return blocked_edges


def create_complete_graph_from_points(
    coordinate_points: list[tuple[float, float]],
) -> nx.Graph:
    """Create a complete graph from a list of 2D coordinate points.

    Builds a complete graph where nodes correspond to the given coordinates and
    edge weights are the Euclidean distances between points.

    Args:
        coordinate_points: List of (x, y) coordinates

    Returns:
        Complete graph with nodes at the specified coordinates
    """
    complete_graph = nx.Graph()

    for point_index, point_coordinates in enumerate(coordinate_points):
        complete_graph.add_node(point_index, pos=point_coordinates)

    for i in range(len(coordinate_points)):
        for j in range(i + 1, len(coordinate_points)):
            distance_weight = euclidean_distance(
                coordinate_points[i], coordinate_points[j]
            )
            complete_graph.add_edge(i, j, weight=distance_weight)

    return complete_graph


def euclidean_distance(
    point1: tuple[float, float], point2: tuple[float, float]
) -> float:
    """Calculate the Euclidean distance between two 2D points.

    Args:
        point1: First point as (x, y) tuple
        point2: Second point as (x, y) tuple

    Returns:
        Euclidean distance between the points
    """
    return np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


def calculate_path_weight(graph: nx.Graph, path: Path) -> Weight:
    """Calculate the total weight of a path in a graph.

    Sums the weights of edges along the given path.

    Args:
        graph: Graph containing the path
        path: Sequence of nodes defining the path

    Returns:
        Total weight of all edges in the path
    """
    total_path_weight: Weight = 0.0
    for i in range(len(path) - 1):
        vertex_u, vertex_v = path[i], path[i + 1]
        edge_weight = graph[vertex_u][vertex_v]["weight"]
        total_path_weight += edge_weight

    return total_path_weight


def compute_stats(values: list[float]) -> dict[str, float]:
    """Compute statistics for a list of values.

    Calculates interquartile mean and quartile values.

    Args:
        values: List of numerical values

    Returns:
        Dictionary with interquartile mean (iqm), first quartile (q1), and
        third quartile (q3)
    """
    values = np.array(values)
    q1, q3 = np.percentile(values, [25, 75])

    mask = (values >= q1) & (values <= q3)
    interquartile_values = values[mask]
    iqm = np.mean(interquartile_values)

    mins = np.min(values)
    maxs = np.max(values)

    return {"iqm": iqm, "q1": q1, "q3": q3, "min": mins, "max": maxs}


def edge(u, v):
    """Create a canonical representation of an edge.

    Orders the nodes to ensure consistent edge representation regardless of
    input order.

    Args:
        u: First node
        v: Second node

    Returns:
        Tuple with nodes ordered by increasing value
    """
    return (min(u, v), max(u, v))
