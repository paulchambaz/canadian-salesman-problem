import pickle

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit


def visualize_n():
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

    with open("results/cnn_runtime_n_results.pk", "rb") as f:
        results = pickle.load(f)

    sizes = results["sizes"]

    iqms = [results["data"][n]["iqm"] for n in sizes]
    q1s = [results["data"][n]["q1"] for n in sizes]
    q3s = [results["data"][n]["q3"] for n in sizes]

    roots_iqm = np.sqrt(iqms)
    roots_q1 = np.sqrt(q1s)
    roots_q3 = np.sqrt(q3s)

    def linear_func(x, a, b):
        return a * x + b

    params, _ = curve_fit(linear_func, sizes, roots_iqm)
    a, b = params
    fit_line = linear_func(sizes, a, b)

    ss_tot = np.sum((roots_iqm - np.mean(roots_iqm)) ** 2)
    ss_res = np.sum((roots_iqm - fit_line) ** 2)
    r_squared = 1 - (ss_res / ss_tot)

    plt.figure(figsize=(6, 6))

    plt.fill_between(
        sizes,
        roots_q1,
        roots_q3,
        alpha=0.2,
        color="#3498db",
        label=r"Racine carré de l'IQ",
    )

    plt.plot(
        sizes,
        roots_iqm,
        "o-",
        color="#3498db",
        linewidth=2,
        label="Racine carré de la moyenne IQ",
    )

    plt.plot(
        sizes,
        fit_line,
        "k-",
        linewidth=1,
        label=rf"Courbe linéaire : ${a:.4f}x + {b:.4f}$",
    )

    plt.grid(True, alpha=0.3)
    plt.xlabel("Nombre de sommet (n)")
    plt.ylabel("Racine carré du temps d'exécution")
    plt.legend()

    plt.annotate(
        rf"$R^2$ = {r_squared:.4f}", xy=(0.7, 0.05), xycoords="axes fraction"
    )

    plt.tight_layout()

    plt.savefig("paper/figures/cnn_time_plot_n.svg", bbox_inches="tight")

    # plt.show()


def visualize_k():
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

    with open("results/cnn_runtime_k_results.pk", "rb") as f:
        results = pickle.load(f)

    sizes = results["sizes"]

    iqms = [results["data"][n]["iqm"] for n in sizes]
    q1s = [results["data"][n]["q1"] for n in sizes]
    q3s = [results["data"][n]["q3"] for n in sizes]

    roots_iqm = np.sqrt(iqms)
    roots_q1 = np.sqrt(q1s)
    roots_q3 = np.sqrt(q3s)

    def linear_func(x, a, b):
        return a * x + b

    params, _ = curve_fit(linear_func, sizes, roots_iqm)
    a, b = params
    fit_line = linear_func(sizes, a, b)

    ss_tot = np.sum((roots_iqm - np.mean(roots_iqm)) ** 2)
    ss_res = np.sum((roots_iqm - fit_line) ** 2)
    r_squared = 1 - (ss_res / ss_tot)

    plt.figure(figsize=(6, 6))

    plt.fill_between(
        sizes,
        roots_q1,
        roots_q3,
        alpha=0.2,
        color="#3498db",
        label=r"Racine carré de l'IQ",
    )

    plt.plot(
        sizes,
        roots_iqm,
        "o-",
        color="#3498db",
        linewidth=2,
        label="Racine carré de la moyenne IQ",
    )

    plt.plot(
        sizes,
        fit_line,
        "k-",
        linewidth=1,
        label=rf"Courbe linéaire : ${a:.4f}x + {b:.4f}$",
    )

    plt.grid(True, alpha=0.3)
    plt.xlabel("Nombre de sommet bloqué (k)")
    plt.ylabel("Racine carré du temps d'exécution")
    plt.legend()

    plt.annotate(
        rf"$R^2$ = {r_squared:.4f}", xy=(0.7, 0.05), xycoords="axes fraction"
    )

    plt.tight_layout()

    plt.savefig("paper/figures/cnn_time_plot_k.svg", bbox_inches="tight")

    # plt.show()


def main():
    visualize_n()
    visualize_k()


if __name__ == "__main__":
    main()
