from typing import List, Tuple

def solve(capacity: int, items_weights: List[int], items_cost: List[int]) -> Tuple[int, int, list, int]:
    comparisons_count = 0
    items_size = len(items_cost)
    items = [0 for i in range(items_size)]
    dp = []
    result_weight = 0
    
    for i in range(items_size + 1):
        dp.append([0] * (capacity + 1))
    for i in range(1, items_size + 1):
        for k in range(1, capacity + 1):
            comparisons_count += 1
            if k < items_weights[i - 1]:
                dp[i][k] = dp[i - 1][k]
            else:
                dp[i][k] = max(dp[i - 1][k], dp[i - 1][k - items_weights[i - 1]] + items_cost[i - 1])

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
            get_items(k - 1, s - items_weights[k - 1])
            items[k - 1] = 1
            result_weight += items_weights[k - 1]

    get_items(items_size, capacity)
    return dp[items_size][capacity], result_weight, items, comparisons_count