import numpy as np

name = 'LS'


def compute_summary_dist(distances, flows, current_ans):

    summuary_dist = 0
    for idx in range(len(distances)):
        summuary_dist += np.sum(distances[idx] * flows[current_ans[idx], current_ans])

    return summuary_dist


def swap_and_compute_summary_dist(distances, flows, current_ans, u, v, current_summary_dist):

    current_summary_dist -= (np.sum(distances[u] * flows[current_ans[u], current_ans]) + 
                             np.sum(distances[v] * flows[current_ans[v], current_ans]))

    current_ans[u], current_ans[v] = current_ans[v], current_ans[u]

    current_summary_dist += (np.sum(distances[u] * flows[current_ans[u], current_ans]) + 
                             np.sum(distances[v] * flows[current_ans[v], current_ans]))

    return current_ans, current_summary_dist


def local_search(distances, flows, current_ans):
    
    n = len(distances)
    current_summary_dist = compute_summary_dist(distances, flows, current_ans)
    dont_look_bits = np.zeros(n)

    u = 0
    while u < n:
        if dont_look_bits[u] == 1:
            u += 1
            continue

        improved_ans = False
        for v in range(u + 1, n):

            new_ans, new_summary_dist = swap_and_compute_summary_dist(
                distances, flows, current_ans.copy(), u, v, current_summary_dist)

            if new_summary_dist < current_summary_dist:
                current_ans = new_ans
                current_summary_dist = new_summary_dist
                improved_ans = True
                u = 0
                break

        if not improved_ans:
            dont_look_bits[u] = 1

        u += 1

    return current_ans, current_summary_dist


def solve(distances, flows):
    initial_ans = np.arange(len(distances))
    np.random.shuffle(initial_ans)

    return local_search(distances, flows, initial_ans)
