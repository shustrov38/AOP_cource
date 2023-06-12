import time
import numpy as np
from pathlib import Path
import algorithms.local_search as local_search
import algorithms.iterated_local_search as iterated_local_search


BENCHMARKS_PATH = Path('./lab_4') / 'benchmarks'
BENCHMARKS_LS_ANSWERS_PATH = Path('./lab_4') / 'local_search_answers'

def read_file(name):
    
    with open(BENCHMARKS_PATH / name, 'r') as bench_file:
        bench_data = bench_file.readlines()
        n = int(bench_data[0])
        
        distances = []
        for idx in range(n):
            distances.append(list(map(int, bench_data[idx + 1].split())))
            
        flows = []
        for idx in range(n + 1, 2 * n + 1):
            flows.append(list(map(int, bench_data[idx + 1].split())))
    
    return np.array(distances), np.array(flows)


def benchmark(module, name: str, iters: int = 100) -> None:

    distance, flows = read_file(name)
    time_sum = 0

    results = []
    for _ in range(iters):
        start_time = time.monotonic()
        results.append((module.solve(distance, flows)))
        end_time = time.monotonic()
        time_sum += end_time - start_time
    mean_time = time_sum / iters

    final_ans, final_summary_dist = sorted(results, key=lambda t: t[1])[0]
    
    print(f"Bench: {name}\n Ans: {final_ans}\n Summary distance: {final_summary_dist}\n Time: {mean_time}\n")

    with open(BENCHMARKS_LS_ANSWERS_PATH / f'{name}.sol', 'a+') as file:
        print(' '.join(list(map(str, final_ans))), file=file)


if __name__ == '__main__':

    benchmark_names = ['tai20a', 'tai40a', 'tai60a', 'tai80a', 'tai100a']
    modules = [local_search, iterated_local_search]
    
    for module in modules:
        for benchmark_name in benchmark_names:
            benchmark(module, benchmark_name, iters=10)
        print()
