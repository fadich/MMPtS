import numpy as np


# Вхідні дані
YEAR = 1995
DAY = 20
MONTH = 2

# Функції для кодування/декодування чисел

def int_to_bin(n, bits):
    return format(n, f'0{bits}b')


def bin_to_int(b):
    return int(b, 2)


def bin_to_gray(b):
    n = int(b, 2)
    gray = n ^ (n >> 1)
    return format(gray, f'0{len(b)}b')


def gray_to_bin(g):
    n = int(g, 2)
    mask = n
    while mask != 0:
        mask >>= 1
        n ^= mask
    return format(n, f'0{len(g)}b')


def real_to_bin(x, xmin, xmax, bits):
    N = 2 ** bits - 1
    q = round((x - xmin) / (xmax - xmin) * N)
    return format(q, f'0{bits}b')


def bin_to_real(b, xmin, xmax):
    N = 2 ** len(b) - 1
    q = int(b, 2)
    return xmin + q / N * (xmax - xmin)


# Генетичний алгоритм

def fitness(x):
    return -(x - DAY) ** 2 + MONTH


def selection(pop, fitnesses):
    idx = np.argsort(fitnesses)[-len(pop) // 2:]
    return pop[idx]


def crossover(parents, bits):
    children = []
    for i in range(len(parents) // 2):
        p1, p2 = parents[2 * i], parents[2 * i + 1]
        point = np.random.randint(1, bits)
        child1 = p1[:point] + p2[point:]
        child2 = p2[:point] + p1[point:]
        children.extend([child1, child2])
    return np.array(children)


def mutation(pop, rate=0.1):
    for i in range(len(pop)):
        if np.random.rand() < rate:
            point = np.random.randint(len(pop[i]))
            l = list(pop[i])
            l[point] = '1' if l[point] == '0' else '0'
            pop[i] = ''.join(l)
    return pop


# Діапазон пошуку [min(a,b), max(a,b)] => [2, 20]
xmin_f, xmax_f = 2, 20

# Нові параметри кодування
precision_f = 0.01
bits_f = int(np.ceil(np.log2((xmax_f - xmin_f) / precision_f + 1)))

# Параметри ГА
pop_size = 8
population = np.array(
    [format(np.random.randint(0, 2 ** bits_f), f'0{bits_f}b') for _ in range(pop_size)]
)

for gen in range(2):
    real_values = np.array([bin_to_real(ind, xmin_f, xmax_f) for ind in population])
    fitnesses = np.array([fitness(x) for x in real_values])
    print(f"\nПокоління {gen + 1}")
    print("Найкраще значення:", real_values[np.argmax(fitnesses)], "з функцією:", np.max(fitnesses))
    parents = selection(population, fitnesses)
    children = crossover(parents, bits_f)
    population = np.array([*parents, *mutation(children)])

# Підсумок
real_values = np.array([bin_to_real(ind, xmin_f, xmax_f) for ind in population])
fitnesses = np.array([fitness(x) for x in real_values])
best = real_values[np.argmax(fitnesses)]
print("\nПідсумковий результат після двох поколінь:", best, "з функцією:", np.max(fitnesses))
