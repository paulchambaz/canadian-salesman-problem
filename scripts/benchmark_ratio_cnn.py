import pickle
import random
from pathlib import Path

import numpy as np
from tqdm import tqdm

from cctp import christofides, cnn, graphs, utils


def main():
    seed = 42
    min_p = 1
    max_p = 8
    step = 1
    repeats = 1

    random.seed(seed)
    np.random.seed(seed)

    p_values = np.arange(min_p, max_p + 1, step)
    sizes = [int(2 ** (p + 1)) for p in p_values]
    results = {"seed": seed, "sizes": sizes, "data": {}}

    for p, n in tqdm(
        zip(p_values, sizes, strict=True), desc="Benchmarking cnn ratio"
    ):
        ratios = []
        for _ in tqdm(range(repeats), desc=f"Testing p={p} n={n}", leave=False):
            graph, blocked_edges = graphs.cnn_tight_bound_graph(int(p))
            christofides_tour, christofides_cost = (
                christofides.christofides_tsp(graph)
            )
            _, cnn_cost = cnn.cnn_cctp(graph, blocked_edges)
            ratios.append(cnn_cost / christofides_cost)

        stats = utils.compute_stats(ratios)
        results["data"][n] = {**stats, "ratios": ratios}

    Path("results").mkdir(exist_ok=True)
    filename = "results/cnn_ratio_results.pk"
    with open(filename, "wb") as f:
        pickle.dump(results, f)


if __name__ == "__main__":
    main()
