import pickle
import random
import time
from pathlib import Path

import numpy as np
from tqdm import tqdm

from cstp import christofides, utils


def main():
    seed = 42
    min_n = 20
    max_n = 400
    step = 20
    repeats = 15

    random.seed(seed)
    np.random.seed(seed)

    sizes = np.arange(min_n, max_n + 1, step)
    results = {"seed": seed, "sizes": sizes, "data": {}}

    for n in tqdm(sizes, desc="Testing graph sizes"):
        runtimes = []
        for _ in tqdm(range(repeats), desc=f"Testing n={n}", leave=False):
            graph = utils.create_random_graph(n)
            start = time.time()
            _, _ = christofides.christofides_tsp(graph)
            runtimes.append(time.time() - start)

        stats = utils.compute_stats(runtimes)
        results["data"][n] = {**stats, "runtimes": runtimes}

    Path("results").mkdir(exist_ok=True)
    filename = "results/christofides_runtime_results.pk"
    with open(filename, "wb") as f:
        pickle.dump(results, f)


if __name__ == "__main__":
    main()
