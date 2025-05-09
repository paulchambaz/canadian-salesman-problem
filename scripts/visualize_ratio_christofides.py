import pickle

import matplotlib.pyplot as plt


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

    with open("results/christofides_ratio_results.pk", "rb") as f:
        results = pickle.load(f)

    sizes = results["sizes"]

    iqms = [results["data"][n]["iqm"] for n in sizes]
    mins = [results["data"][n]["min"] for n in sizes]
    maxs = [results["data"][n]["max"] for n in sizes]

    plt.figure(figsize=(6, 6))

    plt.axhline(
        y=1.5,
        color="black",
        linestyle="--",
        linewidth=1.5,
        label=r"ratio $= 1.5$",
    )

    plt.fill_between(
        sizes,
        mins,
        maxs,
        alpha=0.2,
        color="#64a34f",
        label=r"Min et max des ratios",
    )

    plt.plot(
        sizes,
        iqms,
        "^-",
        color="#64a34f",
        linewidth=2.5,
        markersize=8,
        label=r"IQM des ratios",
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
        "paper/figures/christofides_ratio_plot.svg", bbox_inches="tight"
    )


if __name__ == "__main__":
    main()
