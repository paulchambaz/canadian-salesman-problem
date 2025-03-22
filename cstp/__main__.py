from .utils import create_complete_graph_from_points
from .christofides import christofides_tsp
import matplotlib.pyplot as plt
import networkx as nx


def main():
    pass
    coordinate_points = [(-1, 1), (1, 1), (-2, 0), (2, 0), (0, -1)]
    complete_graph = create_complete_graph_from_points(coordinate_points)
    optimal_tour, total_cost = christofides_tsp(complete_graph)

    print(f"Tour: {optimal_tour}")
    print(f"Cost: {total_cost}")

    # visualisation

    pos = nx.get_node_attributes(complete_graph, "pos")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    ax1.set_title("Complete Graph")
    nx.draw(
        complete_graph,
        pos,
        with_labels=True,
        node_color="lightblue",
        node_size=500,
        font_weight="bold",
        ax=ax1,
    )
    edge_labels = {
        (u, v): f"{d['weight']:.2f}" for u, v, d in complete_graph.edges(data=True)
    }
    nx.draw_networkx_edge_labels(complete_graph, pos, edge_labels=edge_labels, ax=ax1)

    tour_graph = nx.Graph()
    for i in range(len(optimal_tour) - 1):
        u, v = optimal_tour[i], optimal_tour[i + 1]
        tour_graph.add_edge(u, v)

    ax2.set_title(f"Christofides Tour (Cost: {total_cost:.2f})")
    nx.draw(
        tour_graph,
        pos,
        with_labels=True,
        node_color="lightgreen",
        node_size=500,
        font_weight="bold",
        ax=ax2,
    )
    tour_edges = list(zip(optimal_tour, optimal_tour[1:] + [optimal_tour[0]]))
    nx.draw_networkx_edges(
        tour_graph, pos, edgelist=tour_edges, width=2, edge_color="r", ax=ax2
    )

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
