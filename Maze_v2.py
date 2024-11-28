import pygame
import sys

# Лабиринт (0 - свободно, 1 - стена)
maze = [
    [1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 1, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 1],
    [1, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1]
]

# Константы
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 30
ROWS = len(maze)  # Количество строк в лабиринте
COLS = len(maze[0]) if maze else 0  # Количество столбцов в лабиринте

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GRAY = (50, 50, 50)
GREEN = (0, 255, 0)   # Цвет начала
RED = (255, 0, 0)     # Цвет конца

# Начальные координаты объекта
x_start_initial, y_start_initial = (1, 1)   # Начальная точка
x_end, y_end = (5, 3)                        # Конечная точка

def draw_maze(screen):
    for row in range(ROWS):
        for col in range(COLS):
            color = BLACK if maze[row][col] == 1 else WHITE
            pygame.draw.rect(screen, color,
                             (col * GRID_SIZE, row * GRID_SIZE,
                              GRID_SIZE - 1, GRID_SIZE - 1))

def draw_object(screen):
    pygame.draw.rect(screen, DARK_GRAY,
                     (x_start * GRID_SIZE + 5, y_start * GRID_SIZE + 5,
                      GRID_SIZE - 10, GRID_SIZE - 10))

def draw_start_end(screen):
    pygame.draw.rect(screen, GREEN,
                     (x_start_initial * GRID_SIZE + 5,
                      y_start_initial * GRID_SIZE + 5,
                      GRID_SIZE - 10,
                      GRID_SIZE - 10)) # Начало
    pygame.draw.rect(screen, RED,
                     (x_end * GRID_SIZE + 5,
                      y_end * GRID_SIZE + 5,
                      GRID_SIZE - 10,
                      GRID_SIZE - 10))   # Конец

def move_object(dx, dy):
    global x_start,y_start
    new_x = x_start + dx
    new_y = y_start + dy
    
    # Проверка на столкновение со стенами и границами лабиринта
    if (0 <= new_x < COLS) and (0 <= new_y < ROWS) and maze[new_y][new_x] == 0:
        x_start = new_x
        y_start = new_y

def reset_game():
    global x_start,y_start
    x_start = x_start_initial
    y_start = y_start_initial

def main():
    global x_start,y_start
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Maze Game with Start and End")
    
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    move_object(0,-1)
                elif event.key == pygame.K_DOWN:
                    move_object(0,+1)
                elif event.key == pygame.K_LEFT:
                    move_object(-1,0)
                elif event.key == pygame.K_RIGHT:
                    move_object(+1,0)
                elif event.key == pygame.K_r:   # Нажмите 'R' для перезапуска игры
                    reset_game()

        screen.fill(WHITE)
        draw_maze(screen)
        draw_start_end(screen)   # Отрисовка начала и конца
        draw_object(screen)

        # Проверка на достижение конца
        if x_start == x_end and y_start == y_end:
            font = pygame.font.Font(None, 74)
            text = font.render("You Win!", True, GREEN)
            text_rect = text.get_rect(center=(WIDTH //2 , HEIGHT //2))
            screen.blit(text,text_rect)
            pygame.display.flip()
            pygame.time.wait(2000)   # Ждем две секунды перед перезапуском игры
            reset_game()             # Сбросить игру после победы

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    reset_game()   # Инициализация начальных координат перед запуском игры
    main()
