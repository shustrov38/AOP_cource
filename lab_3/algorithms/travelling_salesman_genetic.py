from typing import List, Tuple
import random


MAGIC_NUMBER = 54


def fitness_function(chroms: List[int], edges_weight: List[List[float]]):
    result = 0
    for i in range(len(chroms) - 1):
        result += edges_weight[chroms[i]][chroms[i + 1]]
    return result


def selection(
    fitness_results: List[Tuple[int, int]],
    chroms_size: int, 
    k: int
) -> List[int]:
    random_list = [1 for _ in range(k)] + [0 for _ in range(chroms_size - k)]
    random.shuffle(random_list)

    selected_chroms = [(i, fitness_results[i]) for i in range(chroms_size) if random_list[i]]
    selected_chroms.sort(key=lambda x: x[1])
    selected_chroms = [i for i, _ in selected_chroms]
    selected_chroms = selected_chroms[:len(selected_chroms) // 2]
    
    return selected_chroms


def crossover_and_mutation_function(
    chroms: List[int], 
    selected_chroms: List[int], 
    num_of_edges: int
) -> List[int]:
    for i in range(0, len(selected_chroms), 2):
        chr1 = chroms[selected_chroms[i + 1]]
        chr2 = chroms[selected_chroms[i]]

        p1 = random.randint(0, num_of_edges - 2)
        p2 = random.randint(p1 + 1, num_of_edges)

        o1 = [-1 for _ in range(num_of_edges)]
        o2 = [-1 for _ in range(num_of_edges)]

        tmp1 = chr1[p2:] + chr1[:p1]
        tmp2 = chr2[p2:] + chr2[:p1]

        for j in range(p1, p2):
            o1[j] = chr1[j]
            if chr1[j] in tmp1:
                tmp1.remove(chr1[j])

            o2[j] = chr2[j]
            if chr2[j] in tmp2:
                tmp2.remove(chr2[j])

        o1[p2:] = tmp1[:num_of_edges - p2]
        o1[:p1] = tmp1[num_of_edges - p2:]

        o2[p2:] = tmp2[:num_of_edges - p2]
        o2[:p1] = tmp2[num_of_edges - p2:]

        if random.randint(1, 100) == MAGIC_NUMBER:
            x = random.randint(0, num_of_edges - 1)
            y = random.randint(0, num_of_edges - 1)
            o1[x], o1[y] = o1[y], o1[x]

        if random.randint(1, 100) == MAGIC_NUMBER:
            x = random.randint(0, num_of_edges - 1)
            y = random.randint(0, num_of_edges - 1)
            o2[x], o2[y] = o2[y], o2[x]

        chroms.append(o1)
        chroms.append(o2)
    
    return chroms


def evolve(edges_weight: List[List[float]], chroms_size: int = 1000, epocs: int = 1):
    num_of_edges = len(edges_weight)
    
    temp = list(range(num_of_edges))
    chroms = []
    for _ in range(chroms_size):
        random.shuffle(temp)
        chroms.append(temp.copy())

    fitness_results = [
        (i, fitness_function(chroms[i], edges_weight)) 
        for i in range(chroms_size)
    ]
    fitness_results.sort(key=lambda x: x[1])

    for _ in range(epocs):
        chroms_size = len(chroms)
        k = chroms_size // 4
        k = k // 4
        k *= 4

        selected_chroms = selection(fitness_results, chroms_size, k)
        chroms = crossover_and_mutation_function(chroms, selected_chroms, num_of_edges)

        fitness_results += [
            (i, fitness_function(chroms[i], edges_weight)) 
            for i in range(chroms_size, len(chroms))
        ]
        fitness_results.sort(key=lambda x: x[1])

    return fitness_results[0][1], [i + 1 for i in chroms[fitness_results[0][0]]]