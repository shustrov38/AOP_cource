import time
from pathlib import Path

import algorithms.weights_dp as weights_dp
import algorithms.cost_dp as cost_dp


def unit_tests() -> None:
    print('UNIT TESTS:', end='\n\n')
    
    """
    TODO
    
    modules = [weights_dp, cost_dp]
    testcases = [    ]

    for i, (text, pattern, answer_index) in enumerate(testcases):
        print(f'TESTCASE {i:#>2}: {text=} {pattern=}')
        for module in modules:
            index, comparisons = module.search(text, pattern)
            print(f'{module.__name__:-<35}')
            if index != answer_index:
                print(f'    ### ERROR: wrong index substring index. {answer_index} expected.')
            print(f'    substring index    : {index:5}')
            print(f'    comparinsons count : {comparisons:5}')
        print()
    """ 
    


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
        ans, weights, items, comparisons = module.solve(capasity, weights, cost)
        end_time = time.monotonic()
        time_sum += end_time - start_time
    mean_time = time_sum / iters

    print(name, module.__name__, ans, comparisons, mean_time)

if __name__ == '__main__':
    aho_corasick_unit_tests()
    unit_tests()
    
    modules = [weights_dp, cost_dp]
    benchmark_names = ['p01', 'p02', 'p03', 'p04', 'p05', 'p06']

    for module in modules:
        for benchmark_name in benchmark_names:
            benchmark(module, benchmark_name)
        print()