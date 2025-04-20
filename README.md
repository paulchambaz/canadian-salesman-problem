# Covering Canadian Traveller Problem (CCTP)

This project implements and compares two approximation algorithms for the Covering Canadian Traveller Problem (CCTP): Cyclic Routing (CR) with O(√k) approximation ratio and Christofides Nearest Neighbor (CNN) with O(log k) approximation ratio.

## About CCTP

The Covering Canadian Traveller Problem is a variant of the Traveling Salesman Problem (TSP) where a subset of edges may be blocked, and a traveller only discovers a blockage upon reaching and adjacent vertex. The objective is to visit all vertices while minimizing the total distance traveled.

## Algorithms

- **Christofides**: Base algorithm for TSP with 3/2-approximation
- **Cyclic Routing (CR)**: O(√k) approximation for CCTP
- **Christofides Nearest Neighbor (CNN)**: O(log k) approximation for CCTP

## Requirements

```sh
pip install numpy matplotlib networkx tqdm scipy
```

```sh
# Benchmark analysis
python -m scripts.benchmark_ratio_christofides
python -m scripts.benchmark_time_christofides

python -m scripts.benchmark_ratio_cr
python -m scripts.benchmark_time_cr

python -m scripts.benchmark_ratio_cnn
python -m scripts.benchmark_time_cnn

python -m scripts.benchmark_ratio_graphs

# Visualize analysis
python -m scripts.visualize_ratio_christofides
python -m scripts.visualize_time_christofides

python -m scripts.visualize_ratio_cr
python -m scripts.visualize_time_cr

python -m scripts.visualize_ratio_cnn
python -m scripts.visualize_time_cnn

python -m scripts.visualize_ratio_graphs

# Tests
python -m scripts.test_christofides
python -m scripts.test_cr
python -m scripts.test_cnn
```

## Authors

- [Paul Chambaz](https://www.linkedin.com/in/paul-chambaz-17235a158/)
- [Philipp Hanussek](https://www.linkedin.com/in/philipp-hanussek-689bb7249/)

## License

This project is licensed under the GNU General Public License v3.0 - see the LICENSE file for details.
