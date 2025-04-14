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

    with open("results/cr_ratio_k_results.pk", "rb") as f:
        results = pickle.load(f)

    sizes = np.array(results["sizes"])

    iqms = np.array([results["data"][n]["iqm"] for n in sizes])

    def func(x, a, b):
        return a * np.sqrt(x) + b

    params_log, _ = curve_fit(func, sizes, iqms)
    a_log, b_log = params_log
    fit_log = func(sizes, a_log, b_log)

    ss_tot = np.sum((iqms - np.mean(iqms)) ** 2)
    ss_res_log = np.sum((iqms - fit_log) ** 2)
    r_squared_log = 1 - (ss_res_log / ss_tot)

    plt.figure(figsize=(6, 6))

    plt.plot(
        sizes,
        fit_log,
        "--",
        color="black",
        linewidth=1.5,
        label=rf"${a_log:.4f} \sqrt(n) + {b_log:.4f}$",
    )

    plt.plot(
        sizes,
        iqms,
        "o-",
        color="#3498db",
        linewidth=2,
        label="Ratios du graphe de borne serrée",
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

    plt.annotate(
        rf"$R^2$ = {r_squared_log:.4f}",
        xy=(0.7, 0.1),
        xycoords="axes fraction",
    )

    plt.tight_layout()

    plt.savefig("paper/figures/cr_ratio_plot.svg", bbox_inches="tight")

    plt.show()


if __name__ == "__main__":
    main()
