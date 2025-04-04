from typing import List, Set, Tuple
import networkx as nx
from .utils import calculate_path_weight
from .christofides import christofides_tsp
from .types import T, Weight, Edge, Path


def cnn_cctp(graph: nx.Graph, blocked_edges: Set[Edge] = None) -> Tuple[Path, Weight]:
    print(f"{blocked_edges=}")

    # 1. Initial tour using christofides
    tour, _ = christofides_tsp(graph)
    tour.pop()
    print(f"{tour=}")

    # 2. shortcut - follow christofides tour as far as possible then go back to the start
    visited_nodes, unvisited_nodes, known_blocked = shortcut_phase(
        graph, tour, blocked_edges
    )
    print(f"{visited_nodes=}")
    print(f"{unvisited_nodes=}")
    print(f"{known_blocked=}")

    # if all nodes are visited, then we can just return since we are done
    if not unvisited_nodes:
        final_path = visited_nodes
        total_tour_weight = calculate_path_weight(graph, final_path)
        return final_path, total_tour_weight

    # 3. compress - create reduced graph with unvisited nodes
    compressed_graph = compress_graph(
        graph, visited_nodes, unvisited_nodes, known_blocked
    )

    # 4. explore using nearest neuighbor
    exploration_path = nearest_neighbor(compressed_graph, start_node=tour[0])

    # expand paths in the compressed graph to actual paths in the original graph
    final_path = expand_compressed_path(graph, exploration_path, known_blocked)

    return final_path, calculate_path_weight(graph, final_path)


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
        edge = (min(u, v), max(u, v))

        if edge in blocked_edges:
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


def get_blocked_edges(u, graph, blocked_edges):
    return [
        (min(u, v), max(u, v))
        for v in graph.nodes()
        if u != v and (min(u, v), max(u, v)) in blocked_edges
    ]


def compress_graph(
    graph: nx.Graph,
    visited_nodes: List[T],
    unvisited_nodes: Set[T],
    known_blocked: Set[Edge],
) -> nx.Graph:
    # in this function we want to build the compressed graph, which will first involve buidling the safe graph, in many ways the safe graph is a little bit harder to create than the compressed graph. so here is how to do both.
    # for the safe graph, we should include each and every of the nodes present in the initial graph. then we want to remove nodes, first, of course, we want to remove all the nodes that have never been seen, ie, neither nodes adjacent to the edge are present in the visited_nodes list. then once we've removed all of these, we still need to remove the blocked nodes, ie the nodes that are present in the known_blocked list (make sure to min max properly to have good matches)
    # once we have the safe graph, it is actually pretty easy, we just need to create a new graph, which contains only the unvisited_nodes U {start_node}, as we already have. then we want to add all the edges adjacent to the nodes from the initial graph. then we are not done, we need to make the last, slightly complex element. we want to recompute each and every edge (u, v) in this graph and add a new edge between u and v, we will call this edge the safe edge. how do we compute the safe edge, we just add it with a cost. what is the cost ? it is the length of the shortest path between u and v in the safe graph. since we search in the safe graph, we have a garantee to have a path (i think we will make an exception that asserts and panics if that is not the case since we will need to study this usecase). when we compute that cost, we also want to store the full path (we will expand this at the end properly, but for now we just want to keep the references in a table (so for example we will have {(3, 4): (3, 1, 4)} like a Dict[Edge, List[T]] which we will be able to use at the very end. remember compressed graph is a multigraph that possess both a potential fast route AND the safe route (and sometimes they can be indentical, but we still want both). between each two nodes there should be two edges

    start_node = visited_nodes[0]
    us_nodes = unvisited_nodes.union({start_node})

    safe_graph = graph.copy()
    for u, v in known_blocked:
        if safe_graph.has_edge(u, v):
            safe_graph.remove_edge(u, v)

    compressed = nx.Graph()

    for node in us_nodes:
        compressed.add_node(node)

    for u in us_nodes:
        for v in us_nodes:
            if u < v:
                if graph.has_edge(u, v):
                    compressed.add_edge(
                        u, v, weight=graph[u][v]["weight"], original=True
                    )

                try:
                    path = nx.shortest_path(safe_graph, u, v, weight="weight")
                    path_weight = sum(
                        safe_graph[path[i]][path[i + 1]]["weight"]
                        for i in range(len(path) - 1)
                    )
                    if (
                        not compressed.has_edge(u, v)
                        or path_weight < compressed[u][v]["weight"]
                    ):
                        compressed.add_edge(
                            u, v, weight=path_weight, original=False, safe_path=path
                        )
                except nx.NetworkXNoPath:
                    assert "This is very strange we were not able to find a path"

    return compressed


def nearest_neighbor(graph: nx.Graph, start_node: T) -> Path:
    # here we should know if we take the safe route or the fast route at each point, its very simple, if the fast route exists, we take it, if not we take the safe route. we take the path that has the minimum distance between all available nodes. when we return we should keep just enough information so that we can know whether or not we took the safe route or the fast route and can therefore expand them properly later
    current = start_node
    unvisited = set(graph.nodes()) - {current}
    path = [current]

    while unvisited:
        next_node = min(
            unvisited,
            key=lambda n: graph[current][n]["weight"]
            if graph.has_edge(current, n)
            else float("inf"),
        )

        path.append(next_node)
        unvisited.remove(next_node)
        current = next_node

    path.append(start_node)
    return path


def expand_compressed_path(
    graph: nx.Graph, compressed_path: Path, known_blocked: Set[Tuple[T, T]]
) -> Path:
    expanded_path = [compressed_path[0]]

    for i in range(len(compressed_path) - 1):
        u, v = compressed_path[i], compressed_path[i + 1]

        edge = (min(u, v), max(u, v))
        if edge not in known_blocked:
            expanded_path.append(v)
        else:
            safe_graph = graph.copy()
            for blocked_u, blocked_v in known_blocked:
                if safe_graph.has_edge(blocked_u, blocked_v):
                    safe_graph.remove_edge(blocked_u, blocked_v)

            path = nx.shortest_path(safe_graph, u, v, weight="weight")
            expanded_path.extend(path[1:])

    return expanded_path
