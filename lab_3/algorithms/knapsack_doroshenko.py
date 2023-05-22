import random


def fitness_function(chromosome, items_c, items_w):
    
    ans_w = 0
    ans_c = 0
    for i in range(len(chromosome)):
        ans_w += chromosome[i] * items_w[i]
        ans_c += chromosome[i] * items_c[i]
    return ans_c, ans_w


def remove_random_item(chromosome):
    one_positions = []
    for i in range(len(chromosome)):
        if chromosome[i] == 1:
            one_positions.append(i)
    chromosome[one_positions[random.randint(0, len(one_positions) - 1)]] = 0


def solve(w, items_c, items_w):
    
    num_of_chromosomes = 100
    k = num_of_chromosomes // 4
    k = k // 2
    k *= 2
    num_of_items = len(items_w)
    chromosomes = []

    for i in range(num_of_chromosomes):
        chromosomes.append([random.randint(0, 1) for x in range(num_of_items)])

    fitness_results = []
    for i in range(num_of_chromosomes):
        tmp_c, tmp_w = fitness_function(chromosomes[i], items_c, items_w)
        while tmp_w > w:
            remove_random_item(chromosomes[i])
            tmp_c, tmp_w = fitness_function(chromosomes[i], items_c, items_w)
        fitness_results.append((i, tmp_c))

    fitness_results.sort(key=lambda x: x[1], reverse=True)
    fitness_sum = 0
    for x in fitness_results:
        fitness_sum += x[1]

    p = [x[0] / fitness_sum for x in fitness_results]
    chromosomes_selected = random.choices(chromosomes, weights=p, k=k)

    crossover_point = random.randint(1, num_of_items - 1) // 2
    crossover_point *= 2
    for j in range(0, k, 2):
        for i in range(crossover_point):
            chromosomes_selected[j][i], chromosomes_selected[j + 1][i] = chromosomes_selected[j + 1][i], \
                                                                         chromosomes_selected[j][i]

    for j in range(len(chromosomes_selected)):
        for i in range(len(chromosomes_selected[j])):
            if random.randint(1, 100) == 42:
                chromosomes_selected[j][i] = (chromosomes_selected[j][i] + 1) % 2

    fitness_results_selected = []
    for i in range(len(chromosomes_selected)):
        tmp_c, tmp_w = fitness_function(chromosomes_selected[i], items_c, items_w)
        while tmp_w > w:
            remove_random_item(chromosomes_selected[i])
            tmp_c, tmp_w = fitness_function(chromosomes_selected[i], items_c, items_w)
        fitness_results_selected.append((i, tmp_c))

    fitness_results_selected.sort(key=lambda x: x[1], reverse=True)

    if fitness_results_selected[0][1] > fitness_results[0][1]:
        return chromosomes_selected[fitness_results_selected[0][0]], fitness_results_selected[0][1]
    else:
        return chromosomes[fitness_results[0][0]], fitness_results[0][1]