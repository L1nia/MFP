import pygame
import sys
import heapq
import time

# Определение цветов
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)   # Начальная точка
RED = (255, 0, 0)     # Конечная точка
GRAY = (200, 200, 200) # Путь

# Лабиринт (0 - свободно, 1 - стена)
maze = [
    [1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 1, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 1],
    [1, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1]
]

# Константы
GRID_SIZE = 30
WIDTH = len(maze[0]) * GRID_SIZE
HEIGHT = len(maze) * GRID_SIZE

# Начальные и конечные координаты
start = (1, 1)
end = (5, 3)

# Положение игрока
player_pos = list(start)

def heuristic(a, b):
    """Эвристическая функция для A* (Манхэттенское расстояние)."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(maze, start, end):
    """Алгоритм A* для поиска пути."""
    open_set = []
    heapq.heappush(open_set, (0 + heuristic(start, end), start))
    
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, end)}
    
    while open_set:
        current = heapq.heappop(open_set)[1]
        
        if current == end:
            return reconstruct_path(came_from, current)
        
        for dx, dy in [(0,-1), (0,+1), (-1,0), (+1,0)]:
            neighbor = (current[0] + dx, current[1] + dy)
            
            if neighbor[0] < 0 or neighbor[0] >= len(maze[0]) or neighbor[1] < 0 or neighbor[1] >= len(maze):
                continue
            
            if maze[neighbor[1]][neighbor[0]] == 1:
                continue
            
            tentative_g_score = g_score[current] + 1
            
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, end)
                
                if neighbor not in [i[1] for i in open_set]:
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
    
    return [] # Путь не найден

def reconstruct_path(came_from, current):
    """Восстановление пути из конечной точки к начальной."""
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.append(current)
    return total_path[::-1]

def draw_maze(screen):
    """Отрисовка лабиринта."""
    for y in range(len(maze)):
        for x in range(len(maze[y])):
            color = BLACK if maze[y][x] == 1 else WHITE
            pygame.draw.rect(screen,
                             color,
                             (x * GRID_SIZE,
                              y * GRID_SIZE,
                              GRID_SIZE - 1,
                              GRID_SIZE - 1))

def draw_path(screen,path):
    """Отрисовка найденного пути."""
    for (x,y) in path:
        pygame.draw.rect(screen,
                         GRAY,
                         (x * GRID_SIZE +5,
                          y * GRID_SIZE +5,
                          GRID_SIZE -10,
                          GRID_SIZE -10))

def draw_player(screen):
    """Отрисовка игрока."""
    player_size = GRID_SIZE // 2 # Уменьшенный размер игрока
    pygame.draw.rect(screen,
                     BLACK,
                     (player_pos[0] * GRID_SIZE + (GRID_SIZE - player_size) // 2,
                      player_pos[1] * GRID_SIZE + (GRID_SIZE - player_size) // 2,
                      player_size,
                      player_size))

def move_player(dx, dy):
    """Перемещение игрока по лабиринту."""
    new_x = player_pos[0] + dx
    new_y = player_pos[1] + dy
    
    # Проверка на столкновение со стенами и границами лабиринта
    if (new_x >= 0 and new_x < len(maze[0]) and 
        new_y >= 0 and new_y < len(maze) and 
        maze[new_y][new_x] == 0):
        player_pos[0] = new_x
        player_pos[1] = new_y

def reset_game():
    """Сброс игры к начальному состоянию."""
    global player_pos
    player_pos = list(start)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH + GRID_SIZE *2 , HEIGHT + GRID_SIZE *2))
    pygame.display.set_caption("Pathfinding in Maze")
    
    clock = pygame.time.Clock()
    
    # Поиск пути
    start_time = time.time()
    path = a_star(maze,start,end)
    end_time = time.time()
    
    print(f"Path found: {path}")
    print(f"Time taken: {end_time - start_time:.4f} seconds")
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    move_player(0,-1)
                elif event.key == pygame.K_DOWN:
                    move_player(0,+1)
                elif event.key == pygame.K_LEFT:
                    move_player(-1,0)
                elif event.key == pygame.K_RIGHT:
                    move_player(+1,0)

        screen.fill(WHITE)
        draw_maze(screen)
        draw_path(screen,path)

        # Отрисовка начальной и конечной точек
        pygame.draw.rect(screen,
                         GREEN,
                         (start[0] * GRID_SIZE +5,
                          start[1] * GRID_SIZE +5,
                          GRID_SIZE -10,
                          GRID_SIZE -10))
        
        pygame.draw.rect(screen,
                         RED,
                         (end[0] * GRID_SIZE +5,
                          end[1] * GRID_SIZE +5,
                          GRID_SIZE -10,
                          GRID_SIZE -10))

        # Отрисовка игрока
        draw_player(screen)

        # Проверка достижения финиша
        if tuple(player_pos) == end:
            font = pygame.font.Font(None, 74)
            text_surface = font.render("You Win!", True, GREEN)
            text_rect = text_surface.get_rect(center=(WIDTH //2 , HEIGHT //2))
            screen.blit(text_surface,text_rect)
            pygame.display.flip()
            time.sleep(2)   # Ждем две секунды перед перезапуском игры
            reset_game()   # Сбросить игру после победы

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
