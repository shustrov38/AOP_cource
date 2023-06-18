import algorithm.sim_annealing as sim_annealing
import time


def parse_file(s):
    file = open(s, "r")
    lines = file.readlines()
    m, p = map(int, lines[0].split())
    a = [[0 for x in range(p)] for y in range(m)]
    for line in range(1, len(lines)):
        for i in list(map(int, lines[line].split()))[1:]:
            a[line - 1][i - 1] = 1
    return a


def get_line_from_lists(lst, filename):
    line = ""
    for i in range(int(filename[3:])):
        for l in range(len(lst[2])):
            if i in lst[2][l]:
                line += str(l + 1) + " "
    line += "\n"
    for i in range(int(filename[:2])):
        for l in range(len(lst[1])):
            if i in lst[1][l]:
                line += str(l + 1) + " "
    return line


if __name__ == "__main__":
    for i in ["20x20", "24x40", "30x50", "30x90", "37x53"]:
        total_time = 0
        answers = []
        file = open("lab_5/sim_anealing_answers/" + i + ".sol", "w")
        for j in range(10):
            start = time.time()
            answers.append(sim_annealing.solve(parse_file("lab_5/benchmarks/" + i + ".txt")))
            total_time += time.time() - start
        print(f"FILE: {i} - TIME: {total_time/10}")
        answers = sorted(answers, key=lambda x: x[0], reverse=True)
        file.write(get_line_from_lists(answers[0], i))
