from typing import List, Tuple, Set, TypeVar
import networkx as nx
from networkx.algorithms.matching import min_weight_matching
from networkx.algorithms.euler import eulerian_circuit
import itertools

T = TypeVar("T")
Weight = float
Edge = Tuple[T, T]
Path = List[T]


def christofides_tsp(graph: nx.Graph) -> Tuple[Path, Weight]:
    if not nx.is_connected(graph):
        raise ValueError("Graph must be connected")

    # 1. Calculate a minimum weight spanning tree T of G
    minimum_spanning_tree = nx.minimum_spanning_tree(graph)
    print("MST:")
    for u, v, d in minimum_spanning_tree.edges(data=True):
        print(u, v)

    # 2. Let I be the set of vertices with odd degree in T, calculate a minimum weight perfect matching M in the subgraph induced by the vertices of I
    odd_degree_vertices: List[T] = [
        node for node, degree in minimum_spanning_tree.degree() if degree % 2 == 1
    ]

    # Create the subgraph induces by odd degree vertices
    odd_vertices_subgraph = nx.Graph()
    odd_vertex_pairs = itertools.combinations(odd_degree_vertices, 2)
    for vertex_u, vertex_v in odd_vertex_pairs:
        odd_vertices_subgraph.add_edge(
            vertex_u, vertex_v, weight=graph[vertex_u][vertex_v]["weight"]
        )

    # Find minimum weight perfect matching
    minimum_weight_matching = min_weight_matching(odd_vertices_subgraph)
    print("Perfect matching: ", minimum_weight_matching)

    # 3. Define a multigraph H from the edges of M and T
    eulerian_multigraph = nx.MultiGraph(minimum_spanning_tree)
    for vertex_u, vertex_v in minimum_weight_matching:
        eulerian_multigraph.add_edge(
            vertex_u, vertex_v, weight=graph[vertex_u][vertex_v]["weight"]
        )
    print("Multigraph")
    for u, v, d in eulerian_multigraph.edges(data=True):
        print(u, v)

    # 4. Find a Eulerian cycle in H (H is Eulerian because it is connected and all vertices have even degree)
    eulerian_cycle = list(eulerian_circuit(eulerian_multigraph))
    print("Eulerian cycle:", eulerian_cycle)

    # 5. Transform the Eulerian cycle into a Hamiltonian cycle by removing any double passages on certain vertices
    hamiltonian_cycle = shortcut_eulerian_path([vertex for vertex, _ in eulerian_cycle])
    print("Hamiltonian cycle:", hamiltonian_cycle)

    # Calculate total weight of the tour
    total_tour_weight = calculate_path_weight(graph, hamiltonian_cycle)

    return hamiltonian_cycle, total_tour_weight


def shortcut_eulerian_path(eulerian_path: List[T]) -> Path:
    # Applies the triangle inequality principle implicitly. By skipping repeated vertices, we create direct edges between vertices that were previously connected through intermediary vertices
    already_visited_vertices: Set[T] = set()
    hamiltonian_cycle: List[T] = []

    for vertex in eulerian_path:
        if vertex not in already_visited_vertices:
            already_visited_vertices.add(vertex)
            hamiltonian_cycle.append(vertex)

    # Add the starting vertex to complete the cycle
    if hamiltonian_cycle and hamiltonian_cycle[0] != hamiltonian_cycle[-1]:
        hamiltonian_cycle.append(hamiltonian_cycle[0])

    return hamiltonian_cycle


def calculate_path_weight(graph: nx.Graph, path: List[T]) -> Weight:
    # it is strange that we do not have something better
    if len(path) <= 1:
        return 0.0

    total_path_weight: Weight = 0.0
    for i in range(len(path) - 1):
        vertex_u, vertex_v = path[i], path[i + 1]
        edge_weight = graph[vertex_u][vertex_v]["weight"]
        total_path_weight += edge_weight

    return total_path_weight
