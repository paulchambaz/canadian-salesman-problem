import pickle

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit


def main():
    with open("results/christofides_runtime_results.pk", "rb") as f:
        results = pickle.load(f)

    sizes = results["sizes"]

    iqms = [results["data"][n]["iqm"] for n in sizes]
    q1s = [results["data"][n]["q1"] for n in sizes]
    q3s = [results["data"][n]["q3"] for n in sizes]

    cube_roots_iqm = np.cbrt(iqms)
    cube_roots_q1 = np.cbrt(q1s)
    cube_roots_q3 = np.cbrt(q3s)

    def linear_func(x, a, b):
        return a * x + b

    params, _ = curve_fit(linear_func, sizes, cube_roots_iqm)
    a, b = params
    fit_line = linear_func(sizes, a, b)

    ss_tot = np.sum((cube_roots_iqm - np.mean(cube_roots_iqm)) ** 2)
    ss_res = np.sum((cube_roots_iqm - fit_line) ** 2)
    r_squared = 1 - (ss_res / ss_tot)

    plt.figure(figsize=(10, 6))

    plt.fill_between(
        sizes,
        cube_roots_q1,
        cube_roots_q3,
        alpha=0.2,
        color="#3498db",
        label="Cube root of IQ range (25%-75%)",
    )

    plt.plot(
        sizes,
        cube_roots_iqm,
        "o-",
        color="#3498db",
        linewidth=2,
        label="Cube root of IQM runtime",
    )

    plt.plot(
        sizes,
        fit_line,
        "k-",
        linewidth=1,
        label=f"Linear fit: {a:.2e}x + {b:.2e}",
    )

    plt.grid(True, alpha=0.3)
    plt.xlabel("Number of vertices (n)")
    plt.ylabel("Cube root of runtime (s^(1/3))")
    plt.legend()

    plt.annotate(
        f"R² = {r_squared:.4f}", xy=(0.05, 0.95), xycoords="axes fraction"
    )

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
