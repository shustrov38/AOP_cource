import random
from typing import List, Tuple
import numpy as np


def fitness_function(chrom: List[int], capacity: int, items_weights: List[int], items_cost: List[int]) -> Tuple[int, int]:
    
    result_weights = chrom * items_weights
    result_cost = chrom * items_cost

    while result_weights > capacity:
        nonzero_chrom = np.nonzero(chrom)[0]
        chrom[nonzero_chrom[random.randint(0, len(nonzero_chrom) - 1)]] = 0
        
        result_weights = chrom * items_weights
        result_cost = chrom * items_cost
    
    return result_cost


def evolve(capacity: int, items_weights: List[int], items_cost: List[int], ):
    
    items_weights, items_cost = np.array(items_weights), np.array(items_cost)
    items_size = len(items_cost)
    
    chroms_size = 100
    chroms = np.array([[random.randint(0, 1) for x in range(items_size)] for _ in range(chroms_size)])
    
    k = chroms_size // 4
    k = k // 2
    k *= 2
    
    fitness_results = []
    for chrom in range(chroms_size):
        fitness_results.append((chrom, fitness_function(chroms[chrom], capacity, 
                                                items_weights, items_cost)))
        
    fitness_results.sort(key=lambda x: x[1], reverse=True)
    fitness_sum = 0
    for x in fitness_results:
        fitness_sum += x[1]
        
    p = [x[0] / fitness_sum for x in fitness_results]
    selected_chroms = random.choices(chroms, weights=p, k=k)