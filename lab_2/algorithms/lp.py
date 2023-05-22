from scipy.optimize import linprog
from typing import List, Tuple, Any


comparison_count = 0


def __f(
    c: List[Any], 
    A_ub: List[Any], 
    b_ub: List[Any], 
    A_eq: List[List[Any]], 
    b_eq: List[Any], 
    best_optimum: List[int]
) -> None:
    global best_items
    global comparison_count
    
    fractional_result = linprog(c, A_ub, b_ub, A_eq, b_eq, bounds=(0, 1), method='simplex')
    optimum = -fractional_result['fun']
    items = [round(x, 3) for x in fractional_result['x']]

    comparison_count += 1
    if optimum < best_optimum[0]:
        return
    
    for i in range(len(items)):

        comparison_count += 1
        if not round(items[i], 3).is_integer():
            _A_eq = A_eq.copy()
            _b_eq = b_eq.copy()

            _A_eq.append([0 for _ in range(len(items))])
            _A_eq[-1][i] = 1

            _b_eq += [1]
            __f(c, A_ub, b_ub, _A_eq, _b_eq, best_optimum)
            
            _b_eq[-1] = 0
            __f(c, A_ub, b_ub, _A_eq, _b_eq, best_optimum)

            return
        
    comparison_count += 1
    if optimum > best_optimum[0]:
        best_optimum[0] = optimum
        best_items = items
    return


def solve(
    capacity: int, 
    items_weights: List[int], 
    items_cost: List[int]
) -> Tuple[int, int, List[int], int]:
    global comparison_count

    c = [-x for x in items_cost]
    A_ub = [items_weights]
    b_ub = [capacity]
    A_eq = [[0 for _ in range(len(items_weights))]]
    b_eq = [0]
    best_optimum = [-1]

    __f(c, A_ub, b_ub, A_eq, b_eq, best_optimum)
    
    cost_answer = 0
    result_weight = 0
    items = [int(best_items[i]) for i in range(len(best_items))]

    for i in range(len(items)):
    
        comparison_count += 1
        if items[i] == 1:
            cost_answer += items_cost[i]
            result_weight += items_weights[i]
    
    return cost_answer, result_weight, items, comparison_count