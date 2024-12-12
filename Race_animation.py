import pygame
import sys
import math
import random

# Инициализация pygame
pygame.init()

# Размеры экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Создание экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Гонка по кругу")

# Параметры кругового маршрута
CENTER_X = SCREEN_WIDTH // 2
CENTER_Y = SCREEN_HEIGHT // 2
RADIUS = 200

# Класс персонажа
class Character(pygame.sprite.Sprite):
    def __init__(self, color, speed, angle_offset):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.speed = speed
        self.angle = angle_offset
        self.completed_laps = 0
        self.update_position()

    def update_position(self):
        # Расчет координат на основе угла и радиуса
        x = CENTER_X + RADIUS * math.cos(math.radians(self.angle))
        y = CENTER_Y + RADIUS * math.sin(math.radians(self.angle))
        self.rect.center = (x, y)

    def update(self):
        # Изменение угла для движения по кругу
        self.angle += self.speed
        if self.angle >= 360:
            self.angle -= 360
            self.completed_laps += 1
        self.update_position()

# Функция для создания персонажей
def create_characters(num_characters):
    characters = pygame.sprite.Group()
    for i in range(num_characters):
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        speed = random.uniform(1, 3)  # Случайная скорость
        angle_offset = random.uniform(0, 360)  # Случайное начальное положение
        character = Character(color, speed, angle_offset)
        characters.add(character)
    return characters

# Основная функция игры
def main():
    clock = pygame.time.Clock()
    characters = create_characters(5)  # Создаем 5 персонажей

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Обновление персонажей
        characters.update()

        # Отрисовка
        screen.fill(WHITE)
        pygame.draw.circle(screen, BLACK, (CENTER_X, CENTER_Y), RADIUS, 2)  # Круговой маршрут
        characters.draw(screen)

        # Отображение лидера
        leader = max(characters, key=lambda c: c.completed_laps)
        font = pygame.font.Font(None, 36)
        leader_text = font.render(f"Лидер: {leader.completed_laps} кругов", True, RED)
        screen.blit(leader_text, (10, 10))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
