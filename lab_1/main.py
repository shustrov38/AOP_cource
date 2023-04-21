import time
from pathlib import Path

import algorithms.naive as naive
import algorithms.rabin_karp as rabin_karp
import algorithms.boyer_moore as boyer_moore
import algorithms.knuth_moris_pratt as knuth_moris_pratt
import algorithms.aho_corasick as aho_corasick


def unit_tests() -> None:
    print('UNIT TESTS:', end='\n\n')

    modules = [naive, rabin_karp, boyer_moore, knuth_moris_pratt, aho_corasick]
    testcases = [
        ('qwerty', 'qwe', 0),
        ('qwerty', 'wer', 1),
        ('qwerty', 'ert', 2),
        ('qwerty', 'rty', 3),
        ('bcaa', 'caa', 1),
        ('bcaa', 'aa', 2),
    ]

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


def aho_corasick_unit_tests() -> None:
    print('AHO-CORASICK UINT TESTS:', end='\n\n')
    
    testcases = [
        ('gcatcg', ['acc', 'atc', 'cat', 'gcg'], [('cat', 1), ('atc', 2)]),
        ('gcatcg', ['a', 'ab', 'bc', 'c'], [('c', 1), ('a', 2), ('c', 4)]),
    ]

    for i, (text, patterns, answer) in enumerate(testcases):
        print(f'TESTCASE {i:#>2}: {text=} {patterns=}')
        print(f'{aho_corasick.__name__:-<35}')
        trie = aho_corasick.AhoCorasick()
        for pattern in patterns:
            trie.add_pattern(pattern=pattern)
        trie.set_links()
        result = trie.search('gcatcg')
        if sorted(result) != sorted(answer):
            print(f'    ### ERROR: wrong result. {answer} expected. ###')
        for pattern, index in result:
            print(f'    {pattern:6}: {index:5}')
        print()


BENCHMARKS_PATH = Path('./lab_1') / 'benchmarks'


def benchmark(module, name: str, num: int, iters: int = 100) -> None:
    benchmark_name = '%s_%s_%d.txt'
    text_filename = benchmark_name % (name, 't', num)
    pattern_filename = benchmark_name % (name, 'w', num)

    with open(BENCHMARKS_PATH / text_filename, 'r', encoding='utf8') as text_file:
        text = text_file.read()

    with open(BENCHMARKS_PATH / pattern_filename, 'r', encoding='utf8') as pattern_file:
        pattern = pattern_file.read()

    time_sum = 0
    for _ in range(iters):
        start_time = time.monotonic()
        _, comparisons = module.search(text, pattern)
        end_time = time.monotonic()
        time_sum += end_time - start_time
    mean_time = time_sum / iters

    print(text_filename, module.__name__, comparisons, mean_time)

if __name__ == '__main__':
    aho_corasick_unit_tests()
    unit_tests()
    
    modules = [naive, rabin_karp, boyer_moore, knuth_moris_pratt, aho_corasick]
    benchmark_names = ['bad', 'good']
    benchmark_indexes = list(range(1, 5))

    for module in modules:
        for benchmark_name in benchmark_names:
            for benchmark_index in benchmark_indexes:
                benchmark(module, benchmark_name, benchmark_index)
        print()