# TODO: useless file - should be removed

import matplotlib.pyplot as plt
import networkx as nx

from .christofides import christofides_tsp
from .cnn import cnn_cctp
from .cr import cr_cctp
from .graphs import cr_tight_bound_graph
from .utils import (
    create_polygon_graph,
    create_random_blocks,
    create_random_graph,
    edge,
)


def test_christofides():
    n = 100

    graph = create_random_graph(n)
    tour, cost = christofides_tsp(graph)

    pos = nx.get_node_attributes(graph, "pos")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

    ax1.set_title("Complete Graph")
    nx.draw(
        graph,
        pos,
        with_labels=True,
        node_color="lightblue",
        edge_color="gray",
        node_size=500,
        width=0.2,
        font_weight="bold",
        ax=ax1,
    )

    ax2.set_title(f"Christofides Tour (Cost: {cost:.2f})")

    tour_graph = nx.Graph()
    for i in range(len(tour) - 1):
        u, v = tour[i], tour[i + 1]
        tour_graph.add_edge(u, v)

    nx.draw(
        tour_graph,
        pos,
        with_labels=True,
        node_color="lightgreen",
        node_size=500,
        font_weight="bold",
        ax=ax2,
    )
    tour_edges = list(zip(tour, tour[1:] + [tour[0]], strict=False))
    nx.draw_networkx_edges(
        tour_graph, pos, edgelist=tour_edges, width=2, edge_color="r", ax=ax2
    )

    plt.tight_layout()
    plt.show()


def test_cr():
    n = 5
    k = n - 2

    # graph = create_random_graph(n)
    graph = create_polygon_graph(n)
    blocked_edges = create_random_blocks(k, graph)
    print(f"{blocked_edges=}")

    christofides_tour, christofides_cost = christofides_tsp(graph)
    cnn_tour, cnn_cost = cr_cctp(graph, blocked_edges, christofides_tour)

    pos = nx.get_node_attributes(graph, "pos")

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6))

    ax1.set_title("Graphe complet avec arêtes bloquées")
    nx.draw(
        graph,
        pos,
        with_labels=True,
        node_color="lightblue",
        edge_color="gray",
        width=0.5,
        node_size=300,
        ax=ax1,
    )

    blocked_edges_list = [
        edge(u, v) for u, v in graph.edges() if edge(u, v) in blocked_edges
    ]
    nx.draw_networkx_edges(
        graph,
        pos,
        edgelist=blocked_edges_list,
        edge_color="black",
        width=1,
        ax=ax1,
    )

    ax2.set_title(f"Tour Christofides (Coût: {christofides_cost:.2f})")

    christofides_tour_graph = nx.Graph()
    for i in range(len(christofides_tour) - 1):
        u, v = christofides_tour[i], christofides_tour[i + 1]
        christofides_tour_graph.add_edge(u, v)

    nx.draw(
        christofides_tour_graph,
        pos,
        with_labels=True,
        node_color="lightgreen",
        node_size=500,
        font_weight="bold",
        ax=ax2,
    )
    tour_edges = list(
        zip(
            christofides_tour,
            christofides_tour[1:] + [christofides_tour[0]],
            strict=False,
        )
    )
    nx.draw_networkx_edges(
        christofides_tour_graph,
        pos,
        edgelist=tour_edges,
        width=2,
        edge_color="r",
        ax=ax2,
    )

    ax3.set_title(f"Tour CNN (Coût: {cnn_cost:.2f})")

    cnn_tour_graph = nx.Graph()
    for i in range(len(cnn_tour) - 1):
        u, v = cnn_tour[i], cnn_tour[i + 1]
        cnn_tour_graph.add_edge(u, v)

    nx.draw(
        cnn_tour_graph,
        pos,
        with_labels=True,
        node_color="lightgreen",
        node_size=500,
        font_weight="bold",
        ax=ax3,
    )
    tour_edges = list(zip(cnn_tour, cnn_tour[1:] + [cnn_tour[0]], strict=False))
    nx.draw_networkx_edges(
        cnn_tour_graph,
        pos,
        edgelist=tour_edges,
        width=2,
        edge_color="r",
        ax=ax3,
    )

    plt.tight_layout()
    plt.show()


def test_cnn():
    n = 100
    k = n - 2

    graph = create_random_graph(n)
    # graph = create_polygon_graph(n)
    blocked_edges = create_random_blocks(k, graph)

    christofides_tour, christofides_cost = christofides_tsp(graph)
    cnn_tour, cnn_cost = cnn_cctp(graph, blocked_edges, christofides_tour)

    pos = nx.get_node_attributes(graph, "pos")

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6))

    ax1.set_title("Graphe complet avec arêtes bloquées")
    nx.draw(
        graph,
        pos,
        with_labels=True,
        node_color="lightblue",
        edge_color="gray",
        width=0.5,
        node_size=300,
        ax=ax1,
    )

    blocked_edges_list = [
        edge(u, v) for u, v in graph.edges() if edge(u, v) in blocked_edges
    ]
    nx.draw_networkx_edges(
        graph,
        pos,
        edgelist=blocked_edges_list,
        edge_color="black",
        width=1,
        ax=ax1,
    )

    ax2.set_title(f"Tour Christofides (Coût: {christofides_cost:.2f})")

    christofides_tour_graph = nx.Graph()
    for i in range(len(christofides_tour) - 1):
        u, v = christofides_tour[i], christofides_tour[i + 1]
        christofides_tour_graph.add_edge(u, v)

    nx.draw(
        christofides_tour_graph,
        pos,
        with_labels=True,
        node_color="lightgreen",
        node_size=500,
        font_weight="bold",
        ax=ax2,
    )
    tour_edges = list(
        zip(
            christofides_tour,
            christofides_tour[1:] + [christofides_tour[0]],
            strict=False,
        )
    )
    nx.draw_networkx_edges(
        christofides_tour_graph,
        pos,
        edgelist=tour_edges,
        width=2,
        edge_color="r",
        ax=ax2,
    )

    ax3.set_title(f"Tour CNN (Coût: {cnn_cost:.2f})")

    cnn_tour_graph = nx.Graph()
    for i in range(len(cnn_tour) - 1):
        u, v = cnn_tour[i], cnn_tour[i + 1]
        cnn_tour_graph.add_edge(u, v)

    nx.draw(
        cnn_tour_graph,
        pos,
        with_labels=True,
        node_color="lightgreen",
        node_size=500,
        font_weight="bold",
        ax=ax3,
    )
    tour_edges = list(zip(cnn_tour, cnn_tour[1:] + [cnn_tour[0]], strict=False))
    nx.draw_networkx_edges(
        cnn_tour_graph,
        pos,
        edgelist=tour_edges,
        width=2,
        edge_color="r",
        ax=ax3,
    )

    plt.tight_layout()
    plt.show()


def test():
    graph, blocked_edges = cr_tight_bound_graph(1)
    tour, cost = christofides_tsp(graph)

    cr_tour, _ = cr_cctp(graph, blocked_edges, tour)
    print()
    print(f"{cr_tour=}")
    print()

    pos = nx.get_node_attributes(graph, "pos")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

    ax1.set_title("Graphe complet avec arêtes bloquées")
    nx.draw(
        graph,
        pos,
        with_labels=True,
        node_color="lightblue",
        edge_color="gray",
        width=0.5,
        node_size=300,
        ax=ax1,
    )

    # edge_labels = nx.get_edge_attributes(graph, "weight")
    # nx.draw_networkx_edge_labels(
    #     graph, pos, edge_labels=edge_labels, font_size=8, ax=ax1
    # )

    blocked_edges_list = [
        edge(u, v) for u, v in graph.edges() if edge(u, v) in blocked_edges
    ]
    nx.draw_networkx_edges(
        graph,
        pos,
        edgelist=blocked_edges_list,
        edge_color="black",
        width=1,
        ax=ax1,
    )

    ax2.set_title(f"Christofides Tour (Cost: {cost:.2f})")
    tour_graph = nx.Graph()
    for i in range(len(tour) - 1):
        u, v = tour[i], tour[i + 1]
        tour_graph.add_edge(u, v)

    nx.draw(
        tour_graph,
        pos,
        with_labels=True,
        node_color="lightgreen",
        node_size=500,
        font_weight="bold",
        ax=ax2,
    )
    tour_edges = list(zip(tour, tour[1:] + [tour[0]], strict=False))
    nx.draw_networkx_edges(
        tour_graph, pos, edgelist=tour_edges, width=2, edge_color="r", ax=ax2
    )

    plt.tight_layout()
    plt.show()


def main():
    # test_christofides()
    # test_cr()
    # test_cnn()
    test()


if __name__ == "__main__":
    main()
