"""Cyclic Routing algorithm for solving TSP with blocked edges.

This module implements the Cyclic Routing (CR) algorithm for the
Covering Canadian Travaller Problem (CCTP), which solves
TSP problems with a subset of edges that cannot be traversed.
"""

import networkx as nx

from .christofides import christofides_tsp
from .types import Edge, Node, Path, Weight
from .utils import calculate_path_weight, edge


def cr_cctp(
    graph: nx.Graph, blocked_edges: set[Edge], tour: Path = None
) -> tuple[Path, Weight]:
    """Find a near-optimal path avoiding blocked edges using CR.

    Implements a three-phase approach:
    1. Create a directed graph from an initial Christofides tour
    2. Apply shortcutting operations to avoid blocked edges
    3. Traverse the graph using alternating directions when necessary

    Args:
        graph: Complete graph with weighted edges
        blocked_edges: Set of edges that cannot be traversed
        tour: Already precomputed Christofides tour (optional)

    Returns:
        Tuple containing the final path and its total weight
    """
    # Initialize the tour if not provided
    if tour is None:
        tour, _ = christofides_tsp(graph)
    tour.pop()  # Remove last node (duplicate of first for closed tour)

    # Convert tour to indexed pairs for processing
    full_tour = [(i, tour[i]) for i in range(len(tour))]

    # Find all tour segments using iterative shortcutting
    tours = find_tour_segments(blocked_edges, full_tour)

    # Add final return path if needed
    tours = complete_tour_if_needed(blocked_edges, tours, full_tour)

    # Construct final path from tour segments
    final_path = construct_final_path(tours, full_tour)

    # Calculate total weight and return
    total_tour_weight = calculate_path_weight(graph, final_path)
    return final_path, total_tour_weight


def find_tour_segments(
    blocked_edges: set[Edge], full_tour: list[tuple[int, Node]]
) -> list[list[tuple[int, Node]]]:
    """Find all tour segments through iterative shortcutting.

    Repeatedly applies the shortcut algorithm with direction changes
    to find paths through the graph avoiding blocked edges.

    Args:
        graph: Graph with weighted edges
        blocked_edges: Set of edges that cannot be traversed
        full_tour: Complete initial tour with indices

    Returns:
        List of tour segments
    """
    to_visit = full_tour.copy()
    reverse = False
    direction = 1
    tours = []

    # Process tour segments until all nodes are visited
    while to_visit:
        current_tour = shortcut(
            blocked_edges, to_visit.copy(), full_tour, direction
        )

        if len(current_tour) > 1:
            tours.append(current_tour)

        unvisited = [e for e in to_visit if e not in current_tour]

        if not unvisited:
            break

        # Update direction and to_visit for next iteration
        direction, to_visit = update_traversal_direction(
            current_tour, to_visit, unvisited, reverse
        )

    return tours


def update_traversal_direction(
    current_tour: list[tuple[int, Node]],
    to_visit: list[tuple[int, Node]],
    unvisited: list[tuple[int, Node]],
    reverse: bool,
) -> tuple[int, list[tuple[int, Node]]]:
    """Update the traversal direction and nodes to visit.

    Determines whether to reverse direction and restructures
    the list of nodes to visit accordingly.

    Args:
        current_tour: Current tour segment
        to_visit: Current list of nodes to visit
        unvisited: Nodes not yet visited in current iteration
        reverse: Current reversal state

    Returns:
        Tuple of (new direction, new nodes to visit)
    """
    # Determine if direction needs to be reversed for next segment
    should_reverse = (
        current_tour[-1][0] != to_visit[-1][0] or len(current_tour) == 1
    )

    # Update reversal state
    new_reverse = reverse != should_reverse
    direction = -1 if new_reverse else 1

    # Restructure remaining nodes to visit based on current position
    if should_reverse:
        lower = [(i, u) for (i, u) in unvisited if i < current_tour[-1][0]]
        higher = [(i, u) for (i, u) in unvisited if i > current_tour[-1][0]]
        new_to_visit = [current_tour[-1]] + lower[::-1] + higher[::-1]
    else:
        new_to_visit = [current_tour[-1]] + unvisited

    return direction, new_to_visit


def complete_tour_if_needed(
    blocked_edges: set[Edge],
    tours: list[list[tuple[int, Node]]],
    full_tour: list[tuple[int, Node]],
) -> list[list[tuple[int, Node]]]:
    """Add a return path to complete the tour if necessary.

    Checks if the last node in the tour connects back to the first,
    and if not, finds a path to complete the cycle.

    Args:
        graph: Graph with weighted edges
        blocked_edges: Set of edges that cannot be traversed
        tours: List of tour segments found so far
        full_tour: Complete initial tour with indices

    Returns:
        Updated list of tour segments
    """
    if tours and tours[-1][-1][1] != full_tour[0][1]:
        final_shortcut = add_return_path(
            blocked_edges, tours[-1][-1], full_tour[0], full_tour
        )
        if final_shortcut:
            tours.append(final_shortcut)

    return tours


def construct_final_path(
    tours: list[list[tuple[int, Node]]], full_tour: list[tuple[int, Node]]
) -> Path:
    """Construct the final path from tour segments.

    Combines all tour segments into a single path, ensuring it forms
    a complete cycle returning to the starting node.

    Args:
        tours: List of tour segments
        full_tour: Complete initial tour with indices

    Returns:
        Final path as a list of nodes
    """
    final_path = [full_tour[0][1]]  # Start with the first node

    # Add nodes from each tour segment
    for tour_segment in tours:
        for _, node in tour_segment[1:]:
            final_path.append(node)

    # Ensure tour is closed (ends at the starting node)
    if final_path[-1] != final_path[0]:
        final_path.append(final_path[0])

    return final_path


def shortcut(
    blocked_edges: set[Edge],
    to_visit: list[tuple[int, Node]],
    tour: list[tuple[int, Node]],
    direction: int,
) -> list[tuple[int, Node]]:
    """Find a path through nodes in to_visit that avoids blocked edges.

    Creates a tour segment by traversing nodes while finding alternatives
    when blocked edges are encountered.

    Args:
        graph: Graph with weighted edges
        blocked_edges: Set of edges that cannot be traversed
        to_visit: List of nodes to visit with their indices
        tour: Complete initial tour with indices
        direction: Direction of traversal (1: forward, -1: backward)

    Returns:
        List of visited nodes with their indices
    """
    current_tour = []

    current_index, current_node = to_visit.pop(0)
    current_tour.append(get_node_tour(current_index, tour))

    while to_visit:
        next_index, next_node = to_visit.pop(0)

        if edge(current_node, next_node) in blocked_edges:
            # Edge is blocked, find alternative path
            alternate_path = find_alternate_path(
                blocked_edges,
                (current_index, current_node),
                (next_index, next_node),
                tour,
                direction,
            )

            if alternate_path:
                # Add intermediate nodes from alternate path
                for idx, _ in alternate_path[1:-1]:
                    current_tour.append(get_node_tour(idx, tour))
                current_tour.append(get_node_tour(next_index, tour))
                current_index = next_index
                current_node = next_node
            else:
                # No alternate path found, skip this node
                continue
        else:
            # Direct edge available, add next node to tour
            current_tour.append(get_node_tour(next_index, tour))
            current_index = next_index
            current_node = next_node

    return current_tour


def find_alternate_path(
    blocked_edges: set[Edge],
    start_pair: tuple[int, Node],
    end_pair: tuple[int, Node],
    tour: list[tuple[int, Node]],
    direction: int,
) -> list[tuple[int, Node]]:
    """Find an alternate path between two nodes when direct edge is blocked.

    Searches for a valid two-edge path through another node in the tour
    that avoids blocked edges.

    Args:
        blocked_edges: Set of edges that cannot be traversed
        start_pair: (index, node) of starting node in tour
        end_pair: (index, node) of ending node in tour
        tour: Complete initial tour with indices
        direction: Direction of traversal

    Returns:
        List of nodes forming alternate path, or empty list if none found
    """
    start_index, start_node = start_pair
    end_index, end_node = end_pair

    # Reorder tour nodes based on direction and starting position
    cycle = tour.copy()[::direction]
    passed = False
    lower = []
    higher = []

    # Split the tour into nodes before and after the start node
    for i, u in cycle:
        if passed:
            higher.append((i, u))
        else:
            lower.append((i, u))

        if i == start_index:
            passed = True

    # Reconstruct cycle with start node's position considered
    cycle = higher + lower

    # Extract nodes up to end node
    final_cycle = []
    for i, u in cycle:
        if i == end_index:
            break
        final_cycle.append((i, u))
    cycle = final_cycle.copy()

    # Try to find a node that can form a valid path
    for i, v in cycle:
        if (
            edge(start_node, v) not in blocked_edges
            and edge(v, end_node) not in blocked_edges
        ):
            return [(start_index, start_node), (i, v), (end_index, end_node)]

    return []


def add_return_path(
    blocked_edges: set[Edge],
    start_pair: tuple[int, Node],
    end_pair: tuple[int, Node],
    tour: list[tuple[int, Node]],
) -> list[tuple[int, Node]]:
    """Create a path from the last node back to the starting node.

    Attempts to find a direct or alternate path to complete the tour.

    Args:
        graph: Graph with weighted edges
        blocked_edges: Set of edges that cannot be traversed
        start_pair: (index, node) of last node in current tour
        end_pair: (index, node) of first node in original tour
        tour: Complete initial tour with indices

    Returns:
        List of nodes forming return path, or empty list if none found
    """
    start_idx, start_node = start_pair
    end_idx, end_node = end_pair

    # Check if direct edge is available
    if edge(start_node, end_node) not in blocked_edges:
        return [start_pair, end_pair]

    # Try to find an alternate path in forward direction
    path = find_alternate_path(
        blocked_edges, (start_idx, start_node), (end_idx, end_node), tour, 1
    )

    # If no path found, try reverse direction
    if not path:
        path = find_alternate_path(
            blocked_edges,
            (start_idx, start_node),
            (end_idx, end_node),
            tour,
            -1,
        )

    return path


def get_node_tour(i: int, tour: list[tuple[int, Node]]) -> tuple[int, Node]:
    """Find the node with given index in the tour.

    Args:
        i: Index to search for
        tour: Complete tour with indices

    Returns:
        Tuple (index, node) from the tour, or None if not found
    """
    for j, v in tour:
        if i == j:
            return (i, v)
    return None
