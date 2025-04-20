import pickle

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit


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

    with open("results/cr_ratio_results.pk", "rb") as f:
        results = pickle.load(f)

    sizes = np.array(results["sizes"])

    iqms = np.array([results["data"][n]["iqm"] for n in sizes])
    mins = np.array([results["data"][n]["min"] for n in sizes])
    maxs = np.array([results["data"][n]["max"] for n in sizes])

    squared_iqm = np.square(iqms)
    squared_min = np.square(mins)
    squared_max = np.square(maxs)

    def linear_func(x, a, b):
        return a * x + b

    params, _ = curve_fit(linear_func, sizes, squared_iqm)
    a, b = params
    fit_line = linear_func(sizes, a, b)

    ss_tot = np.sum((squared_iqm - np.mean(squared_iqm)) ** 2)
    ss_res = np.sum((squared_iqm - fit_line) ** 2)
    r_squared = 1 - (ss_res / ss_tot)

    plt.figure(figsize=(6, 6))

    plt.plot(
        sizes,
        squared_iqm,
        "o-",
        color="#d66b6a",
        linewidth=2,
        label="Carré du ratios du graphe de borne serrée",
    )

    plt.fill_between(
        sizes,
        squared_min,
        squared_max,
        alpha=0.2,
        color="#d66b6a",
        label=r"Carré du min et max des ratios",
    )

    plt.plot(
        sizes,
        fit_line,
        color="black",
        linestyle="--",
        linewidth=1.5,
        label=rf"Courbe linéaire : ${a:.4f}x + {b:.4f}$",
    )

    plt.axhline(
        y=1.0,
        color="black",
        linestyle="-",
        linewidth=1.5,
        label=r"ratio $= 1.0$",
    )

    plt.grid(True, alpha=0.3)
    plt.xlabel("Nombre de sommet (n)")
    plt.ylabel("Ratio")
    plt.legend()

    plt.grid(True, alpha=0.3)
    plt.xlabel("Nombre de sommet bloqué (k)")
    plt.ylabel("Carré du temps d'exécution")
    plt.legend(loc="upper left")
    plt.annotate(
        rf"$R^2$ = {r_squared:.4f}", xy=(0.68, 0.05), xycoords="axes fraction"
    )

    plt.tight_layout()

    plt.savefig("paper/figures/cr_ratio_plot.svg", bbox_inches="tight")


if __name__ == "__main__":
    main()
