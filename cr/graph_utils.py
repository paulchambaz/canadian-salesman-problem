import random

import networkx as nx
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
            G[i][j]["weight"] = poids
            G[j][i]["weight"] = poids  # Graphe non orienté

    return G


def generer_blockages(G, percentage=0.5):
    edge_list = list(G.edges())
    return [edge for edge in edge_list if random.random() <= percentage]
