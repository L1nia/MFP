import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Количество частиц
num_particles = 15

# Начальные координаты (центр)
initial_positions = np.zeros((num_particles, 2))

# Генерация случайных скоростей для частиц
# Скорости уменьшаются с увеличением номера частицы
speeds = np.linspace(1.0, 0.1, num_particles)

# Угол для каждой частицы (равномерно распределенные)
angles = np.linspace(0, 2 * np.pi, num_particles, endpoint=False)

# Начальные скорости в векторной форме
velocities = np.array([[speed * np.cos(angle), speed * np.sin(angle)] for speed, angle in zip(speeds, angles)])

# Инициализация позиций частиц
positions = initial_positions.copy()

# Настройка графика
fig, ax = plt.subplots()
scat = ax.scatter(positions[:, 0], positions[:, 1], s=100)

ax.set_xlim(-5, 5)
ax.set_ylim(-5, 5)
ax.set_aspect('equal')
ax.set_title('Анимация расхождения частиц')

# Функция обновления для анимации
def update(frame):
    global positions
    positions += velocities * 0.1  # Увеличиваем позиции на основе скоростей
    scat.set_offsets(positions)     # Обновляем позиции частиц на графике
    return scat,

# Создание анимации
ani = animation.FuncAnimation(fig, update, frames=100, interval=50)

plt.show()
