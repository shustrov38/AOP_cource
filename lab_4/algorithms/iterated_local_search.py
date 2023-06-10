import random
from typing import List
from .local_search import local_search


def stochastic_two_opt(ans: List[int], i: int, j: int):
    if i == 0:
        new_ans = ans[:i] + ans[j::-1] + ans[j+1:]
    else:
        new_ans = ans[:i] + ans[j:i-1:-1] + ans[j+1:]
    return new_ans


def solve(distances: List[int], flows: List[List[int]]):
    initial_ans = list(range(len(distances)))
    random.shuffle(initial_ans)
    ans, current_ans = local_search(distances, flows, initial_ans)
    count = 0
    n = len(distances)
    i = random.randint(0, n - 2)
    j = max(i + random.randint(1, n // 2), n - 1)
    while count < 100:
        count += 1
        tmp_ans = stochastic_two_opt(ans, i, j)
        tmp_ans, new_ans = local_search(distances, flows, tmp_ans)
        if new_ans < current_ans:
            current_ans = new_ans
            ans = tmp_ans
            count = 0
    return ans, current_ans
