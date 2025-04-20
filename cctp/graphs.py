"""List of helper function to create graphs."""
# TODO: write proper docstring

import math
import random

import networkx as nx

from .types import Edge
from .utils import create_complete_graph_from_points, create_random_graph, edge


def cr_tight_bound_graph(p: int) -> tuple[nx.Graph, set[Edge]]:
    """Create a graph that demonstrates the tight bound for CR algorithm.

    Constructs a graph with three pseudo-nodes and connecting vertices that
    forces CR to take approximately sqrt(k) tours, demonstrating the
    O(sqrt(k))-competitive ratio.

    Args:
        p: Parameter determining the size of the graph

    Returns:
        Tuple containing the graph and the set of blocked edges
    """
    points = []

    total_nodes = int(3 * ((p * (p + 1)) / 2 + 1))
    total_added_nodes = int(total_nodes - 3 * p)
    added_nodes = int(total_added_nodes / 3)

    dist = 1
    index = 0
    index_tiny = 0
    for i in range(total_nodes):
        if (
            (i >= 0 and i < added_nodes)
            or (i >= p + added_nodes and i < 2 * added_nodes + p)
            or (i >= 2 * p + 2 * added_nodes and i < 3 * added_nodes + 2 * p)
        ):
            angle = 2 * math.pi * index / (total_added_nodes + 3)
            points.append((-math.sin(angle) * dist, math.cos(angle) * dist))
            index += 1
            index_tiny = 0
        else:
            angle = (
                2
                * math.pi
                * (index + index_tiny * 0.001)
                / (total_added_nodes + 3)
            )
            points.append((-math.sin(angle) * dist, math.cos(angle) * dist))
            index_tiny += 1
            if index_tiny == p:
                index += 1

    blocked_edges = set()
    for i in range(total_nodes):
        for j in range(total_nodes):
            if i < j:
                blocked_edges.add((i, j))

    golden_path = []
    for j in range(3):
        for i in range(added_nodes):
            golden_path.append(j * (added_nodes + p) + i)

    for i in range(p):
        for j in range(3):
            golden_path.append((3 - j) * added_nodes + (2 - j) * p + i)

    golden_path.append(0)

    remove_blocked_edges = set()
    for i in range(len(golden_path) - 1):
        remove_blocked_edges.add(edge(golden_path[i], golden_path[i + 1]))

    blocked_edges -= remove_blocked_edges

    return create_complete_graph_from_points(points), blocked_edges


def cnn_tight_bound_graph(p: int) -> tuple[nx.Graph, set[Edge]]:
    """Create a graph that demonstrates the tight bound for CNN algorithm.

    Constructs a graph with a chain of triangles and strategic blocked edges
    that forces CNN to take a path with O(log k) approximation ratio.

    Args:
        p: Parameter determining the size of the graph

    Returns:
        Tuple containing the graph and the set of blocked edges
    """
    tight_bound_graph = nx.Graph()

    for i in range(2**p):
        tight_bound_graph.add_node(i, pos=(i, 0))

    for i in range(2**p - 1):
        tight_bound_graph.add_node(2**p + i, pos=(i + 0.5, 1))

    u = 2 ** (p + 1) - 1
    tight_bound_graph.add_node(u, pos=(-1, 0))

    for i in range(2**p - 1):
        tight_bound_graph.add_edge(i, i + 1, weight=1)
        tight_bound_graph.add_edge(i, 2**p + i, weight=1)
        tight_bound_graph.add_edge(i + 1, 2**p + i, weight=1)

    tight_bound_graph.add_edge(u, 0, weight=1)

    blocked_edges = set()

    for v in range(1, u):
        tight_bound_graph.add_edge(v, u, weight=1)
        blocked_edges.add((v, u))

    for i in range(u):
        for j in range(i + 1, u):
            if not tight_bound_graph.has_edge(i, j):
                tight_bound_graph.add_edge(i, j, weight=2)

    return tight_bound_graph, blocked_edges


def create_constant_weight_graph(n: int) -> nx.Graph:
    """Create a complete graph where all edges have the same weight.

    Generates n nodes and connects all pairs with edges of constant weight 1.
    This naturally satisfies the triangle inequality since the direct path
    between any two nodes has the same cost as any indirect path.

    Args:
        n: Number of nodes in the graph

    Returns:
        Complete graph with n nodes and constant edge weights
    """
    graph = nx.complete_graph(n)

    for node in graph.nodes():
        graph.nodes[node]["pos"] = (random.random(), random.random())

    for u, v in graph.edges():
        graph[u][v]["weight"] = 1.0

    return graph


def create_euclidian_graph(n: int) -> nx.Graph:
    """Create a complete graph with randomly positioned nodes.

    Generates n nodes with random x,y coordinates within the specified range and
    connects all nodes with edges weighted by their Euclidean distance.

    Args:
        n: Number of nodes in the graph

    Returns:
        Complete graph with n randomly positioned nodes
    """
    return create_random_graph(n)


def create_manhattan_graph(n: int) -> nx.Graph:
    """Create a graph based on a 2D grid with Manhattan distances.

    Generates a grid of n^2 nodes arranged in an n times n grid, where nodes are
    connected to their grid neighbors. Additional edges connect non-neighbor
    nodes with weights equal to their Manhattan distance, ensuring strict
    triangle inequality.

    Args:
        n: Width/height of the grid (resulting in n times n total nodes)

    Returns:
        Complete graph with Manhattan distances that strictly respects triangle
        inequality
    """
    grid = nx.grid_2d_graph(n, n)

    graph = nx.Graph()
    pos = {}
    node_mapping = {}

    for i, (x, y) in enumerate(grid.nodes()):
        graph.add_node(i)
        pos[i] = (x, y)
        node_mapping[(x, y)] = i

    for i in range(len(graph)):
        x1, y1 = pos[i]
        for j in range(i + 1, len(graph)):
            x2, y2 = pos[j]
            manhattan_dist = abs(x1 - x2) + abs(y1 - y2)
            graph.add_edge(i, j, weight=float(manhattan_dist))

    nx.set_node_attributes(graph, pos, "pos")

    return graph


def create_clustered_graph(
    n: int, intra_weight: float = 1.0, inter_multiplier: float = 20.0
) -> nx.Graph:
    """Create a strongly clustered graph with n clusters of n nodes each.

    Generates a graph with n clusters, each containing n nodes. Clusters are
    positioned randomly with centers far apart, and nodes within each cluster
    are positioned close to their cluster center.

    Args:
        n: Number of clusters and number of nodes per cluster
        intra_weight: Max distance of nodes from cluster center (default: 1.0)
        inter_multiplier: Scale factor for distance between cluster centers
        (default: 20.0)

    Returns:
        Complete graph with clustered nodes
    """
    cluster_centers = [
        (
            random.uniform(-inter_multiplier, inter_multiplier),
            random.uniform(-inter_multiplier, inter_multiplier),
        )
        for _ in range(n)
    ]

    points = []
    for center_x, center_y in cluster_centers:
        for _ in range(n):
            x = center_x + random.uniform(-intra_weight, intra_weight)
            y = center_y + random.uniform(-intra_weight, intra_weight)
            points.append((x, y))

    return create_complete_graph_from_points(points)


def create_power_law_graph(n: int, exponent: float = 2.5) -> nx.Graph:
    """Create a graph with weights based on power-law distribution.

    Generates a complete graph where node positions follow a power-law
    distribution, resulting in some nodes being central (hubs) and others being
    peripheral. Edge weights are based on Euclidean distances, preserving
    triangle inequality.

    Args:
        n: Number of nodes in the graph
        exponent: Power-law exponent (default: 2.5)

    Returns:
        Graph with power-law structure that respects triangle inequality
    """
    points = []
    for i in range(n):
        distance = ((i + 1) / n) ** (1 / exponent) * 10
        angle = random.uniform(0, 2 * math.pi)
        x = distance * math.cos(angle)
        y = distance * math.sin(angle)
        points.append((x, y))

    return create_complete_graph_from_points(points)
