run *ARGS:
  python -m cctp

full:
  just test
  just benchmark-ratio
  # just visualize-ratio
  just benchmark-time
  # just visualize-time
  just benchmark-graphs
  # just visualize-graphs

visualize:
  just visualize-ratio
  just visualize-time
  just visualize-graphs

test *ARGS:
  python -m scripts.test_christofides {{ ARGS }}
  python -m scripts.test_cr {{ ARGS }}
  python -m scripts.test_cnn {{ ARGS }}

benchmark-ratio *ARGS:
  # python -m scripts.benchmark_ratio_christofides {{ ARGS }}
  python -m scripts.benchmark_ratio_cr {{ ARGS }}
  # python -m scripts.benchmark_ratio_cnn {{ ARGS }}

visualize-ratio *ARGS:
  python -m scripts.visualize_ratio_christofides {{ ARGS }}
  python -m scripts.visualize_ratio_cr {{ ARGS }}
  python -m scripts.visualize_ratio_cnn {{ ARGS }}

benchmark-time *ARGS:
  # python -m scripts.benchmark_time_christofides {{ ARGS }}
  python -m scripts.benchmark_time_cr {{ ARGS }}
  # python -m scripts.benchmark_time_cnn {{ ARGS }}

visualize-time *ARGS:
  python -m scripts.visualize_time_christofides {{ ARGS }}
  python -m scripts.visualize_time_cr {{ ARGS }}
  python -m scripts.visualize_time_cnn {{ ARGS }}

benchmark-graphs *ARGS:
  python -m scripts.benchmark_ratio_graphs {{ ARGS }}

visualize-graphs *ARGS:
  python -m scripts.visualize_ratio_graphs {{ ARGS }}

publish:
  rm -fr dist
  rm -fr RP-paulchambaz-philipphanussek
  mkdir -p RP-paulchambaz-philipphanussek
  mkdir -p RP-paulchambaz-philipphanussek/cctp
  cp -r cctp/*.py RP-paulchambaz-philipphanussek/cctp
  rm RP-paulchambaz-philipphanussek/cctp/__main__.py
  mkdir -p RP-paulchambaz-philipphanussek/scripts
  cp -r scripts/*.py RP-paulchambaz-philipphanussek/scripts
  cp paper/paper.pdf RP-paulchambaz-philipphanussek
  cp README.md RP-paulchambaz-philipphanussek
  zip -r RP-paulchambaz-philipphanussek.zip RP-paulchambaz-philipphanussek
  rm -fr RP-paulchambaz-philipphanussek
  mkdir -p dist
  mv RP-paulchambaz-philipphanussek.zip dist/
