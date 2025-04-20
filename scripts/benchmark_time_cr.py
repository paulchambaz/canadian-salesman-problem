import pickle
import random
import time
from pathlib import Path

import numpy as np
from tqdm import tqdm

from cctp import christofides, cr, utils


def benchmark_n():
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
            blocked_edges = utils.create_random_blocks(n - 2, graph)
            tour, _ = christofides.christofides_tsp(graph)
            start = time.time()
            _, _ = cr.cr_cctp(graph, blocked_edges, tour)
            runtimes.append(time.time() - start)

        stats = utils.compute_stats(runtimes)
        results["data"][n] = {**stats, "runtimes": runtimes}

    Path("results").mkdir(exist_ok=True)
    filename = "results/cr_runtime_n_results.pk"
    with open(filename, "wb") as f:
        pickle.dump(results, f)


def benchmark_k():
    seed = 42
    min_n = 4
    max_n = 256
    step = 12
    repeats = 100

    random.seed(seed)
    np.random.seed(seed)

    sizes = np.arange(min_n, max_n + 1, step)
    results = {"seed": seed, "sizes": sizes, "data": {}}

    for n in tqdm(sizes, desc="Testing graph sizes"):
        runtimes = []
        for _ in tqdm(range(repeats), desc=f"Testing k={n}", leave=False):
            graph = utils.create_random_graph(max_n + 2)
            blocked_edges = utils.create_random_blocks(n, graph)
            tour, _ = christofides.christofides_tsp(graph)
            start = time.time()
            _, _ = cr.cr_cctp(graph, blocked_edges, tour)
            runtimes.append(time.time() - start)

        stats = utils.compute_stats(runtimes)
        results["data"][n] = {**stats, "runtimes": runtimes}

    Path("results").mkdir(exist_ok=True)
    filename = "results/cr_runtime_k_results.pk"
    with open(filename, "wb") as f:
        pickle.dump(results, f)


def main():
    benchmark_n()
    benchmark_k()


if __name__ == "__main__":
    main()
