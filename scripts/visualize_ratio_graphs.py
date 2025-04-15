import pickle

import matplotlib.pyplot as plt


def visualize_graph_n(graph_type: str):
    with open(f"results/graphs_ratio_{graph_type}_n_results.pk", "rb") as f:
        results = pickle.load(f)

    sizes = results["sizes"]

    cr_iqms = [results["cr_data"][n]["iqm"] for n in sizes]
    cr_q1s = [results["cr_data"][n]["q1"] for n in sizes]
    cr_q3s = [results["cr_data"][n]["q3"] for n in sizes]

    cnn_iqms = [results["cnn_data"][n]["iqm"] for n in sizes]
    cnn_q1s = [results["cnn_data"][n]["q1"] for n in sizes]
    cnn_q3s = [results["cnn_data"][n]["q3"] for n in sizes]

    plt.figure(figsize=(6, 6))

    plt.fill_between(
        sizes,
        cnn_q1s,
        cnn_q3s,
        alpha=0.2,
        color="#3498db",
        label=r"IQ des ratios CNN",
    )

    plt.plot(
        sizes,
        cnn_iqms,
        "o-",
        color="#3498db",
        linewidth=2.5,
        markersize=8,
        label=r"IQM des ratios CNN",
    )

    plt.fill_between(
        sizes,
        cr_q1s,
        cr_q3s,
        alpha=0.2,
        color="#d66b6a",
        label=r"IQ des ratios CR",
    )

    plt.plot(
        sizes,
        cr_iqms,
        "s-",
        color="#d66b6a",
        linewidth=2.5,
        markersize=8,
        label=r"IQM des ratios CR",
    )

    plt.axhline(
        y=1.0,
        color="black",
        linestyle="-",
        linewidth=1.5,
        label=r"ratio $= 1.0$",
    )

    plt.grid(True, alpha=0.3)
    plt.xlabel(r"Nombre de sommet ($n$)", fontsize=18)
    plt.ylabel(r"Ratio", fontsize=18)

    plt.legend(fontsize=16, framealpha=0.9)
    plt.tight_layout()

    plt.savefig(
        f"paper/figures/graphs_ratio_{graph_type}_n_plot.svg",
        bbox_inches="tight",
    )


def visualize_graph_k(graph_type: str):
    with open(f"results/graphs_ratio_{graph_type}_k_results.pk", "rb") as f:
        results = pickle.load(f)

    sizes = results["sizes"]

    cr_iqms = [results["cr_data"][n]["iqm"] for n in sizes]
    cr_q1s = [results["cr_data"][n]["q1"] for n in sizes]
    cr_q3s = [results["cr_data"][n]["q3"] for n in sizes]

    cnn_iqms = [results["cnn_data"][n]["iqm"] for n in sizes]
    cnn_q1s = [results["cnn_data"][n]["q1"] for n in sizes]
    cnn_q3s = [results["cnn_data"][n]["q3"] for n in sizes]

    plt.figure(figsize=(6, 6))

    plt.fill_between(
        sizes,
        cnn_q1s,
        cnn_q3s,
        alpha=0.2,
        color="#3498db",
        label=r"IQ des ratios CNN",
    )

    plt.plot(
        sizes,
        cnn_iqms,
        "o-",
        color="#3498db",
        linewidth=2.5,
        markersize=8,
        label=r"IQM des ratios CNN",
    )

    plt.fill_between(
        sizes,
        cr_q1s,
        cr_q3s,
        alpha=0.2,
        color="#d66b6a",
        label=r"IQ des ratios CR",
    )

    plt.plot(
        sizes,
        cr_iqms,
        "s-",
        color="#d66b6a",
        linewidth=2.5,
        markersize=8,
        label=r"IQM des ratios CR",
    )

    plt.axhline(
        y=1.0,
        color="black",
        linestyle="-",
        linewidth=1.5,
        label=r"ratio $= 1.0$",
    )

    plt.grid(True, alpha=0.3)
    plt.xlabel(r"Nombre de sommet bloqué ($k$)", fontsize=18)
    plt.ylabel(r"Ratio", fontsize=18)

    plt.legend(fontsize=16, framealpha=0.9)
    plt.tight_layout()

    plt.savefig(
        f"paper/figures/graphs_ratio_{graph_type}_k_plot.svg",
        bbox_inches="tight",
    )


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

    visualize_graph_k("constant")
    visualize_graph_k("euclidian")
    visualize_graph_k("manhattan")
    visualize_graph_k("clustered")
    visualize_graph_k("power_law")


if __name__ == "__main__":
    main()
