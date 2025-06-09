import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

# Параметри для рівномірного розподілу
low = 4
high = 14

# Генерація 1000 псевдовипадкових чисел
data = np.random.uniform(low, high, 1000)

# Статистичні характеристики
mean = np.mean(data)
std = np.std(data)
minimum = np.min(data)
maximum = np.max(data)

print(f"Середнє значення: {mean}")
print(f"Стандартне відхилення: {std}")
print(f"Мінімальне значення: {minimum}")
print(f"Максимальне значення: {maximum}")

# Побудова гістограми
plt.hist(data, bins=20, edgecolor='black', alpha=0.7)
plt.title("Рівномірний розподіл, 1К")
plt.xlabel("Значення")
plt.ylabel("Кількість")
plt.grid()
plt.show()
