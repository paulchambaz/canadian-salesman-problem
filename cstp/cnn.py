from typing import List, Set, Tuple
import networkx as nx
from .utils import calculate_path_weight, edge
from .christofides import christofides_tsp
from .types import T, Weight, Edge, Path


def cnn_cctp(graph: nx.Graph, blocked_edges: Set[Edge] = None) -> Tuple[Path, Weight]:
    # print(f"{blocked_edges=}")

    # 1. Initial tour using christofides
    tour, _ = christofides_tsp(graph)
    tour.pop()
    # print(f"initial christofides tour: {tour}")

    # 2. shortcut - follow christofides tour as far as possible then go back to the start
    visited_nodes, unvisited_nodes, known_blocked = shortcut_phase(
        graph, tour, blocked_edges
    )
    # print(f"{visited_nodes=}")
    # print(f"{unvisited_nodes=}")
    # print(f"{known_blocked=}")

    # if all nodes are visited, then we can just return since we are done
    if len(unvisited_nodes) == 0:
        final_path = visited_nodes
        total_tour_weight = calculate_path_weight(graph, final_path)
        return final_path, total_tour_weight

    # 3. compress - create reduced graph with unvisited nodes
    explore_graph = exploration_graph(
        graph, visited_nodes, unvisited_nodes, known_blocked
    )

    # 4. explore using nearest neuighbor
    exploration_path = nearest_neighbor(explore_graph, tour[0], blocked_edges)

    # print(f"{visited_nodes=}")
    # print(f"{exploration_path=}")

    final_path = visited_nodes + exploration_path
    total_tour_weight = calculate_path_weight(graph, final_path)

    # print(f"{final_path=}")
    return final_path, total_tour_weight


def get_blocked_edges(u, graph, blocked_edges):
    return [edge(u, v) for v in graph.nodes() if u != v and edge(u, v) in blocked_edges]


def shortcut_phase(
    graph: nx.Graph, tour: Path, blocked_edges: Set[Edge]
) -> Tuple[Path, Set[T], Set[Edge], T]:
    start_node = tour[0]
    visited_path = [start_node]
    visited_nodes = {start_node}
    known_blocked = set()

    u = start_node
    known_blocked.update(get_blocked_edges(u, graph, blocked_edges))

    for v in tour[1:] + [tour[0]]:
        if edge(u, v) in blocked_edges:
            continue
        else:
            visited_path.append(v)
            visited_nodes.add(v)
            known_blocked.update(get_blocked_edges(v, graph, blocked_edges))
            u = v

    if visited_path[-1] != start_node:
        visited_path = visited_path + visited_path[:-1][::-1]

    unvisited_nodes = set(tour) - visited_nodes
    return visited_path, unvisited_nodes, known_blocked


def exploration_graph(
    graph: nx.Graph,
    visited_nodes: List[T],
    unvisited_nodes: Set[T],
    known_blocked: Set[Edge],
) -> nx.Graph:
    start_node = visited_nodes[0]

    nodes = graph.nodes()
    us_nodes = unvisited_nodes.union({start_node})

    seen = set(visited_nodes)
    edges = [edge(u, v) for u in graph.nodes() for v in graph.nodes() if u < v]
    unseen_edges = [
        edge(u, v) for (u, v) in edges if u < v and u not in seen and v not in seen
    ]
    seen_edges = set(edges) - set(unseen_edges)

    knowledge_graph = nx.Graph()
    for node in nodes:
        knowledge_graph.add_node(node)

    for u, v in seen_edges:
        if (u, v) not in known_blocked:
            knowledge_graph.add_edge(u, v, weight=graph[u][v]["weight"])

    # print(f"{knowledge_graph.nodes()=}")
    # print(f"{knowledge_graph.edges()=}")

    exploration_graph = nx.MultiGraph()
    for node in us_nodes:
        exploration_graph.add_node(node)

    for u, v in unseen_edges:
        exploration_graph.add_edge(u, v, weight=graph[u][v]["weight"], path=[u, v])

    us_pairs = [(u, v) for u in us_nodes for v in us_nodes if u < v]

    for u, v in us_pairs:
        safe_path = nx.shortest_path(knowledge_graph, u, v, weight="weight")
        cost = sum(
            knowledge_graph[safe_path[i]][safe_path[i + 1]]["weight"]
            for i in range(len(safe_path) - 1)
        )
        # print(safe_path)
        exploration_graph.add_edge(u, v, weight=cost, path=safe_path)

    # print(f"{exploration_graph.nodes()=}")
    # print(f"{exploration_graph.edges()=}")

    return exploration_graph


def nearest_neighbor(
    graph: nx.MultiGraph, start_node: T, blocked_edges: Set[Edge]
) -> Path:
    current = start_node
    unvisited = set(graph.nodes()) - {current}
    path = []

    while unvisited:
        min_cost = float("inf")
        min_path = []
        for node in unvisited:
            u, v = edge(current, node)
            for _, data in graph[u][v].items():
                current_cost = data["weight"]
                current_path = data["path"]

                if (
                    len(current_path) == 2
                    and edge(current_path[0], current_path[1]) in blocked_edges
                ):
                    continue

                if current_cost < min_cost:
                    min_cost = current_cost
                    min_path = current_path

        if current == min_path[0]:
            path.extend(min_path[1:])
        else:
            path.extend(reversed(min_path[:-1]))

        current = path[-1]
        unvisited = unvisited - {current}

    min_cost = float("inf")
    min_path = []
    for _, data in graph[start_node][current].items():
        current_cost = data["weight"]
        current_path = data["path"]

        if (
            len(current_path) == 2
            and edge(current_path[0], current_path[1]) in blocked_edges
        ):
            continue

        if current_cost < min_cost:
            min_cost = current_cost
            min_path = current_path

    path.extend(reversed(min_path[:-1]))

    return path
