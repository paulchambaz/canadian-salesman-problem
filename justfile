run *ARGS:
  python -m cstp {{ ARGS }}

benchmark *ARGS:
  python -m scripts.benchmark_christofides {{ ARGS }}

test *ARGS:
  python -m scripts.test_christofides {{ ARGS }}

visualize *ARGS:
  python -m scripts.visualize_christofides {{ ARGS }}
