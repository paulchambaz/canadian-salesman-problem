from cstp import utils, christofides
import numpy as np
import random
from tqdm import tqdm
import pickle
from pathlib import Path


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

        def run_christofides():
            graph = utils.create_random_graph(n)
            christofides.christofides_tsp(graph)

        results["data"][n] = utils.measure_runtime(run_christofides, n, repeats)

        Path("results").mkdir(exist_ok=True)
        filename = "results/christofides_runtime_results.pk"
        with open(filename, "wb") as f:
            pickle.dump(results, f)


if __name__ == "__main__":
    main()
