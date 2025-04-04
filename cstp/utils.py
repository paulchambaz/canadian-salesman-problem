from typing import Dict, List, Tuple, Callable, Any, Set
import networkx as nx
import numpy as np
import random
import time
import math
from tqdm import tqdm
from .types import T, Weight, Edge


def create_polygon_graph(n: int, low: float = 5.0, high: float = 5.0) -> nx.Graph:
    points = []
    for i in range(n):
        angle = 2 * math.pi * i / n
        x = high * math.sin(angle)
        y = high * math.cos(angle)
        points.append((x, y))
    return create_complete_graph_from_points(points)


def create_random_graph(n: int, low: float = -5.0, high: float = 5.0) -> nx.Graph:
    points = [(random.uniform(low, high), random.uniform(low, high)) for _ in range(n)]
    return create_complete_graph_from_points(points)


def create_random_blocks(n: int, graph: nx.Graph) -> Set[Edge]:
    edges = list(graph.edges())
    blocked_edges = set()
    for _ in range(n):
        edge = random.choice(edges)
        blocked_edges.add((min(edge), max(edge)))
        edges.remove(edge)
    return blocked_edges


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


def calculate_path_weight(graph: nx.Graph, path: List[T]) -> Weight:
    total_path_weight: Weight = 0.0
    for i in range(len(path) - 1):
        vertex_u, vertex_v = path[i], path[i + 1]
        edge_weight = graph[vertex_u][vertex_v]["weight"]
        total_path_weight += edge_weight

    return total_path_weight


def compute_stats(values: List[float]) -> Dict[str, float]:
    values = np.array(values)
    q1, q3 = np.percentile(values, [25, 75])

    mask = (values >= q1) & (values <= q3)
    interquartile_values = values[mask]
    iqm = np.mean(interquartile_values)

    return {"iqm": iqm, "q1": q1, "q3": q3}


def measure_runtime(
    function: Callable[[], Any],
    n: int,
    repeats: int = 15,
) -> Dict:
    runtimes = []
    for _ in tqdm(range(repeats), desc=f"Testing n={n}", leave=False):
        start = time.time()
        function()
        runtimes.append(time.time() - start)

    stats = compute_stats(runtimes)
    return {**stats, "runtimes": runtimes}
