import random

import networkx as nx
import numpy as np
from .types import *


def generer_graphe_tsp(n: int) -> nx.Graph:
    # Générer des positions aléatoires dans un espace 2D
    positions = {i: np.random.rand(2) for i in range(n)}

    # Créer un graphe complet respectant l'inégalité triangulaire
    G = nx.complete_graph(n)
    for i in range(n):
        for j in range(i + 1, n):
            # Calculer la distance euclidienne entre les points
            poids = np.linalg.norm(positions[i] - positions[j]) * 10
            G[i][j]["weight"] = poids
            G[j][i]["weight"] = poids  # Graphe non orienté

    return G


def generer_blockages(G: nx.Graph, percentage: float=0.5) -> Edge_Path:
    """Randomly generates blocked edges in a graph based on a given percentage.

    This function selects a subset of edges from the graph `G` to be marked as blocked. 
    The number of blocked edges is determined by the given percentage of the total 
    number of edges in the graph.

    Args:
        G: An undirected graph (nx.Graph) from which to select blocked edges.
        percentage: A float between 0 and 1 indicating the proportion of edges to block. 
                    Default is 0.5 (i.e., 50% of edges are blocked).

    Returns:
        A list of edges (Edge_Path) that have been randomly selected to be blocked.
    """
    edge_list = list(G.edges())
    return [edge for edge in edge_list if random.random() <= percentage]

def calculate_path_weight(graph: nx.Graph, path: Edge_Path)->Weight:
    """Calculate the total weight of a path in a graph.

    Sums the weights of edges along the given path.

    Args:
        graph: Graph containing the path
        path: Sequence of Edges defining the path

    Returns:
        Total weight of all edges in the path
    """
    total_path_weight = 0.0
    for edge in path:
        edge_weight = graph[edge[0]][edge[1]]["weight"]
        total_path_weight += edge_weight

    return total_path_weight