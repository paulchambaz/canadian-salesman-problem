import pickle

import matplotlib.pyplot as plt


def visualize_graph_n(graph_type: str):
    with open(f"results/graphs_ratio_{graph_type}_n_results.pk", "rb") as f:
        results = pickle.load(f)

    sizes = results["sizes"]

    iqms = [results["cnn_data"][n]["iqm"] for n in sizes]
    q1s = [results["cnn_data"][n]["q1"] for n in sizes]
    q3s = [results["cnn_data"][n]["q3"] for n in sizes]

    plt.figure(figsize=(6, 6))

    plt.fill_between(
        sizes,
        q1s,
        q3s,
        alpha=0.2,
        color="#3498db",
        label=r"IQ des ratios",
    )

    plt.plot(
        sizes,
        iqms,
        "o-",
        color="#3498db",
        linewidth=2.5,
        markersize=8,
        label=r"IQM des ratios",
    )

    plt.grid(True, alpha=0.3)
    plt.xlabel(r"Nombre de sommet ($n$)", fontsize=18)
    plt.ylabel(r"Ratio", fontsize=18)

    plt.legend(fontsize=16, framealpha=0.9)
    plt.tight_layout()

    plt.savefig(
        f"paper/figures/christofides_ratio_{graph_type}_n_plot.svg",
        bbox_inches="tight",
    )

    plt.show()


def visualize_graph_k(graph_type: str):
    with open(f"results/graphs_ratio_{graph_type}_k_results.pk", "rb") as f:
        results = pickle.load(f)

    sizes = results["sizes"]

    iqms = [results["cnn_data"][n]["iqm"] for n in sizes]
    q1s = [results["cnn_data"][n]["q1"] for n in sizes]
    q3s = [results["cnn_data"][n]["q3"] for n in sizes]

    plt.figure(figsize=(6, 6))

    plt.fill_between(
        sizes,
        q1s,
        q3s,
        alpha=0.2,
        color="#3498db",
        label=r"IQ des ratios",
    )

    plt.plot(
        sizes,
        iqms,
        "o-",
        color="#3498db",
        linewidth=2.5,
        markersize=8,
        label=r"IQM des ratios",
    )

    plt.grid(True, alpha=0.3)
    plt.xlabel(r"Nombre de sommet ($n$)", fontsize=18)
    plt.ylabel(r"Ratio", fontsize=18)

    plt.legend(fontsize=16, framealpha=0.9)
    plt.tight_layout()

    plt.savefig(
        f"paper/figures/christofides_ratio_{graph_type}_k_plot.svg",
        bbox_inches="tight",
    )

    plt.show()


def main():
    plt.rcParams.update(
        {
            "text.usetex": True,
            "font.family": "serif",
            "font.serif": ["Computer Modern Roman"],
            "axes.labelsize": 20,
            "font.size": 20,
            "legend.fontsize": 16,
            "xtick.labelsize": 16,
            "ytick.labelsize": 16,
        }
    )
    visualize_graph_n("constant")
    visualize_graph_n("euclidian")
    visualize_graph_n("manhattan")
    visualize_graph_n("clustered")
    visualize_graph_n("power_law")

    # visualize_graph_k("constant")
    # visualize_graph_k("euclidian")
    # visualize_graph_k("manhattan")
    # visualize_graph_k("clustered")
    # visualize_graph_k("power_law")


if __name__ == "__main__":
    main()
