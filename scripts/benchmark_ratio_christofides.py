import pickle
import random
from pathlib import Path

import numpy as np
from tqdm import tqdm

from cstp import christofides, tsp, utils


def main():
    seed = 42
    min_n = 4
    max_n = 10
    step = 1
    repeats = 20

    random.seed(seed)
    np.random.seed(seed)

    sizes = np.arange(min_n, max_n + 1, step)
    results = {"seed": seed, "sizes": sizes, "data": {}}

    for n in tqdm(sizes, desc="Benchmarking christofides ratio"):
        ratios = []
        for _ in tqdm(range(repeats), desc=f"Testing n={n}", leave=False):
            graph = utils.create_random_graph(n)
            _, optimal_cost = tsp.optimal_tsp(graph)
            _, christofides_cost = christofides.christofides_tsp(graph)
            ratios.append(christofides_cost / optimal_cost)

        stats = utils.compute_stats(ratios)
        results["data"][n] = {**stats, "ratios": ratios}

    Path("results").mkdir(exist_ok=True)
    filename = "results/christofides_ratio_results.pk"
    with open(filename, "wb") as f:
        pickle.dump(results, f)


if __name__ == "__main__":
    main()
