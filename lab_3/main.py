import time
import math
from pathlib import Path
from typing import List, Tuple
import algorithms.knapsack_genetic as knapsack_genetic
import algorithms.travelling_salesman_genetic as travelling_salesman_genetic




KNAPSACK_BENCHMARKS_PATH = Path('./lab_3') / 'benchmarks' / 'knapsack'
TSP_BENCHMARKS_PATH = Path('./lab_3') / 'benchmarks' / 'travelling_salesman'


def knapsack_benchmark(name: str, iters: int = 100) -> None:
    """
    _c.txt - the knapsack capacity.
    _w.txt - the weights of the objects.
    _p.txt - the profits of each object.
    _s.txt - the optimal selection of weights.
    """
    print("Knapsack evolution algorithm")

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
    chroms_size = 100
    
    for _ in range(iters):
        start_time = time.monotonic()
        iterration, final_chroms, knapsack_result = knapsack_genetic.evolve(
            capacity, weights, cost, chroms_size)
        end_time = time.monotonic()
        time_sum += end_time - start_time
    mean_time = time_sum / iters

    print(f"Bench: {name} Answer: {optimal} \nAlgorithm solve: iter - {iterration}, {final_chroms}, {knapsack_result}, {mean_time}\n")


def euclidean_distance(a: Tuple[float, float], b: Tuple[float, float]) -> float:
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def parse_adjaecency_matrix(lines: List[str]) -> List[List[float]]:
    edge_weights = [list(map(float, line.split())) for line in lines]
    return edge_weights


def parse_coordinates(lines: List[str]) -> List[List[float]]:
    coords = [tuple(map(float, line.split())) for line in lines]
    edge_weights = []
    for i in range(len(coords)):
        edge_weights.append([euclidean_distance(coords[i], coords[j]) for j in range(len(coords))])
    return edge_weights


def travelling_salesman_benchmark(edges_weights: List[List[float]], iters: int = 100) -> None:
    answers = []
    time_sum = 0
    for _ in range(iters):
        start_time = time.monotonic()
        answer = travelling_salesman_genetic.evolve(edges_weights, epocs=50)
        end_time = time.monotonic()
        answers.append(answer)
        time_sum += end_time - start_time
    mean_time = time_sum / iters

    print(f"Bench: {benchmark}")
    print(f"time {mean_time}")
    best_answer = min(list(map(lambda x: x[1], answers)))
    print(f'answer: {best_answer}')
    for i in answers:
        if i[1] == best_answer:
            print(f'path: {i[0]}')
            break
    print()



if __name__ == '__main__':

    knapsack_benchmark_names = ['p01', 'p02', 'p03', 'p04', 'p05', 'p06', 'p07']

    for benchmark_name in knapsack_benchmark_names:
        knapsack_benchmark(benchmark_name)
     
    print()

    salesman_benchmarks = {
        'a280': (open(f'{TSP_BENCHMARKS_PATH}/a280.tsp', 'r').readlines()[6:-1], parse_coordinates),
        'att48': (open(f'{TSP_BENCHMARKS_PATH}/att48.tsp', 'r').readlines()[6:-1], parse_coordinates),
        'bays29': (open(f'{TSP_BENCHMARKS_PATH}/bays29.tsp', 'r').readlines()[8:37], parse_adjaecency_matrix),
        'ch150': (open(f'{TSP_BENCHMARKS_PATH}/ch150.tsp', 'r').readlines()[6:-1], parse_coordinates),
        'fl417': (open(f'{TSP_BENCHMARKS_PATH}/fl417.tsp', 'r').readlines()[6:-1], parse_coordinates),
        'gr17': (open(f'{TSP_BENCHMARKS_PATH}/gr17.tsp', 'r').readlines()[8:-1], parse_adjaecency_matrix),
    }

    for benchmark in salesman_benchmarks:
        lines, parser = salesman_benchmarks[benchmark]
        edges_weights = parser(lines)
        travelling_salesman_benchmark(edges_weights, iters=3)
