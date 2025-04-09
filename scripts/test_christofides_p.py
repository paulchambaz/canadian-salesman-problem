import random

from tqdm import tqdm
import networkx as nx


from cstp import graph_utils, christofides_p, utils
def main():
    n_instances: int = 200

    for _ in tqdm(range(n_instances)):
        n: int = int(random.uniform(4, 256))

       # graph = graph_utils.generer_graphe_tsp(n)
        graph = utils.create_random_graph(n)
        christofides_tour, _ = christofides_p.travelling_salesman_christofides(graph)        
        christofides_tour = [edge[0] for edge in christofides_tour] +[christofides_tour[-1][1]]

        assert christofides_tour[0] == christofides_tour[-1], (
            "Tour does not start and end at the same vertex"
        )

        assert set(christofides_tour) == set(graph.nodes()), (
            "Tour does not contain all nodes"
        )

        visited_nodes = set(christofides_tour[:-1])
        assert len(visited_nodes) == n, "Not all nodes visited exactly once"


if __name__ == "__main__":
    main()
