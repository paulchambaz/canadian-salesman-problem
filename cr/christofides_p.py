import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def travelling_salesman_christofides(G, return_difference = False):
    # arbre couvrante poids min
    T = nx.minimum_spanning_tree(G)

    O = [node for node in T.nodes if T.degree[node] % 2 != 0]
    sub_G = G.subgraph(O)

    M = nx.algorithms.matching.min_weight_matching(sub_G)
    assert(nx.algorithms.is_perfect_matching(sub_G,M))
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
    edge_list_tsp = [(visited[i],visited[i+1]) for i in range(len(visited)-1)]
    edge_list_tsp.append((visited[-1],visited[0]))

    final_G = G.edge_subgraph(edge_list_tsp)
    assert nx.has_eulerian_path(final_G), 'Error: No Eulerian Path in final graph'

    # difference entre solution generee par nx et la notre
    lamda = 0
    if return_difference:
        visited_nx = nx.approximation.traveling_salesman_problem(G)
        edge_list_tsp_nx = [(visited_nx[i],visited_nx[i+1]) for i in range(len(visited_nx)-1)]
        edge_list_tsp_nx.append((visited_nx[-1],visited_nx[0]))
        final_G_nx = G.edge_subgraph(edge_list_tsp_nx)
        lamda = (final_G_nx.size(weight = 'weight') - final_G.size(weight = 'weight')) 
        print("-------")
    return edge_list_tsp, lamda


## Cyclic Routing ##

def find_successor(P, n):
    return list(P.adj[n])[0]


# sort bc idk how to do better
def sort_vm(vm,s,dir):
    smaller_than_s = list(filter(lambda el: el < s, vm))
    bigger_than_s = list(filter(lambda el: el > s, vm))
    if dir == -1:
        return [s] + sorted(smaller_than_s,reverse=True) + sorted(bigger_than_s,reverse=True)
    else:
        return [s] + sorted(bigger_than_s) + sorted(smaller_than_s) 

def shortcut(Vm, Pcr, dir,G,blocked):
    Vm = [Vm[0]] + Vm[1:][::dir]
    Vm_1 = Vm.copy()
    vm = sort_vm(Vm[1:],Vm[0],dir )
    print(vm)
    print("---------- after sort")
    Em = []
    i = 0
    j = 1
    while j < len(Vm):
        vmi = vm[i]
        vmj = vm[j]

        current_edge = (vmi,vmj) 
        if not current_edge in blocked:
            Vm_1.remove(vmj)
            Pcr.append(current_edge)
            i = j
            j = i + 1
        else: # blockage
            Em.append(current_edge)
            l = 1

            vl = find_successor(G,vmi)
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
                vl = find_successor(G,vl)
                vmi_vl_edge = (vmi, vl)
                vl_vmj_edge = (vl, vmj)
                vmi_vl_blocked = vmi_vl_edge in blocked
                vl_vmj_blocked = vl_vmj_edge in blocked
            if not vl == vmj:
                Vm_1.remove(vmj)
                Pcr.append(vmi_vl_edge)
                Pcr.append(vl_vmj_edge)
                i = j
                j =  i + 1
            else:
                j = j + 1
    return Vm_1


def turn_around_vm(Vm):
    Vm_new = [(vmj,vmi) for vmi,vmj in Vm]
    return Vm_new


def cyclic_routing(G, blocked):
    blocked = blocked + turn_around_vm(blocked)

    Pcr = []
    m = 1
    graphs = {
        -1 : G.reverse(),
        1  : G
    }
    nodelist = list(G.nodes())
    Vm = nodelist.copy()
    last_m_end = -1 # node where last iteration ended
    dir = 1
    while not Vm == []:
        print(Vm)
        if m == 1 or last_m_end == Vm[0]:
            last_m_end = Vm[-1]
            if m == 1:
                Vm_1 = shortcut(Vm,Pcr,dir,graphs[dir],blocked)
            else:
                Vm_1 = shortcut(Vm,Pcr,dir,graphs[dir],blocked)
            
            if Vm == Vm_1:
                dir *= -1
                Vm = shortcut(Vm, Pcr, dir,graphs[dir],blocked)
            else:
                Vm = Vm_1.copy()
        else:
            dir *= -1
            last_m_end = Vm[-1]
            Vm = shortcut(Vm, Pcr, dir,graphs[dir],blocked)
        if len(Vm) == 1:
            Vm = []
        else: 
            Vm = [Pcr[-1][1]] + Vm[1:]
        m += 1
        
    print("Pre final PCR---")
    print(Pcr)
    print("Final PCR")
    # retour 
    Vm = [Pcr[-1][1],0]
    if len(shortcut(Vm, Pcr, dir, graphs[dir],blocked)) == 2:
        print("Again")
        dir *= -1
        shortcut(Vm, Pcr, dir, graphs[dir],blocked)
    print(Pcr)

    return Pcr

def canadian_traveller_cyclic_routing(G, blocked):
    # for the cr algorithm nodes need to be labeled in ascending order
    tour = travelling_salesman_christofides(G)[0]
    tour_nodes = [n1 for (n1,_) in tour]
    node_map = {node:i for i,node in enumerate(tour_nodes)}
    print(node_map)
    P = [(i,i+1) for i in range(len(tour_nodes)-1)] + [(len(tour_nodes)-1,0)]
    tsp_tour_G = nx.DiGraph(P)


    blocked_mapped = [(node_map[i],node_map[j]) for (i,j) in blocked]
    tour_cr = cyclic_routing(tsp_tour_G, blocked_mapped)

    node_map_inv = {j:i for (i,j) in node_map.items()}
    print(node_map_inv)
    tour_cr = [(node_map_inv[i], node_map_inv[j]) for (i,j) in tour_cr]
    return nx.edge_subgraph(G, tour_cr)