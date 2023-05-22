import time
from pathlib import Path
import algorithms.knapsack_genetic as knapsack_genetic


KNAPSACK_BENCHMARKS_PATH = Path('./lab_3') / 'benchmarks' / 'knapsack'
TSP_BENCHMARKS_PATH = Path('./lab_3') / 'benchmarks' / 'TSP'


def knapsack_benchmark(module, name: str, iters: int = 100) -> None:
    """
    _c.txt - the knapsack capacity.
    _w.txt - the weights of the objects.
    _p.txt - the profits of each object.
    _s.txt - the optimal selection of weights.
    """

    with open(KNAPSACK_BENCHMARKS_PATH / (name + "_c.txt"), 'r', encoding='utf8') as text_file:
        capacity = int(text_file.read())

    with open(KNAPSACK_BENCHMARKS_PATH / (name + "_w.txt"), 'r', encoding='utf8') as pattern_file:
        weights = pattern_file.read()
        weights = list(map(int, weights.split()))

    with open(KNAPSACK_BENCHMARKS_PATH / (name + "_p.txt"), 'r', encoding='utf8') as pattern_file:
        cost = pattern_file.read()
        cost = list(map(int, cost.split()))

    with open(KNAPSACK_BENCHMARKS_PATH / (name + "_s.txt"), 'r', encoding='utf8') as pattern_file:
        optimal = pattern_file.read()
        optimal = list(map(int, optimal.split()))
        
    time_sum = 0
    for _ in range(iters):
        start_time = time.monotonic()
        res_cost, res_weight, res_items, comparisons = knapsack_genetic.evolve(
            capacity, weights, cost)
        end_time = time.monotonic()
        time_sum += end_time - start_time
    mean_time = time_sum / iters

    print(name, module.__name__, res_items, comparisons, mean_time)


if __name__ == '__main__':

    knapsack_benchmark_names = ['p01', 'p02', 'p03', 'p04', 'p05', 'p06', 'p07']

    #benchmarks for knapsack
    for benchmark_name in knapsack_benchmark_names:
        knapsack_benchmark(benchmark_name)
    print()