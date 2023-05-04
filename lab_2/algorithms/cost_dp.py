from typing import List
import scipy

def solve(capacity: int, items_weights: List[int], items_cost: List[int]):
    comparisons_count = 0
    items_size = len(items_cost)
    C = sum(items_cost)
    dp = []
    
    for i in range(items_size + 1):
        dp.append([capacity+1] * (C + 1))
    dp[0][0] = 0
    
    for j in range(1, items_size + 1):
        for k in range(1, C + 1):
            comparisons_count += 1
            if k < items_cost[j - 1]:
                dp[j][k] = dp[j - 1][k]
            else:
                dp[j][k] = min(dp[j - 1][k], dp[j - 1][k - items_cost[j - 1]] + items_weights[j - 1])


    items = [0 for i in range(items_size)]
    result_weight = 0

    def get_items(k, s):
        nonlocal result_weight
        nonlocal comparisons_count
        comparisons_count += 1
        
        if dp[k][s] == 0:
            return
        comparisons_count += 1
        if dp[k - 1][s] == dp[k][s]:
            get_items(k - 1, s)
        else:
            get_items(k - 1, s - items_cost[k - 1])
            items[k - 1] = 1
            result_weight += items_weights[k - 1]

    cost_answer = -1
    for i in range(C, -1, -1):
        comparisons_count += 1
        if dp[items_size][i] < capacity + 1:
            cost_answer = i
            break
    get_items(items_size, cost_answer)

    return cost_answer, result_weight, items, comparisons_count