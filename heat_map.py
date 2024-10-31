import numpy as np
import matplotlib.pyplot as plt

# Задаем размеры региона
region_size = 15

# Генерируем случайные температуры в диапазоне [-15, 35]
temperature_data = np.random.uniform(-15, 35, (region_size, region_size))

# Создаем тепловую карту
plt.figure(figsize=(8, 6))
plt.imshow(temperature_data, cmap='hot', interpolation='nearest', vmin=-15, vmax=35)
plt.colorbar(label='Температура (°C)')  # Добавляем цветовую шкалу
plt.title('Тепловая карта температуры')
plt.xlabel('X координата')
plt.ylabel('Y координата')
plt.xticks(range(region_size))
plt.yticks(range(region_size))
plt.grid(False)  # Отключаем сетку
plt.show()
