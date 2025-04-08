import pickle

import matplotlib.pyplot as plt
import numpy as np


def main():
    with open("results/cnn_ratio_k_results.pk", "rb") as f:
        results = pickle.load(f)

    sizes = np.array(results["sizes"])
    iqms = np.array([results["data"][n]["iqm"] for n in sizes])
    mins = np.array([results["data"][n]["min"] for n in sizes])
    maxs = np.array([results["data"][n]["max"] for n in sizes])

    max_ratio = results["data"][sizes[-1]]["max"]

    k_values_safe = sizes + 1

    max_log = np.log(k_values_safe[-1])
    scaled_log_bound = 1 + (max_ratio - 1) * np.log(k_values_safe) / max_log

    plt.figure(figsize=(6, 6))

    plt.plot(
        sizes,
        scaled_log_bound,
        color="black",
        label="log(k) bound (scaled)",
    )

    plt.fill_between(
        sizes,
        mins,
        maxs,
        alpha=0.2,
        color="#3498db",
        label="IQ range (25%-75%)",
    )

    plt.plot(
        sizes, iqms, "o-", color="#3498db", linewidth=2, label="IQM of ratios"
    )

    plt.axhline(y=1.0, color="black", label="ratio=1.0")

    plt.grid(True, alpha=0.3)
    plt.xlabel("Number of blocked edges (k)")
    plt.ylabel("Ratio")
    plt.legend()

    plt.tight_layout()
    plt.savefig("cnn_vs_scaled_log_bound.png")
    plt.show()


if __name__ == "__main__":
    main()
