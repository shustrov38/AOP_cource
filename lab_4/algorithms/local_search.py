import numpy as np


def generate_answer(distances, flows, ans):

    summuary_dist = 0
    for idx in range(len(distances)):
        summuary_dist += sum(distances[idx] * flows[ans[idx], ans])

    return summuary_dist


def local_search(distances, flows, current_ans):

    current_summary_dist = generate_answer(distances, flows, current_ans)
    dont_look_bits = np.zeros(len(distances))

    u = 0
    while u < len(distances):

        if dont_look_bits[u] == 1:
            u += 1
            continue

        improve_summary_dist = False
        for v in range(u + 1, len(distances)):
            
            new_ans = current_ans.copy()
            new_summuary_dist = current_summary_dist.copy()
            new_ans[u], new_ans[v] = new_ans[v], new_ans[u]
            
            new_summuary_dist += sum(distances[u] * flows[new_ans[u]]) - sum(distances[u] * flows[new_ans[v]])
            new_summuary_dist += sum(distances[v] * flows[new_ans[v]]) - sum(distances[v] * flows[new_ans[u]])
    
            if new_summuary_dist < current_summary_dist:
                current_ans = new_ans
                current_summary_dist = new_summuary_dist
                improve_summary_dist = True
                u = 0
                break

        if not improve_summary_dist:
            dont_look_bits[u] = 1
        u += 1

    return current_summary_dist, current_ans


def solve(distances, flows):

    initial_ans = np.arange(len(distances))
    np.random.shuffle(initial_ans)

    return local_search(distances, flows, initial_ans)
