import networkx as nx
from cstp import graph_utils
from .types import *

def travelling_salesman_christofides(G: nx.Graph) -> tuple[Edge_Path, Weight]:
    """Approximates a solution to the Travelling Salesman Problem using Christofides' algorithm.

    This function implements Christofides' algorithm to compute a near-optimal solution 
    to the symmetric Travelling Salesman Problem (TSP) on a given undirected, weighted graph 
    that satisfies the triangle inequality.

    Args:
        G: An undirected, weighted graph (nx.Graph) where edge weights represent distances 
           and satisfy the triangle inequality.

    Returns:
        A tuple containing:
            - A list of edges (Edge_Path) forming a Hamiltonian cycle that approximates the TSP solution.
            - The total weight (Weight) of the cycle.
    """
    # arbre couvrante poids min
    T = nx.minimum_spanning_tree(G)

    O = [node for node in T.nodes if T.degree[node] % 2 != 0]
    sub_G = G.subgraph(O)

    M = nx.algorithms.matching.min_weight_matching(sub_G)
    assert nx.algorithms.is_perfect_matching(sub_G, M)
    H1 = G.edge_subgraph(list(M))
    H2 = G.edge_subgraph(list(T.edges))

    # Create a new MultiGraph and combine
    H = nx.MultiGraph()
    H.add_edges_from(H1.edges(data=True))
    H.add_edges_from(H2.edges(data=True))

    EH = nx.MultiGraph(nx.algorithms.eulerian_circuit(H))

    # shortcutting
    visited = []
    edges = []
    for edge in nx.algorithms.eulerian_circuit(H):
        if edge[0] not in visited:
            visited.append(edge[0])
            edges.append(edge)

    # créer graphe final
    edge_list_tsp = [
        (visited[i], visited[i + 1]) for i in range(len(visited) - 1)
    ]
    edge_list_tsp.append((visited[-1], visited[0]))

    final_G = G.edge_subgraph(edge_list_tsp)

    return edge_list_tsp, final_G.size(weight="weight")