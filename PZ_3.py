from dataclasses import dataclass
from typing import List
from prettytable import PrettyTable

# Конфігурація критеріїв
TYPE_K = ["min", "max", "min"]

# Межі критеріїв
RANGES = [
    (5.0, 12.5),  # k1
    (0.8, 0.99),  # k2
    (21.2, 47.5)  # k3
]


@dataclass
class Alternative:
    i: int
    k1: float
    k2: float
    k3: float
    e1: float = 0.0
    e2: float = 0.0
    e3: float = 0.0


# Вхідні альтернативи (дані із звіту)
alternatives = [
    Alternative(1, 7.6, 0.84, 23.1),
    Alternative(2, 10.4, 0.91, 26.3),
    Alternative(3, 10.3, 0.9, 43.6),
    Alternative(16, 5.7, 0.97, 27.5),
    Alternative(17, 6.2, 0.9, 41.5),
]


# Нормалізація критеріїв (функція корисності)
def calculate_utilities(alt_list: List[Alternative]):
    for alt in alt_list:
        values = [alt.k1, alt.k2, alt.k3]
        utilities = []
        for i, (val, (low, high)) in enumerate(zip(values, RANGES)):
            if TYPE_K[i] == 'max':
                e = (val - low) / (high - low)
            else:  # min
                e = (high - val) / (high - low)
            utilities.append(round(e, 3))
        alt.e1, alt.e2, alt.e3 = utilities


# Виклик нормалізації
calculate_utilities(alternatives)

# Виведення результатів
table = PrettyTable()
table.field_names = ["i", "k1", "k2", "k3", "e1", "e2", "e3"]

for alt in alternatives:
    table.add_row([alt.i, alt.k1, alt.k2, alt.k3, alt.e1, alt.e2, alt.e3])

print(table)

# Приклад простої агрегації (як оцінка узагальненого критерію)
# За замовчуванням вага всіх критеріїв рівна
lambdas = [0.1, 0.1, 0.8]  # Наприклад: ваги визначені експертом

print("\nУзагальнені оцінки:")
best_score = -1
best_alt = None

for alt in alternatives:
    score = alt.e1 * lambdas[0] + alt.e2 * lambdas[1] + alt.e3 * lambdas[2]
    print(f"Alternative {alt.i}: Score = {round(score, 3)}")
    if score > best_score:
        best_score = score
        best_alt = alt

print(f"\nНайкраща альтернатива: {best_alt.i} з оцінкою {round(best_score, 3)}")
