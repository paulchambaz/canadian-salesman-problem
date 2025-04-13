from collections.abc import Callable
import pickle
import random
from pathlib import Path

import numpy as np
from tqdm import tqdm

from cstp import christofides, cnn, graphs, utils


def benchmark_graph_n(
    graph_type: str,
    min_w: int,
    max_w: int,
    step: int,
    get_size: Callable[[int], int],
):
    create_graph = {
        "constant": graphs.create_constant_weight_graph,
        "euclidian": graphs.create_euclidian_graph,
        "manhattan": graphs.create_manhattan_grid_graph,
        "clustered": graphs.create_clustered_graph,
        "power_law": graphs.create_power_law_graph,
    }[graph_type]

    seed = 42
    repeats = 15

    random.seed(seed)
    np.random.seed(seed)

    w_values = np.arange(min_w, max_w + 1, step)
    sizes = [int(get_size(w)) for w in w_values]
    results = {"seed": seed, "sizes": sizes, "cnn_data": {}}

    for w, n in tqdm(
        zip(w_values, sizes, strict=True),
        desc=f"Benchmarking christofides ratio on n {graph_type} graph",
    ):
        cnn_ratios = []
        for _ in tqdm(range(repeats), desc=f"Testing n={n}", leave=False):
            graph = create_graph(w)
            blocked_edges = utils.create_random_blocks(n - 2, graph)
            christofides_tour, christofides_cost = (
                christofides.christofides_tsp(graph)
            )
            # TODO: ajouter CR
            # _, cr_cost = cr.cr_cctp(graph, blocked_edges)
            _, cnn_cost = cnn.cnn_cctp(graph, blocked_edges)
            cnn_ratios.append(cnn_cost / christofides_cost)

        stats = utils.compute_stats(cnn_ratios)
        results["cnn_data"][n] = {**stats, "cnn": cnn_ratios}

    Path("results").mkdir(exist_ok=True)
    filename = f"results/graphs_ratio_{graph_type}_n_results.pk"
    with open(filename, "wb") as f:
        pickle.dump(results, f)


def benchmark_graph_k(
    graph_type: str,
    w: int,
    step: int,
    get_size: Callable[[int], int],
):
    create_graph = {
        "constant": graphs.create_constant_weight_graph,
        "euclidian": graphs.create_euclidian_graph,
        "manhattan": graphs.create_manhattan_grid_graph,
        "clustered": graphs.create_clustered_graph,
        "power_law": graphs.create_power_law_graph,
    }[graph_type]

    seed = 42
    repeats = 15

    random.seed(seed)
    np.random.seed(seed)

    n = get_size(w)

    sizes = np.arange(0, n - 1, step)
    results = {"seed": seed, "sizes": sizes, "cnn_data": {}}

    for k in tqdm(
        sizes,
        desc=f"Benchmarking christofides ratio on k {graph_type} graph",
    ):
        cnn_ratios = []
        for _ in tqdm(range(repeats), desc=f"Testing k={k}", leave=False):
            graph = create_graph(w)
            blocked_edges = utils.create_random_blocks(k, graph)
            christofides_tour, christofides_cost = (
                christofides.christofides_tsp(graph)
            )
            # TODO: ajouter CR
            # _, cr_cost = cr.cr_cctp(graph, blocked_edges)
            _, cnn_cost = cnn.cnn_cctp(graph, blocked_edges)
            cnn_ratios.append(cnn_cost / christofides_cost)

        stats = utils.compute_stats(cnn_ratios)
        results["cnn_data"][n] = {**stats, "cnn": cnn_ratios}

    Path("results").mkdir(exist_ok=True)
    filename = f"results/graphs_ratio_{graph_type}_k_results.pk"
    with open(filename, "wb") as f:
        pickle.dump(results, f)


def main():
    benchmark_graph_n("constant", 4, 256, 12, lambda x: x)
    benchmark_graph_n("euclidian", 4, 256, 12, lambda x: x)
    benchmark_graph_n("manhattan", 2, 16, 1, lambda x: x * x)
    benchmark_graph_n("clustered", 2, 16, 1, lambda x: x * x)
    benchmark_graph_n("power_law", 4, 256, 12, lambda x: x)

    benchmark_graph_k("constant", 256, 12, lambda x: x)
    benchmark_graph_k("euclidian", 256, 12, lambda x: x)
    benchmark_graph_k("manhattan", 16, 12, lambda x: x * x)
    benchmark_graph_k("clustered", 16, 12, lambda x: x * x)
    benchmark_graph_k("power_law", 256, 12, lambda x: x)


if __name__ == "__main__":
    main()
