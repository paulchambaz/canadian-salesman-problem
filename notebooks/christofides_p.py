import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


def generer_graphe_tsp(n):
    # Générer des positions aléatoires dans un espace 2D
    positions = {i: np.random.rand(2) for i in range(n)}
    
    # Créer un graphe complet respectant l'inégalité triangulaire
    G = nx.complete_graph(n)
    for i in range(n):
        for j in range(i + 1, n):
            # Calculer la distance euclidienne entre les points
            poids = np.linalg.norm(positions[i] - positions[j]) * 10
            G[i][j]['weight'] = poids
            G[j][i]['weight'] = poids  # Graphe non orienté

    return G, positions

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

#for i in range(10,100,10):
 #   print(travelling_salesman_christofides(n= i, return_difference=True)[1])