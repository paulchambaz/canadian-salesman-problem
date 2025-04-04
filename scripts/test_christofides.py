from cstp import utils, tsp, christofides
from tqdm import tqdm


def main():
    n_instances: int = 100
    n_vertices: int = 10

    for _ in tqdm(range(n_instances)):
        graph = utils.create_random_graph(n_vertices)

        _, optimal_cost = tsp.optimal_tsp(graph)
        _, christofides_cost = christofides.christofides_tsp(graph)

        ratio = christofides_cost / optimal_cost

        assert ratio <= 1.5
        assert ratio >= 1.0


if __name__ == "__main__":
    main()
