import numpy as np
import matplotlib.pyplot as plt

# Вхідні параметри
sim_time_hours = 6
sim_time = sim_time_hours * 60  # хвилини
p_repeat = 0.1

# Генератори інтервалів
def arrival_time():
    return np.random.uniform(4, 14)

def service_time():
    return np.random.normal(9, 2)

# Основна симуляція
np.random.seed(42)
current_time = 0
queue = []
queue_lengths = []
wait_times = []
service_times = []
system_times = []

next_arrival = arrival_time()
next_service_end = None

while current_time < sim_time or len(queue) > 0:
    if next_service_end is None or (next_arrival <= next_service_end and next_arrival <= sim_time):
        # Прибуття заявки
        current_time = next_arrival
        queue.append(current_time)
        next_arrival += arrival_time()
        queue_lengths.append(len(queue))
    else:
        # Обслуговування заявки
        current_time = next_service_end
        start_service = queue.pop(0)
        wait = current_time - start_service
        wait_times.append(wait)
        serv_time = max(service_time(), 0)
        service_times.append(serv_time)
        system_times.append(wait + serv_time)
        if np.random.rand() < p_repeat:
            queue.insert(0, current_time)
        if queue:
            next_service_end = current_time + max(service_time(), 0)
        else:
            next_service_end = None

    if next_service_end is None and queue:
        next_service_end = current_time + max(service_time(), 0)

# Статистика
print(f"Загальна кількість обслужених заявок: {len(service_times)}")
print(f"Середня довжина черги: {np.mean(queue_lengths)}")
print(f"Максимальна довжина черги: {max(queue_lengths)}")
print(f"Середній час очікування: {np.mean(wait_times):.2f} хв")
print(f"Середній час обслуговування: {np.mean(service_times):.2f} хв")
print(f"Середній час перебування у системі: {np.mean(system_times):.2f} хв")

# Побудова графіку довжини черги
plt.plot(queue_lengths)
plt.title("Довжина черги під час моделювання")
plt.xlabel("Кількість подій")
plt.ylabel("Довжина черги")
plt.grid()
plt.show()
