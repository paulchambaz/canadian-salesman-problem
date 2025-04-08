import pickle

import matplotlib.pyplot as plt


def main():
    with open("results/christofides_ratio_results.pk", "rb") as f:
        results = pickle.load(f)

    sizes = results["sizes"]

    iqms = [results["data"][n]["iqm"] for n in sizes]
    mins = [results["data"][n]["min"] for n in sizes]
    maxs = [results["data"][n]["max"] for n in sizes]

    plt.figure(figsize=(6, 6))

    plt.axhline(y=1.5, color="black", label="ratio=1.5")

    plt.fill_between(
        sizes,
        mins,
        maxs,
        alpha=0.2,
        color="#3498db",
        label="Min and max of ratios",
    )

    plt.plot(
        sizes,
        iqms,
        "o-",
        color="#3498db",
        linewidth=2,
        label="IQM of ratios",
    )

    plt.axhline(y=1.0, color="black", label="ratio=1.0")

    plt.grid(True, alpha=0.3)
    plt.xlabel("Number of vertices (n)")
    plt.ylabel("Ratio")
    plt.legend()

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
