from typing import List, Tuple


def C_max_greed(capacity: int, items_weights: List[int], items_cost: List[int]) -> Tuple[int, int, list, int]:

    comparisons_count, cost_answer, residual_capacity = 0, 0, capacity
    items_size = len(items_cost)
    items = [0 for _ in range(items_size)]
    items_arr = [(i, items_cost[i], items_weights[i])
                 for i in range(items_size)]
    items_arr.sort(key=lambda x: x[1], reverse=True)

    for item in items_arr:
        comparisons_count += 1
        if residual_capacity > item[2]:
            residual_capacity -= item[2]
            items[item[0]] = 1
            cost_answer += item[1]

    return cost_answer, capacity - residual_capacity, items, comparisons_count


def C_greed(capacity: int, items_weights: List[int], items_cost: List[int]) -> Tuple[int, int, list, int]:

    comparisons_count, cost_answer, residual_capacity = 0, 0, capacity
    items_size = len(items_cost)
    items = [0 for x in range(items_size)]
    items_arr = [(i, items_cost[i] / items_weights[i])
                 for i in range(items_size)]
    items_arr.sort(key=lambda x: x[1], reverse=True)

    for item in items_arr:
        comparisons_count += 1
        if residual_capacity > items_weights[item[0]]:
            residual_capacity -= items_weights[item[0]]
            items[item[0]] = 1
            cost_answer += items_cost[item[0]]

    return cost_answer, capacity - residual_capacity, items, comparisons_count


def solve(capacity: int, items_weights: List[int], items_cost: List[int]):
    
    cost_answer_1, result_weight_1, items_1, comparisons_count_1 = C_max_greed(
        capacity, items_weights, items_cost)
    
    cost_answer_2, result_weight_2, items_2, comparisons_count_2 = C_greed(
        capacity, items_weights, items_cost)
    
    if cost_answer_1 > cost_answer_2:
        return cost_answer_1, result_weight_1, items_1, comparisons_count_1
    else:
        return cost_answer_2, result_weight_2, items_2, comparisons_count_2