import random

from tqdm import tqdm

from cstp import christofides, utils


def main():
    n_instances: int = 200

    for _ in tqdm(range(n_instances)):
        n: int = int(random.uniform(4, 256))

        graph = utils.create_random_graph(n)

        christofides_tour, _ = christofides.christofides_tsp(graph)

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
