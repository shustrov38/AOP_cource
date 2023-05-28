import time
from pathlib import Path
import algorithms.local_search as local_search


BENCHMARKS_PATH = Path('./lab_4') / 'benchmarks'


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
    
    return distances, flows


def benchmark(name: str, iters: int = 100) -> None:

    distance, flows = read_file(name)
    time_sum = 0

    for _ in range(iters):
        start_time = time.monotonic()
        _, _ = local_search.solve(distance, flows)
        end_time = time.monotonic()
        time_sum += end_time - start_time
    mean_time = time_sum / iters

    print(f"Bench: {name}\n")


if __name__ == '__main__':

    benchmark_names = ['tai20a', 'tai40a', 'tai60a', 'tai80a', 'tai100a']

    for benchmark_name in benchmark_names:
        benchmark(benchmark_name)
    print()
