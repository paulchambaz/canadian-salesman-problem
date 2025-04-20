"""Christofides Nearest Neighbour solves constrained TSP with blocked edges.

This module implements the Constrained Nearest Neighbor (CNN) algorithm for
the Covering Canadian Travaller Problem (CCTP) with blocked edges.
"""

import networkx as nx

from .christofides import christofides_tsp
from .types import Edge, Node, Path, Weight
from .utils import calculate_path_weight, edge


def cnn_cctp(
    graph: nx.Graph,
    blocked_edges: set[Edge],
    tour: Path = None,
) -> tuple[Path, Weight]:
    """Find a near-optimal path avoiding blocked edges using CNN.

    Implements a four-phase approach:
    1. Generate initial tour using Christofides algorithm
    2. Shortcut phase: Follow initial tour until blocked edges are encountered
    3. Compression phase: Create exploration graph with unvisited nodes
    4. Exploration phase: Complete tour using nearest neighbor approach

    Args:
        graph: Complete graph with weighted edges
        blocked_edges: Set of edges that cannot be traversed
        tour: Already precomputed Christofides tour (optional)

    Returns:
        Tuple containing the final path and its total weight
    """
    if tour is None:
        # 1. Initial tour using christofides
        tour, _ = christofides_tsp(graph)
    tour.pop()

    # 2. shortcut - follow christofides tour as far as possible then go back to
    # the start
    visited_nodes, unvisited_nodes, known_blocked = shortcut_phase(
        graph, tour, blocked_edges
    )

    # if all nodes are visited, then we can just return since we are done
    if len(unvisited_nodes) == 0:
        final_path = visited_nodes
        total_tour_weight = calculate_path_weight(graph, final_path)
        return final_path, total_tour_weight

    # 3. compress - create exploration graph with unvisited nodes
    exploration_graph = create_exploration_graph(
        graph, visited_nodes, unvisited_nodes, known_blocked
    )

    # 4. explore using nearest neuighbor
    exploration_path = nearest_neighbor(
        exploration_graph, tour[0], blocked_edges
    )

    final_path = visited_nodes + exploration_path
    total_tour_weight = calculate_path_weight(graph, final_path)

    return final_path, total_tour_weight


def get_blocked_edges(u, graph, blocked_edges):
    """Find all blocked edges connected to node u.

    Args:
        u: Node to check for connected blocked edges
        graph: Graph containing the edges
        blocked_edges: Set of all blocked edges

    Returns:
        List of blocked edges connected to node u
    """
    return [
        edge(u, v)
        for v in graph.nodes()
        if u != v and edge(u, v) in blocked_edges
    ]


def shortcut_phase(
    graph: nx.Graph, tour: Path, blocked_edges: set[Edge]
) -> tuple[Path, set[Node], set[Edge], Node]:
    """Follow initial tour until blocked edges are encountered.

    Traverses the initial tour, skipping blocked edges and accumulating
    knowledge about the graph structure.

    Args:
        graph: Graph representation
        tour: Initial tour path
        blocked_edges: Set of edges that cannot be traversed

    Returns:
        Tuple containing visited path, unvisited nodes, and known blocked edges
    """
    start_node = tour[0]
    visited_path = [start_node]
    visited_nodes = {start_node}
    known_blocked = set()

    u = start_node
    known_blocked.update(get_blocked_edges(u, graph, blocked_edges))

    for v in tour[1:] + [tour[0]]:
        if edge(u, v) in blocked_edges:
            continue

        visited_path.append(v)
        visited_nodes.add(v)
        known_blocked.update(get_blocked_edges(v, graph, blocked_edges))
        u = v

    if visited_path[-1] != start_node:
        visited_path = visited_path + visited_path[:-1][::-1]

    unvisited_nodes = set(tour) - visited_nodes
    return visited_path, unvisited_nodes, known_blocked


def create_exploration_graph(
    graph: nx.Graph,
    visited_nodes: Path,
    unvisited_nodes: set[Node],
    known_blocked: set[Edge],
) -> nx.Graph:
    """Create a multigraph for exploring unvisited nodes.

    Builds a graph containing both direct (potentially risky) edges and safe
    paths between nodes that need to be visited.

    Args:
        graph: Original graph
        visited_nodes: Nodes already visited in the shortcut phase
        unvisited_nodes: Nodes that still need to be visited
        known_blocked: Blocked edges discovered during shortcut phase

    Returns:
        MultiGraph containing all possible paths for exploration
    """
    # build correct sets for manipulation
    visited_set = set(visited_nodes)
    all_edges = graph.edges()

    # construct state of things we know and things we do not know
    seen_edges = {
        (u, v) for (u, v) in all_edges if u in visited_set or v in visited_set
    }
    unseen_edges = set(all_edges) - seen_edges

    # build knowledge graph which contains all the knowledge we currenly have
    knowledge_graph = nx.Graph()
    for node in graph.nodes():
        knowledge_graph.add_node(node)

    for u, v in seen_edges:
        # since we have already seen the node, we know whether it is blocked or
        # not
        if (u, v) not in known_blocked:
            knowledge_graph.add_edge(u, v, weight=graph[u][v]["weight"])

    # build exploration graph which contains all the nodes we have yet to
    # visit, as well as the starting node
    start_node = visited_nodes[0]
    nodes_to_explore = unvisited_nodes.union({start_node})

    exploration_graph = nx.MultiGraph()
    for node in nodes_to_explore:
        exploration_graph.add_node(node)

    # add risky paths which might be blocked
    for u, v in unseen_edges:
        exploration_graph.add_edge(
            u, v, weight=graph[u][v]["weight"], path=[u, v], safe=False
        )

    # add safe path which are longer path that pass through the knowledge graph
    unvisited_pairs = [
        (u, v) for u in nodes_to_explore for v in nodes_to_explore if u < v
    ]
    for u, v in unvisited_pairs:
        safe_path = nx.shortest_path(knowledge_graph, u, v, weight="weight")
        path_cost = sum(
            knowledge_graph[safe_path[i]][safe_path[i + 1]]["weight"]
            for i in range(len(safe_path) - 1)
        )
        exploration_graph.add_edge(
            u, v, weight=path_cost, path=safe_path, safe=True
        )

    return exploration_graph


def nearest_neighbor(
    graph: nx.MultiGraph, start_node: Node, blocked_edges: set[Edge]
) -> Path:
    """Find path visiting all nodes using nearest neighbor heuristic.

    Selects next node to visit based on the shortest available path that
    doesn't contain blocked edges.

    Args:
        graph: Exploration graph with multiple path options
        start_node: Starting node for the exploration
        blocked_edges: Set of edges that cannot be traversed

    Returns:
        Path visiting all unvisited nodes and returning to start
    """
    current = start_node
    unvisited = set(graph.nodes()) - {current}
    path = []

    # visit all unvisited nodes
    while unvisited:
        # find next node with best path
        next_path = find_best_path(graph, current, unvisited, blocked_edges)

        # add path to result
        if current == next_path[0]:
            path.extend(next_path[1:])
        else:
            path.extend(reversed(next_path[:-1]))

        current = path[-1]
        unvisited.remove(current)

    return_path = find_best_path(graph, current, {start_node}, blocked_edges)

    path.extend(reversed(return_path[:-1]))

    return path


def find_best_path(
    graph: nx.MultiGraph,
    current: Node,
    target_nodes: set[Node],
    blocked_edges: set[Edge],
) -> Path:
    """Find the best path from current node to one of the target nodes.

    Evaluates all possible paths to target nodes, considering path safety
    and avoiding blocked edges.

    Args:
        graph: MultiGraph containing path options
        current: Current node position
        target_nodes: Set of potential destination nodes
        blocked_edges: Set of edges that cannot be traversed

    Returns:
        Lowest-cost valid path to one of the target nodes
    """
    min_cost = float("inf")
    best_path = []

    for node in target_nodes:
        u, v = edge(current, node)

        for _, data in graph[u][v].items():
            cost = data["weight"]
            path = data["path"]
            is_safe = data["safe"]

            if not is_safe and edge(path[0], path[1]) in blocked_edges:
                continue

            if cost < min_cost:
                min_cost = cost
                best_path = path

    return best_path
