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


## Cyclic Routing ##


def find_successor(P: nx.Graph, n:Node) -> Node:
    """Finds the successor of a node in a path represented as a graph.

    Assumes that the input graph `P` represents a path or cycle, where each node 
    has at most one outgoing edge. Returns the immediate successor of node `n`.

    Args:
        P: A graph (nx.Graph) representing a path.
        n: A node (Node) whose successor is to be found.

    Returns:
        Successor node of n
    """

    return list(P.adj[n])[0]


# sort bc idk how to do better
def sort_vm(vm: Path, s:Node, dir: int) -> Path: 
    """Sorts a path relative to a reference node and a direction.

    Args:
        vm: A path (Path) represented as a list of nodes.
        s: The reference node (Node) from which sorting begins.
        dir: Direction indicator (int): 
             - If -1, sorts in descending order (backward).
             - Otherwise, sorts in ascending order (forward).

    Returns:
        A new path (Path) starting from `s`, followed by sorted nodes 
        in the specified direction.
    """

    smaller_than_s = list(filter(lambda el: el < s, vm))
    bigger_than_s = list(filter(lambda el: el > s, vm))
    if dir == -1:
        return (
            [s]
            + sorted(smaller_than_s, reverse=True)
            + sorted(bigger_than_s, reverse=True)
        )
    return [s] + sorted(bigger_than_s) + sorted(smaller_than_s)


def shortcut(Vm: Path, Pcr: Path, dir: int, G: nx.Graph, blocked: Path) -> Path:
    """Applies one iteration of the shortcut procedure on a cyclic routing path.

    This function performs a single iteration of the shortcutting process used in
    cyclic routing. It modifies the virtual matching path (Vm) by attempting to
    bypass visited or blocked segments in the current routing path (Pcr), 
    following a given direction.

    Args:
        Vm: The current virtual matching path (Path) to be modified.
        Pcr: The current cyclic routing path (Path).
        dir: Direction indicator (int), e.g., 1 for forward, -1 for backward traversal.
        G: The underlying graph (nx.Graph) used for evaluating potential shortcuts.
        blocked: A path (Path) representing edges that are blocked and must be avoided.

    Returns:
        A new path (Path) resulting from applying one shortcut iteration to Vm.
    """

    Vm = [Vm[0]] + Vm[1:][::dir]
    Vm_1 = Vm.copy()
    vm = sort_vm(Vm[1:], Vm[0], dir)
    Em = []
    i = 0
    j = 1
    while j < len(Vm):
        vmi = vm[i]
        vmj = vm[j]

        current_edge = (vmi, vmj)
        if current_edge not in blocked:
            Vm_1.remove(vmj)
            Pcr.append(current_edge)
            i = j
            j = i + 1
        else:  # blockage
            Em.append(current_edge)
            l = 1

            vl = find_successor(G, vmi)
            vmi_vl_edge = (vmi, vl)
            vl_vmj_edge = (vl, vmj)
            vmi_vl_blocked = vmi_vl_edge in blocked
            vl_vmj_blocked = vl_vmj_edge in blocked
            while not vl == vmj and (vmi_vl_blocked or vl_vmj_blocked):
                if vmi_vl_blocked:
                    Em.append(vmi_vl_edge)
                if vl_vmj_blocked:
                    Em.append(vl_vmj_edge)
                l += 1
                vl = find_successor(G, vl)
                vmi_vl_edge = (vmi, vl)
                vl_vmj_edge = (vl, vmj)
                vmi_vl_blocked = vmi_vl_edge in blocked
                vl_vmj_blocked = vl_vmj_edge in blocked
            if not vl == vmj:
                Vm_1.remove(vmj)
                Pcr.append(vmi_vl_edge)
                Pcr.append(vl_vmj_edge)
                i = j
                j = i + 1
            else:
                j = j + 1
    return Vm_1


def turn_around_vm(Vm: Path) -> Path:
    """Reverses the direction of each edge in a path.

    Args:
        Vm: A path (Path) represented as a list of directed edges (tuples of nodes).

    Returns:
        A new path (Path) with all edges reversed in direction.
    """
    Vm_new = [(vmj, vmi) for vmi, vmj in Vm]
    return Vm_new


def cyclic_routing(G: nx.Graph, blocked: Path) -> Path:
    """Computes a cyclic tour in a graph while avoiding blocked edges.

    This function plans a tour that visits nodes in the graph in a cyclic manner,
    adapting the route to avoid a predefined set of blocked edges. 

    Args:
        G: The input graph represented as a NetworkX graph (nx.Graph).
        blocked: A path (Path) representing the edges that are blocked and must be avoided.

    Returns:
        A path (Path) representing a valid cyclic tour that avoids the blocked edges.
    """

    blocked = blocked + turn_around_vm(blocked)

    Pcr = []
    m = 1
    graphs = {-1: G.reverse(), 1: G}
    nodelist = list(G.nodes())
    Vm = nodelist.copy()
    last_m_end = -1  # node where last iteration ended
    dir = 1
    while not Vm == []:
        if m == 1 or last_m_end == Vm[0]:
            last_m_end = Vm[-1]
            if m == 1:
                Vm_1 = shortcut(Vm, Pcr, dir, graphs[dir], blocked)
            else:
                Vm_1 = shortcut(Vm, Pcr, dir, graphs[dir], blocked)

            if Vm == Vm_1:
                dir *= -1
                Vm = shortcut(Vm, Pcr, dir, graphs[dir], blocked)
            else:
                Vm = Vm_1.copy()
        else:
            dir *= -1
            last_m_end = Vm[-1]
            Vm = shortcut(Vm, Pcr, dir, graphs[dir], blocked)
        if len(Vm) == 1:
            Vm = []
        else:
            Vm = [Pcr[-1][1]] + Vm[1:]
        m += 1

    # retour
    Vm = [Pcr[-1][1], 0]
    if len(shortcut(Vm, Pcr, dir, graphs[dir], blocked)) == 2:
        dir *= -1
        shortcut(Vm, Pcr, dir, graphs[dir], blocked)

    return Pcr


def canadian_traveller_cyclic_routing(G: nx.Graph, blocked: Path, tour: Edge_Path = []) -> tuple[nx.Graph, Weight]:
    """Solves the Canadian Traveller Problem in a cyclic graph.

    This function implements a strategy to traverse a graph while accounting for 
    potentially blocked edges, as in the Canadian Traveller Problem. It dynamically 
    updates the graph based on discovered blockages during traversal and returns 
    the updated graph along with the total cost of the journey.

    Args:
        G: The initial graph represented as a NetworkX graph (nx.Graph).
        blocked: A path (Path) representing edges that are blocked, discovered during traversal.
        tour: Optional list of edges (Edge_Path) representing an initial planned tour.

    Returns:
        A tuple containing:
            - The updated graph after accounting for blocked edges.
            - The total weight (Weight) of the actual traversal in the graph.
    """
    # for the cr algorithm nodes need to be labeled in ascending order
    if tour == []:
        tour = travelling_salesman_christofides(G)[0]
    tour_nodes = [n1 for (n1, _) in tour]
    node_map = {node: i for i, node in enumerate(tour_nodes)}
    P = [(i, i + 1) for i in range(len(tour_nodes) - 1)] + [
        (len(tour_nodes) - 1, 0)
    ]
    tsp_tour_G = nx.DiGraph(P)

    blocked_mapped = [(node_map[i], node_map[j]) for (i, j) in blocked]
    tour_cr = cyclic_routing(tsp_tour_G, blocked_mapped)

    node_map_inv = {j: i for (i, j) in node_map.items()}
    tour_cr = [(node_map_inv[i], node_map_inv[j]) for (i, j) in tour_cr]
    final_G = nx.DiGraph(tour_cr)
    final_weight = graph_utils.calculate_path_weight(G,tour_cr)
    return final_G, final_weight
