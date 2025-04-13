import networkx as nx

from .types import Edge


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
                # blocked_edges.add((i, j))

    return tight_bound_graph, blocked_edges
