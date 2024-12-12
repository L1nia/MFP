import pygame
import sys
import random

# Инициализация pygame
pygame.init()

# Размеры экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 40

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Создание экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Лабиринт")

# Класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5

    def update(self, walls):
        keys = pygame.key.get_pressed()
        new_x, new_y = self.rect.x, self.rect.y

        if keys[pygame.K_LEFT]:
            new_x -= self.speed
        if keys[pygame.K_RIGHT]:
            new_x += self.speed
        if keys[pygame.K_UP]:
            new_y -= self.speed
        if keys[pygame.K_DOWN]:
            new_y += self.speed

        # Проверка на столкновение с препятствиями
        temp_rect = self.rect.move(new_x - self.rect.x, new_y - self.rect.y)
        if not any(temp_rect.colliderect(wall.rect) for wall in walls):  # Исправлено здесь
            self.rect.x = new_x
            self.rect.y = new_y

# Класс препятствия
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Класс цели (выход из лабиринта)
class Goal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Создание лабиринта
def create_maze(width, height):
    walls = pygame.sprite.Group()
    for x in range(0, width, TILE_SIZE):
        walls.add(Wall(x, 0, RED))
        walls.add(Wall(x, height - TILE_SIZE, RED))
    for y in range(0, height, TILE_SIZE):
        walls.add(Wall(0, y, RED))
        walls.add(Wall(width - TILE_SIZE, y, RED))

    # Добавление случайных препятствий
    for _ in range(10):
        x = random.randint(1, (width // TILE_SIZE) - 2) * TILE_SIZE
        y = random.randint(1, (height // TILE_SIZE) - 2) * TILE_SIZE
        walls.add(Wall(x, y, RED))

    return walls

# Основная функция игры
def main():
    clock = pygame.time.Clock()
    walls = create_maze(SCREEN_WIDTH, SCREEN_HEIGHT)
    player = Player(TILE_SIZE, TILE_SIZE)
    goal = Goal(SCREEN_WIDTH - 2 * TILE_SIZE, SCREEN_HEIGHT - 2 * TILE_SIZE)

    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    all_sprites.add(goal)
    all_sprites.add(walls)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Обновление игрока
        player.update(walls)

        # Проверка на достижение цели
        if pygame.sprite.collide_rect(player, goal):
            print("Победа!")
            running = False

        # Отрисовка
        screen.fill(WHITE)
        all_sprites.draw(screen)
        pygame.display.flip()

        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
