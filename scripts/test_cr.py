import random

from tqdm import tqdm

from cctp import cr, utils


def main():
    n_instances: int = 1000

    for _ in tqdm(range(n_instances)):
        n: int = int(random.uniform(4, 256))
        k: int = int(random.uniform(0, n - 2))

        graph = utils.create_random_graph(n)
        blocked_edges = utils.create_random_blocks(k, graph)

        cr_tour, _ = cr.cr_cctp(graph, blocked_edges)

        assert cr_tour[0] == cr_tour[-1], (
            "Tour does not start and end at the same vertex"
        )

        assert set(cr_tour) == set(graph.nodes()), (
            "Tour did not contain all nodes"
        )

        edges = [
            utils.edge(cr_tour[i], cr_tour[i + 1])
            for i in range(len(cr_tour) - 1)
        ]
        assert len(set(blocked_edges) & set(edges)) == 0, (
            "Tour contains a blocked edge"
        )


if __name__ == "__main__":
    main()
