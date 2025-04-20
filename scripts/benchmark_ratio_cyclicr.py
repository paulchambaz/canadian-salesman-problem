import pickle
import random
from pathlib import Path

import numpy as np
from cstp import christofides_p, utils
from tqdm import tqdm


def main():
    seed = 21867
    min_k = 0
    max_k = 254
    step = 12
    repeats = 15

    random.seed(seed)
    np.random.seed(seed)

    sizes = np.arange(min_k, max_k + 1, step)
    results = {"seed": seed, "sizes": sizes, "data": {}}

    for k in tqdm(sizes, desc="Benchmarking cr ratio"):
        ratios = []
        for _ in tqdm(range(repeats), desc=f"Testing k={k}", leave=False):
            graph = utils.create_random_graph(max_k + 2)
            blocked_edges = utils.create_random_blocks(k, graph)
            christofides_tour, christofides_cost = (
                christofides_p.travelling_salesman_christofides(graph)
            )
            _, cnn_cost = christofides_p.canadian_traveller_cyclic_routing(
                graph, blocked_edges, christofides_tour
            )
            ratios.append(cnn_cost / christofides_cost)

        stats = utils.compute_stats(ratios)
        results["data"][k] = {**stats, "ratios": ratios}

    Path("results").mkdir(exist_ok=True)
    filename = "results/cr_ratio_k_results.pk"
    with open(filename, "wb") as f:
        pickle.dump(results, f)


if __name__ == "__main__":
    main()
