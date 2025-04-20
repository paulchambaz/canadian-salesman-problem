"""Implements the Christofides algorithm for approximating TSP solutions.

This module provides an implementation of the Christofides algorithm, a
polynomial-time approximation algorithm for the Traveling Salesman Problem (TSP)
that guarantees solutions within 1.5 times the optimal solution for metric TSPs.
"""

import itertools

import networkx as nx
from networkx.algorithms.euler import eulerian_circuit
from networkx.algorithms.matching import min_weight_matching

from .types import Node, Path, Weight
from .utils import calculate_path_weight


def christofides_tsp(graph: nx.Graph) -> tuple[Path, Weight]:
    """Solve TSP approximately using the Christofides algorithm.

    Implements the Christofides approximation algorithm which guarantees a tour
    with weight at most 1.5 times the optimal solution when the graph satisfies
    the triangle inequality. The algorithm works through five main steps:

    1. Find a minimum spanning tree
    2. Identify vertices with odd degree and compute minimum weight matching
    3. Combine the MST and matching to form an Eulerian multigraph
    4. Find an Eulerian circuit in this multigraph
    5. Convert to a Hamiltonian cycle by shortcutting

    Args:
        graph: Undirected weighted graph where edges have a 'weight' attribute

    Returns:
        A tuple containing the Hamiltonian cycle as a list of nodes and the
        total weight of the tour
    """
    # 1. Calculate a minimum weight spanning tree T of G
    minimum_spanning_tree = nx.minimum_spanning_tree(graph)

    # 2. Let I be the set of vertices with odd degree in T, calculate a minimum
    # weight perfect matching M in the subgraph induced by the vertices of I
    odd_degree_vertices: list[Node] = [
        node
        for node, degree in minimum_spanning_tree.degree()
        if degree % 2 == 1
    ]

    # Create the subgraph induces by I
    odd_vertices_subgraph = nx.Graph()
    odd_vertex_pairs = itertools.combinations(odd_degree_vertices, 2)
    for vertex_u, vertex_v in odd_vertex_pairs:
        odd_vertices_subgraph.add_edge(
            vertex_u, vertex_v, weight=graph[vertex_u][vertex_v]["weight"]
        )

    # Find minimum weight perfect matching
    minimum_weight_matching = min_weight_matching(odd_vertices_subgraph)

    # 3. Define a multigraph H from the edges of M and T
    eulerian_multigraph = nx.MultiGraph(minimum_spanning_tree)
    for vertex_u, vertex_v in minimum_weight_matching:
        eulerian_multigraph.add_edge(
            vertex_u, vertex_v, weight=graph[vertex_u][vertex_v]["weight"]
        )

    # 4. Find a Eulerian cycle in H (H is Eulerian because it is connected and
    # all vertices have even degree)
    eulerian_cycle = list(eulerian_circuit(eulerian_multigraph))

    # 5. Transform the Eulerian cycle into a Hamiltonian cycle by removing any
    # double passages on certain vertices
    hamiltonian_cycle = shortcut_eulerian_path(
        [vertex for vertex, _ in eulerian_cycle]
    )

    # Calculate total weight of the tour
    total_tour_weight = calculate_path_weight(graph, hamiltonian_cycle)

    return hamiltonian_cycle, total_tour_weight


def shortcut_eulerian_path(eulerian_path: list[Node]) -> Path:
    """Convert an Eulerian path to a Hamiltonian cycle via shortcutting.

    Takes an Eulerian path and removes repeated vertices to create a Hamiltonian
    cycle. This implicitly applies the triangle inequality by replacing paths
    through intermediary vertices with direct edges between non-repeated
    vertices.

    Args:
        eulerian_path: List of nodes forming an Eulerian path

    Returns:
        A Hamiltonian cycle (Path) with no repeated vertices except the first
        and last which should be identical
    """
    already_visited_vertices: set[Node] = set()
    hamiltonian_cycle: list[Node] = []

    for vertex in eulerian_path:
        if vertex not in already_visited_vertices:
            already_visited_vertices.add(vertex)
            hamiltonian_cycle.append(vertex)

    # Add the starting vertex to complete the cycle
    if hamiltonian_cycle and hamiltonian_cycle[0] != hamiltonian_cycle[-1]:
        hamiltonian_cycle.append(hamiltonian_cycle[0])

    return hamiltonian_cycle
