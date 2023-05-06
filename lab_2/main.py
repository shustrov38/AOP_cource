import time
from pathlib import Path
import algorithms.weights_dp as weights_dp
import algorithms.cost_dp as cost_dp
import algorithms.approx2 as approx2


def unit_tests() -> None:
    print('UNIT TESTS:', end='\n\n')

    modules = [weights_dp, cost_dp, approx2]

    # TODO MORE CASES
    #['capacity': 6, 'weights': [2, 10, 3, 1], 'cost': [3, 5, 4, 2], 'ans': 9]

    testcases = [
        [[6], [2, 10, 3, 1], [3, 5, 4, 2], [9]],
        [[8], [3, 4, 5, 8, 9], [1, 6, 4, 7, 6], [7]]
    ]

    for i, (capacity, weights, cost, true_res) in enumerate(testcases):
        print(f'TESTCASE {i:#>2}: {capacity=}')
        for module in modules:
            ans, res_weights, res_items, comparisons = module.solve(
                capacity[0], weights, cost)
            print(f'{module.__name__:-<35}')
            if true_res[0] != ans:
                print(
                    f'    ### ERROR: wrong answer {ans}. {true_res[0]} expected.')
            print(f'    comparinsons count : {comparisons:5}')
        print()


BENCHMARKS_PATH = Path('./lab_2') / 'benchmarks'


def benchmark(module, name: str, iters: int = 100) -> None:
    """
    _c.txt - the knapsack capacity.
    _w.txt - the weights of the objects.
    _p.txt - the profits of each object.
    _s.txt - the optimal selection of weights.
    """

    with open(BENCHMARKS_PATH / name + "_c.txt", 'r', encoding='utf8') as text_file:
        capasity = text_file.read()

    with open(BENCHMARKS_PATH / name + "_p.txt", 'r', encoding='utf8') as pattern_file:
        weights = pattern_file.read()

    with open(BENCHMARKS_PATH / name + "_s.txt", 'r', encoding='utf8') as pattern_file:
        cost = pattern_file.read()

    with open(BENCHMARKS_PATH / name + "_w.txt", 'r', encoding='utf8') as pattern_file:
        optimal = pattern_file.read()

    time_sum = 0
    for _ in range(iters):
        start_time = time.monotonic()
        ans, res_weights, res_items, comparisons = module.solve(
            capasity, weights, cost)
        end_time = time.monotonic()
        time_sum += end_time - start_time
    mean_time = time_sum / iters

    print(name, module.__name__, ans, comparisons, mean_time)


if __name__ == '__main__':
    unit_tests()

    # modules = [weights_dp, cost_dp]
    # benchmark_names = ['p01', 'p02', 'p03', 'p04', 'p05', 'p06']

    # for module in modules:
    #    for benchmark_name in benchmark_names:
    #        benchmark(module, benchmark_name)
    #    print()
