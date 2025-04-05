from cstp import utils, cnn
from tqdm import tqdm


def main():
    n_instances: int = 200
    n: int = 200
    k: int = n - 2

    for _ in tqdm(range(n_instances)):
        graph = utils.create_random_graph(n)
        blocked_edges = utils.create_random_blocks(k, graph)

        cnn_tour, cnn_cost = cnn.cnn_cctp(graph, blocked_edges)

        assert set(cnn_tour) == set(graph.nodes()), "Tour did not contain all nodes"

        edges = [
            utils.edge(cnn_tour[i], cnn_tour[i + 1]) for i in range(len(cnn_tour) - 1)
        ]

        assert len(set(blocked_edges) & set(edges)) == 0, "Tour contains a blocked edge"


if __name__ == "__main__":
    main()
