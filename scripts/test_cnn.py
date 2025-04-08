import random

from tqdm import tqdm

from cstp import cnn, utils


def main():
    n_instances: int = 200

    for _ in tqdm(range(n_instances)):
        n: int = int(random.uniform(4, 256))
        k: int = int(random.uniform(0, n - 2))

        graph = utils.create_random_graph(n)
        blocked_edges = utils.create_random_blocks(k, graph)

        cnn_tour, _ = cnn.cnn_cctp(graph, blocked_edges)

        assert cnn_tour[0] == cnn_tour[-1], (
            "Tour does not start and end at the same vertex"
        )

        assert set(cnn_tour) == set(graph.nodes()), (
            "Tour did not contain all nodes"
        )

        edges = [
            utils.edge(cnn_tour[i], cnn_tour[i + 1])
            for i in range(len(cnn_tour) - 1)
        ]
        assert len(set(blocked_edges) & set(edges)) == 0, (
            "Tour contains a blocked edge"
        )


if __name__ == "__main__":
    main()
