from typing import List, Tuple
import numpy as np
import random

MAGIC_NUMBER = 54


def selection_function(chroms: List[int], fitness_results: List[int]) -> List[int]:

    chroms_size = len(fitness_results)
    fitness_results.sort(key=lambda x: x[1], reverse=True)
    reordered_chroms = [chroms[idx[0]] for idx in fitness_results]

    first_part = random.choices(
        reordered_chroms[0: chroms_size // 4], k=int(chroms_size // 4 * 0.5))
    second_part = random.choices(
        reordered_chroms[chroms_size // 4: chroms_size // 2], k=int(chroms_size // 4 * 0.3))
    third_part = random.choices(
        reordered_chroms[chroms_size // 2: 3 * chroms_size // 4], k=int(chroms_size // 4 * 0.15))
    fourth_part = random.choices(
        reordered_chroms[3 * chroms_size // 4: chroms_size], k=int(chroms_size // 4 * 0.05))
    
    return first_part + second_part + third_part + fourth_part


def crossover_and_mutation_function(chroms: List[int], items_size: int, selected_size: int) -> List[List[int]]:

    crossover = (np.random.randint(low=1, high=items_size - 1) // 2) * 2

    for j in range(0, selected_size - 1, 2):
        for i in range(crossover):
            chroms[j][i], chroms[j + 1][i] = chroms[j + 1][i], chroms[j][i]

    for j in range(len(chroms)):
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


def evolve(capacity: int, items_weights: List[int], items_cost: List[int], chroms_size: int = 100):

    items_weights, items_cost = np.array(items_weights), np.array(items_cost)
    items_size = len(items_cost)

    chroms = np.array([[np.random.randint(low=0, high=2)
                      for _ in range(items_size)] for _ in range(chroms_size)])

    fitness_results = []
    for idx_chrom in range(chroms_size):
        fitness_results.append((idx_chrom, fitness_function(chroms[idx_chrom], capacity,
                                                            items_weights, items_cost)))

    selected_chroms = selection_function(chroms, fitness_results)

    new_chroms = crossover_and_mutation_function(
        selected_chroms, items_size, len(selected_chroms))
    
    new_fitness_results = []
    for idx_chrom in range(len(new_chroms)):
        new_fitness_results.append((idx_chrom, fitness_function(new_chroms[idx_chrom], capacity,
                                                                items_weights, items_cost)))

    new_fitness_results.sort(key=lambda x: x[1], reverse=True)

    if new_fitness_results[0][1] > fitness_results[0][1]:
        return new_chroms[new_fitness_results[0][0]], new_fitness_results[0][1]
    else:
        return chroms[fitness_results[0][0]], fitness_results[0][1]
