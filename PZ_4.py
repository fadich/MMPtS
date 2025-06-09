import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.linalg import expm

# Вихідні дані для варіанта 1
A = np.array(
    [
        [0.1, 0, 0],
        [0.3, 0.2, 0],
        [0.4, 0.5, -0.2]
    ]
)

print("A:")
print(A)

xi = np.array([0.1, 0.3, -0.1])
B = np.identity(3)  # для керування (припустимо одинична матриця B)
delta = np.array([0.05, 0.02, -0.03])  # приклад керуючого впливу

# Обчислюємо власні значення та власні вектори
eigvals, eigvecs = np.linalg.eig(A)

print("Власні значення:")
print(eigvals)
print("\nВласні вектори:")
print(eigvecs)

# Вибираємо початкові умови — перший власний вектор (нормалізуємо)
Z0 = eigvecs[:, 1].real
Z0 = Z0 / np.linalg.norm(Z0)
print("\nПочаткові умови Z(0):")
print(Z0)


# Метод Рунге-Кутти 4-го порядку
def runge_kutta(f, Z0, t):
    n = len(t)
    Z = np.zeros((n, len(Z0)))
    Z[0] = Z0
    for i in range(n - 1):
        h = t[i + 1] - t[i]
        k1 = h * f(t[i], Z[i])
        k2 = h * f(t[i] + h / 2, Z[i] + k1 / 2)
        k3 = h * f(t[i] + h / 2, Z[i] + k2 / 2)
        k4 = h * f(t[i] + h, Z[i] + k3)
        Z[i + 1] = Z[i] + (k1 + 2 * k2 + 2 * k3 + k4) / 6
    return Z


# Вільний рух (тільки A)
def f_free(t, Z):
    return A @ Z


# Рух з збуренням (без керування)
def f_with_disturbance(t, Z):
    return A @ Z + xi


# Рух з збуренням та керуванням
def f_with_control(t, Z):
    return A @ Z + xi + B @ delta


# Інтервал моделювання
t0, t_end = 0, 20
h = 0.1
t = np.arange(t0, t_end + h, h)

# Чисельні розв'язки
Z_free = runge_kutta(f_free, Z0, t)
Z_disturbance = runge_kutta(f_with_disturbance, Z0, t)
Z_control = runge_kutta(f_with_control, Z0, t)

# Аналітичний розв’язок для вільного руху: Z(t) = e^(At) * Z(0)
Z_analytic = np.array([expm(A * ti) @ Z0 for ti in t])

# === Таблиця значень для вільного руху (чисельний розв'язок) ===
df = pd.DataFrame(
    {
        't': t,
        'z1(t)': Z_free[:, 0],
        'z2(t)': Z_free[:, 1],
        'z3(t)': Z_free[:, 2]
    }
)
print("\nТаблиця значень чисельного розв'язку:")
print(df.head(100))  # виводимо перші 100 рядків

df = pd.DataFrame(
    {
        't': t,
        'z1(t)': Z_analytic[:, 0],
        'z2(t)': Z_analytic[:, 1],
        'z3(t)': Z_analytic[:, 2]
    }
)
print("\nТаблиця значень аналітичного розв'язку:")
print(df.head(100))  # виводимо перші 10 0рядків

# === Побудова графіків ===

# Суміщений графік чисельний vs аналітичний (вільний рух)
plt.figure(figsize=(10, 6))
for i in range(3):
    plt.plot(t, Z_free[:, i], label=f'z{i + 1}(t) чисельно')
    plt.plot(t, Z_analytic[:, i], '--', label=f'z{i + 1}(t) аналітично')
plt.title('Вільний рух: чисельний та аналітичний розв’язок')
plt.xlabel('Час t')
plt.ylabel('Координати стану')
plt.grid()
plt.legend()
plt.show()

# Рух без керування (із збуренням)
plt.figure(figsize=(10, 6))
for i in range(3):
    plt.plot(t, Z_disturbance[:, i], label=f'z{i + 1}(t)')
plt.title('Рух при збуренні (без керування)')
plt.xlabel('Час t')
plt.ylabel('Координати стану')
plt.grid()
plt.legend()
plt.show()

# Рух з керуванням
plt.figure(figsize=(10, 6))
for i in range(3):
    plt.plot(t, Z_control[:, i], label=f'z{i + 1}(t)')
plt.title('Рух з керуванням')
plt.xlabel('Час t')
plt.ylabel('Координати стану')
plt.grid()
plt.legend()
plt.show()
