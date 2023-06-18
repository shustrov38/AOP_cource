import math
import random
import numpy as np



def fitness(cells_machines, cells_parts, arr, num_of_cells):
    n_1 = 0
    n_0_in = 0
    n_1_out = 0
    for x in arr:
        for y in x:
            n_1_out += y
    for i in range(num_of_cells):
        for machines in cells_machines[i]:
            for detail in cells_parts[i]:
                n_1 += arr[machines][detail]
                if arr[machines][detail] == 0:
                    n_0_in += 1
    n_1_out -= n_1
    if (n_1 + n_0_in) == 0:
        return
    return (n_1 - n_1_out) / (n_1 + n_0_in)


def single_move(current_solve, arr, num_of_cells):
    n = len(arr[0])
    cells_parts = current_solve[1].copy()
    best_f = -9999
    best_cells_parts = []
    best_cells_machine = []
    detail_to_move = random.randint(0, n - 1)
    old_cell = 0
    for i in range(len(cells_parts)):
        if detail_to_move in cells_parts[i]:
            old_cell = i
            cells_parts[old_cell].remove(detail_to_move)
            break
    for i in range(len(cells_parts)):
        if i != old_cell:
            cells_parts[i].append(detail_to_move)
            new_cells_machine = machines_cells_selecting(
                arr, cells_parts, num_of_cells
            )
            new_f = fitness(new_cells_machine, cells_parts, arr, num_of_cells)
            if new_f > best_f:
                best_cells_machine = new_cells_machine.copy()
                best_cells_parts = cells_parts.copy()
                best_f = new_f
            cells_parts[i].remove(detail_to_move)
    cells_parts[old_cell].append(detail_to_move)
    return best_f, best_cells_parts, best_cells_machine


def exchange_move(current_solve, arr, num_of_cells):
    n = len(arr[0])  
    cells_parts = current_solve[1].copy()
    best_f = -9999
    best_cells_parts = []
    best_cells_machine = []
    detail_to_move = random.randint(0, n - 1)
    old_cell = 0
    for i in range(len(cells_parts)):
        if detail_to_move in cells_parts[i]:
            old_cell = i
            cells_parts[old_cell].remove(detail_to_move)
            break
    for i in range(len(cells_parts)):
        if i != old_cell and len(cells_parts[i]) != 0:
            detail_to_move2 = cells_parts[i][
                random.randint(0, len(cells_parts[i]) - 1)
            ]
            cells_parts[i].append(detail_to_move)
            cells_parts[i].remove(detail_to_move2)
            cells_parts[old_cell].append(detail_to_move2)
            new_cells_machine = machines_cells_selecting(
                arr, cells_parts, num_of_cells
            )
            new_f = fitness(new_cells_machine, cells_parts, arr, num_of_cells)
            if new_f > best_f:
                best_cells_machine = new_cells_machine.copy()
                best_cells_parts = cells_parts.copy()
                best_f = new_f
            cells_parts[i].remove(detail_to_move)
            cells_parts[i].append(detail_to_move2)
            cells_parts[old_cell].remove(detail_to_move2)
    cells_parts[old_cell].append(detail_to_move)
    return best_f, best_cells_parts, best_cells_machine


def machines_cells_selecting(arr, cells_parts, num_of_cells):
    m = len(arr) 
    cells_machines = [[] for x in range(num_of_cells)]
    for machine in range(m):
        error = [0 for x in range(num_of_cells)]
        for cell in range(num_of_cells):
            for detail in cells_parts[cell]:
                if arr[machine][detail] == 0:
                    error[cell] += 1
                else:
                    for i in range(num_of_cells):
                        if i != cell:
                            error[i] += 1

        ans = np.argmin(error)
        cells_machines[ans].append(machine)

    return cells_machines

def S(idx_i, idx_j, arr):
    both_counter = 0
    only_i_counter = 0
    only_j_counter = 0
    for x in range(len(arr)):
        if arr[x][idx_i] == 1 and arr[x][idx_j] == 1:
            both_counter += 1
        elif arr[x][idx_i] == 1:
            only_i_counter += 1
        elif arr[x][idx_j] == 1:
            only_j_counter += 1

    return both_counter / (both_counter + only_j_counter + only_i_counter)

def solve(arr):
    num_of_cells = 2

    n = len(arr[0]) 
    m = len(arr) 
    b = [[0 for x in range(n)] for y in range(n)]

    similarity = []

    for i in range(n):
        for j in range(i + 1, n):
            b[i][j] = S(i, j, arr)
            if b[i][j] != 0:
                similarity.append((b[i][j], i, j))
    similarity.sort(reverse=True)
    best_solve = [-9, [], []]

    stage1 = True
    while True:
        if stage1:
            delta = [
                similarity[(x + 1) * int(math.sqrt(len(similarity)))][0]
                for x in range(num_of_cells - 1)
            ]
            cells_parts = [[] for x in range(num_of_cells)]
            cells_parts[0].append(similarity[0][1])
            cells_parts[0].append(similarity[0][2])
            delta_counter = 0
            for i in range(1, len(similarity)):
                if similarity[i][0] > delta[delta_counter]:
                    if similarity[i][1] not in cells_parts[delta_counter]:
                        cells_parts[delta_counter].append(similarity[i][1])
                    if similarity[i][2] not in cells_parts[delta_counter]:
                        cells_parts[delta_counter].append(similarity[i][2])
                else:
                    delta_counter += 1
                if delta_counter == num_of_cells - 1:
                    break
            for detail in range(n):
                f = True
                for i in range(num_of_cells - 1):
                    if detail in cells_parts[i]:
                        f = False
                if f:
                    cells_parts[num_of_cells - 1].append(detail)
            cells_machines = machines_cells_selecting(arr, cells_parts, num_of_cells)

            current_best_solve = (
                fitness(cells_machines, cells_parts, arr, num_of_cells),
                cells_parts,
                cells_machines,
            )  
            if current_best_solve[0] > best_solve[0]:
                best_solve = current_best_solve  
            current_solve = current_best_solve 
            T_0 = 1
            T_f = 0.2
            T = T_0
            alpha = 0.5
            L = 1000
            D = 10
            counter = 0
            counter_mc = 0
            counter_trapped = 0
            counter_stagnant = 0

        stage1 = False
        while counter_mc < L and counter_trapped < L / 2:
            new_solve = single_move(current_solve, arr, num_of_cells)  # S_c
            if counter % D == 0:
                new_solve = exchange_move(current_solve, arr, num_of_cells)
            if new_solve[0] > current_best_solve[0]:
                current_best_solve = new_solve
                counter_stagnant = 0
                counter_mc += 1
                current_solve = new_solve
                continue
            if new_solve[0] == current_best_solve[0]:
                current_solve = new_solve
                counter_stagnant += 1
                counter_mc += 1
                continue
            delta = new_solve[0] - current_solve[0]
            if math.e ** (delta / T) > random.uniform(0, 1):
                current_solve = new_solve
                counter_trapped = 0
            else:
                counter_trapped += 1
            counter_mc += 1
        if T <= T_f or counter_stagnant > 100:
            if current_best_solve[0] > best_solve[0]:
                best_solve = current_best_solve
                num_of_cells += 1
                stage1 = True
            else:
                break
        else:
            T = T * alpha
            counter_mc = 0
            counter += 1
            continue
        
    return best_solve
