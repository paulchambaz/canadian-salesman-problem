import pickle
import random
from collections.abc import Callable
from pathlib import Path

import networkx as nx
import numpy as np
from tqdm import tqdm

from cctp import christofides, cnn, cr, graphs, utils


def benchmark_graph_n(
    graph_type: str,
    min_w: int,
    max_w: int,
    step: int,
    get_size: Callable[[int], int],
    create_graph: Callable[[int], nx.Graph],
):
    seed = 42
    repeats = 15

    random.seed(seed)
    np.random.seed(seed)

    w_values = np.arange(min_w, max_w + 1, step)
    sizes = [int(get_size(w)) for w in w_values]
    results = {"seed": seed, "sizes": sizes, "cnn_data": {}, "cr_data": {}}

    for w, n in tqdm(
        zip(w_values, sizes, strict=True),
        desc=f"Benchmarking christofides ratio on n {graph_type} graph",
    ):
        cnn_ratios = []
        cr_ratios = []
        for _ in tqdm(range(repeats), desc=f"Testing n={n}", leave=False):
            graph = create_graph(w)
            blocked_edges = utils.create_random_blocks(n - 2, graph)
            christofides_tour, christofides_cost = (
                christofides.christofides_tsp(graph)
            )
            _, cr_cost = cr.cr_cctp(graph, blocked_edges)
            cr_ratios.append(cr_cost / christofides_cost)

            _, cnn_cost = cnn.cnn_cctp(graph, blocked_edges)
            cnn_ratios.append(cnn_cost / christofides_cost)

        cnn_stats = utils.compute_stats(cnn_ratios)
        results["cnn_data"][n] = {**cnn_stats, "ratios": cnn_ratios}

        cr_stats = utils.compute_stats(cr_ratios)
        results["cr_data"][n] = {**cr_stats, "ratios": cr_ratios}

    Path("results").mkdir(exist_ok=True)
    filename = f"results/graphs_ratio_{graph_type}_n_results.pk"
    with open(filename, "wb") as f:
        pickle.dump(results, f)


def benchmark_graph_k(
    graph_type: str,
    w: int,
    step: int,
    get_size: Callable[[int], int],
    create_graph: Callable[[int], nx.Graph],
):
    seed = 42
    repeats = 15

    random.seed(seed)
    np.random.seed(seed)

    n = get_size(w)

    sizes = np.arange(0, n - 1, step)
    results = {"seed": seed, "sizes": sizes, "cnn_data": {}, "cr_data": {}}

    for k in tqdm(
        sizes,
        desc=f"Benchmarking christofides ratio on k {graph_type} graph",
    ):
        cr_ratios = []
        cnn_ratios = []
        for _ in tqdm(range(repeats), desc=f"Testing k={k}", leave=False):
            graph = create_graph(w)
            blocked_edges = utils.create_random_blocks(k, graph)
            christofides_tour, christofides_cost = (
                christofides.christofides_tsp(graph)
            )
            _, cr_cost = cr.cr_cctp(graph, blocked_edges)
            cr_ratios.append(cr_cost / christofides_cost)

            _, cnn_cost = cnn.cnn_cctp(graph, blocked_edges)
            cnn_ratios.append(cnn_cost / christofides_cost)

        cnn_stats = utils.compute_stats(cnn_ratios)
        results["cnn_data"][k] = {**cnn_stats, "ratios": cnn_ratios}

        cr_stats = utils.compute_stats(cr_ratios)
        results["cr_data"][k] = {**cr_stats, "ratios": cr_ratios}

    Path("results").mkdir(exist_ok=True)
    filename = f"results/graphs_ratio_{graph_type}_k_results.pk"
    with open(filename, "wb") as f:
        pickle.dump(results, f)


def main():
    benchmark_graph_n(
        "constant", 4, 256, 12, lambda x: x, graphs.create_constant_weight_graph
    )
    benchmark_graph_n(
        "euclidian", 4, 256, 12, lambda x: x, graphs.create_euclidian_graph
    )
    benchmark_graph_n(
        "manhattan", 2, 16, 1, lambda x: x * x, graphs.create_manhattan_graph
    )
    benchmark_graph_n(
        "clustered", 2, 16, 1, lambda x: x * x, graphs.create_clustered_graph
    )
    benchmark_graph_n(
        "power_law", 4, 256, 12, lambda x: x, graphs.create_power_law_graph
    )

    benchmark_graph_k(
        "constant", 256, 12, lambda x: x, graphs.create_constant_weight_graph
    )
    benchmark_graph_k(
        "euclidian", 256, 12, lambda x: x, graphs.create_euclidian_graph
    )
    benchmark_graph_k(
        "manhattan", 16, 12, lambda x: x * x, graphs.create_manhattan_graph
    )
    benchmark_graph_k(
        "clustered", 16, 12, lambda x: x * x, graphs.create_clustered_graph
    )
    benchmark_graph_k(
        "power_law", 256, 12, lambda x: x, graphs.create_power_law_graph
    )


if __name__ == "__main__":
    main()
