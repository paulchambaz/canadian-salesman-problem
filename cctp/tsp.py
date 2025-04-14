"""Find the optimal solution to TSP using brute force enumeration.

This module implements a brute force approach to solve the Traveling Salesman
Problem exactly by examining all possible permutations of vertices.
"""

from itertools import permutations

import networkx as nx

from .types import Path, Weight
from .utils import calculate_path_weight


def optimal_tsp(graph: nx.Graph) -> tuple[Path, Weight]:
    """Find the optimal TSP solution by evaluating all possible paths.

    Computes the exact solution to the Traveling Salesman Problem by generating
    all permutations of vertices and selecting the lowest-cost tour. This
    approach guarantees optimality but has factorial time complexity O(n!).

    Args:
        graph: Undirected weighted graph where edges have a 'weight' attribute

    Returns:
        A tuple containing the optimal path as a list of nodes and its total
        weight, where the path starts at the first node but doesn't repeat it
    """
    nodes = list(graph.nodes())

    best_path = None
    best_cost = float("inf")

    for perm in permutations(nodes[1:]):
        path = [nodes[0]] + list(perm) + [nodes[0]]

        cost = calculate_path_weight(graph, path)

        if cost < best_cost:
            best_cost = cost
            best_path = path[:-1]

    return best_path, best_cost
