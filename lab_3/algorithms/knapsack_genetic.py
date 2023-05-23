from typing import List, Tuple
import numpy as np
import random

MAGIC_NUMBER = 54


def crossover_and_mutation_function(chroms: List[int], items_size: int, k: int) -> List[int]:

    crossover = np.random.randint(low=1, high=items_size - 1) // 2
    crossover *= 2

    for j in range(0, k, 2):
        for i in range(crossover):
            chroms[j][i], chroms[j + 1][i] = chroms[j + 1][i], chroms[j][i]

    for j in range(items_size):
        for i in range(len(chroms[j])):
            if np.random.randint(low=1, high=100) == MAGIC_NUMBER:
                chroms[j][i] = (chroms[j][i] + 1) % 2

    return chroms


def fitness_function(chroms: List[int], capacity: int, items_weights: List[int], items_cost: List[int]) -> Tuple[int]:

    result_weights = np.sum(chroms * items_weights)
    result_cost = np.sum(chroms * items_cost)

    while result_weights > capacity:
        nonzero_chrom = np.nonzero(chroms)[0]
        chroms[nonzero_chrom[np.random.randint(
            low=0, high=len(nonzero_chrom) - 1)]] = 0

        result_weights = np.sum(chroms * items_weights)
        result_cost = np.sum(chroms * items_cost)

    return result_cost


def evolve(capacity: int, items_weights: List[int], items_cost: List[int]):

    items_weights, items_cost = np.array(items_weights), np.array(items_cost)
    items_size = len(items_cost)

    chroms_size = 100
    chroms = np.array([[np.random.randint(low=0, high=2)
                      for _ in range(items_size)] for _ in range(chroms_size)])

    k = chroms_size // 4
    k = k // 2
    k *= 2

    fitness_results = []
    for idx_chrom in range(chroms_size):
        fitness_results.append((idx_chrom, fitness_function(chroms[idx_chrom], capacity,
                                                            items_weights, items_cost)))

    fitness_results.sort(key=lambda x: x[1], reverse=True)
    fitness_sum = 0
    for x in fitness_results:
        fitness_sum += x[1]

    selected_chroms = random.choices(
        chroms, weights=[x[0] / fitness_sum for x in fitness_results], k=k)

    selected_chroms = crossover_and_mutation_function(
        selected_chroms, items_size, k)

    new_fitness_results = []
    for idx_chrom in range(len(selected_chroms)):
        new_fitness_results.append((idx_chrom, fitness_function(selected_chroms[idx_chrom], capacity,
                                                                items_weights, items_cost)))

    new_fitness_results.sort(key=lambda x: x[1], reverse=True)

    if new_fitness_results[0][1] > fitness_results[0][1]:
        return selected_chroms[new_fitness_results[0][0]], new_fitness_results[0][1]
    else:
        return chroms[fitness_results[0][0]], fitness_results[0][1]
