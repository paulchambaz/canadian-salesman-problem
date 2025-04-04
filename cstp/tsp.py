from typing import Tuple
import networkx as nx
from itertools import permutations
from .utils import calculate_path_weight
from .types import Weight, Path


def optimal_tsp(graph: nx.Graph) -> Tuple[Path, Weight]:
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
