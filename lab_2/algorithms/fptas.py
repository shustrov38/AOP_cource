from typing import List, Tuple
from .cost_dp import solve as cost_dp_solve
from .approx2 import solve as approx2_solve
from math import floor


def solve(capacity: int, items_weights: List[int], items_cost: List[int], E: float = 0.01) -> Tuple[int, int, list, int]:

    cost_answer = 0
    items_size = len(items_cost)

    approx2_results = approx2_solve(capacity, items_weights, items_cost)
    alpha = approx2_results[0] * E / items_size
    #print(approx2_results, alpha)
    new_items_cost = [floor(items_cost[i] / alpha) for i in range(items_size)]

    _, cdp_weight, cdp_items, cdp_comparisons_count = cost_dp_solve(
        capacity, items_weights, new_items_cost)

    cdp_comparisons_count += approx2_results[3]
    for i in range(items_size):
        cdp_comparisons_count += 1
        if cdp_items[i] == 1:
            cost_answer += items_cost[i]
    return cost_answer, cdp_weight, cdp_items, cdp_comparisons_count
