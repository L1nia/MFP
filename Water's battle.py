import pygame
import random
import sys

# Константы
WIDTH, HEIGHT = 700, 700
GRID_SIZE = 7
CELL_SIZE = WIDTH // GRID_SIZE
FPS = 30

# Цвета
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

class BattleshipGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Морской бой")
        self.clock = pygame.time.Clock()
        self.player1_board = [['~'] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.player2_board = [['~'] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.current_player = "Player1"
        self.ships_to_place = [1] * 2 + [2] * 1 + [3] * 1 # Два корабля по 1 клетке, один по 2 клетки и один по 3 клетки
        self.score1 = 0
        self.score2 = 0
        self.game_over = False
        
    def place_ships(self, board):
        for ship in self.ships_to_place:
            placed = False
            while not placed:
                orientation = random.choice(['H', 'V']) 
                row = random.randint(0, GRID_SIZE - 1)
                col = random.randint(0, GRID_SIZE - 1)

                if orientation == 'H':
                    if col + ship <= GRID_SIZE and all(board[row][col + i] == '~' for i in range(ship)):
                        for i in range(ship):
                            board[row][col + i] = 'S'
                        placed = True

                elif orientation == 'V':
                    if row + ship <= GRID_SIZE and all(board[row + i][col] == '~' for i in range(ship)):
                        for i in range(ship):
                            board[row + i][col] = 'S'
                        placed = True

    def draw_board(self, board):
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                color = WHITE
                if board[row][col] == 'S':
                    color = BLUE
                elif board[row][col] == 'X':
                    color = RED
                elif board[row][col] == 'O':
                    color = GREEN
                
                pygame.draw.rect(self.screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(self.screen, BLACK, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

    def handle_click(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        col = mouse_x // CELL_SIZE
        row = mouse_y // CELL_SIZE
        
        if self.current_player == "Player1":
            if self.player2_board[row][col] == 'S':
                self.player2_board[row][col] = 'X'  
                self.score1 += 10 
            else:
                self.player2_board[row][col] = 'O'  

            if all(cell != 'S' for row in self.player2_board for cell in row):
                self.game_over = True
            
            # Переключаем игрока
            self.current_player = "Player2"
        
        elif self.current_player == "Player2":
            if self.player1_board[row][col] == 'S':
                self.player1_board[row][col] = 'X'  
                self.score2 += 10 
            else:
                self.player1_board[row][col] = 'O'  

            if all(cell != 'S' for row in self.player1_board for cell in row):
                self.game_over = True
            
            # Переключаем игрока обратно
            self.current_player = "Player1"

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                    self.handle_click()

            # Отрисовка экранов
            self.screen.fill(WHITE)
            if self.current_player == "Player1":
                self.draw_board(self.player2_board)  
            elif self.current_player == "Player2":
                self.draw_board(self.player1_board)  

            # Проверка на окончание игры
            if self.game_over:
                font = pygame.font.Font(None, 74)
                text_surface = font.render("Игра Окончена!", True, (255, 0, 0))
                text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
                
                score_surface_1 = font.render(f"Очки Игрока 1: {self.score1}", True, (255, 0, 0))
                score_rect_1 = score_surface_1.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                
                score_surface_2 = font.render(f"Очки Игрока 2: {self.score2}", True, (255, 0, 0))
                score_rect_2 = score_surface_2.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
                
                self.screen.blit(text_surface, text_rect)
                self.screen.blit(score_surface_1, score_rect_1)
                self.screen.blit(score_surface_2, score_rect_2)

            pygame.display.flip()
            self.clock.tick(FPS)

def main():
    game_instance = BattleshipGame()

    # Даем время на расстановку кораблей игрока 1
    print("Игроку 1 дайте время на расстановку кораблей.")
    game_instance.place_ships(game_instance.player1_board)

    # Даем время на расстановку кораблей игрока 2
    print("Игроку 2 дайте время на расстановку кораблей.")
    game_instance.place_ships(game_instance.player2_board)

    # Начинаем игру между двумя игроками
    game_instance.run()

if __name__ == "__main__":
    main()
