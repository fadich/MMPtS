import numpy as np


# --- Завдання 1 (оновлене) ---

# Функції для кодування/декодування цілих чисел

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


# Вхідні дані
YEAR = 1995
DAY = 20
MONTH = 2

# Параметри для цілих чисел
min_int = 0
max_int = YEAR
bits_int = int(np.ceil(np.log2(max_int - min_int + 1)))

# Демонстрація для цілого числа
n = YEAR
bincode = int_to_bin(n, bits_int)
graycode = bin_to_gray(bincode)
decoded_bin = bin_to_int(bincode)
decoded_gray = bin_to_int(gray_to_bin(graycode))

print("Ціле число:")
print("Оригінал:", n)
print("Двійковий код:", bincode)
print("Код Грея:", graycode)
print("Декодування двійкового:", decoded_bin)
print("Декодування коду Грея:", decoded_gray)

# Параметри для дійсних чисел
x_real = float(f"{MONTH}.{DAY}")  # 2.20
xmin = 0
xmax = 100  # Обираємо достатній діапазон для демонстрації
precision = 0.01
bits_real = int(np.ceil(np.log2((xmax - xmin) / precision + 1)))


# Кодування дійсного числа

def real_to_bin(x, xmin, xmax, bits):
    N = 2 ** bits - 1
    q = round((x - xmin) / (xmax - xmin) * N)
    return format(q, f'0{bits}b')


def bin_to_real(b, xmin, xmax):
    N = 2 ** len(b) - 1
    q = int(b, 2)
    return xmin + q / N * (xmax - xmin)


bincode_real = real_to_bin(x_real, xmin, xmax, bits_real)
graycode_real = bin_to_gray(bincode_real)
decoded_bin_real = bin_to_real(bincode_real, xmin, xmax)
decoded_gray_real = bin_to_real(gray_to_bin(graycode_real), xmin, xmax)

print("\nДійсне число:")
print("Оригінал:", x_real)
print("Двійковий код:", bincode_real)
print("Код Грея:", graycode_real)
print("Декодування двійкового:", decoded_bin_real)
print("Декодування коду Грея:", decoded_gray_real)
