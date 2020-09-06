import pygame
import random

WIDTH = 400
HEIGHT = 400
SQUARE = 20
XTRA = 40
FPS = 15

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTGRAY = (225, 225, 225)
DARKGRAY = (160, 160, 160)

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT+XTRA))
pygame.display.set_caption("MINESWEEPER")
clock = pygame.time.Clock()
WINNER = False

font_name = pygame.font.match_font("arial")


def draw_grid(screen, col=WHITE):
    for x in range(0, WIDTH, SQUARE):
        pygame.draw.line(screen, col, (x, XTRA), (x, HEIGHT+XTRA), 1)

    for y in range(XTRA, HEIGHT+XTRA, SQUARE):
        pygame.draw.line(screen, col, (0, y), (WIDTH, y), 1)


def draw_text(surf, text, size, x, y, color = WHITE):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def get_board(size=15):
    bombs = size * 2
    board = [[0 for i in range(size)] for j in range(size)]
    dir = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    bomb_pos = []
    for i in range(bombs):
        x, y = random.randrange(0, size), random.randrange(0, size)
        while (x, y) in bomb_pos:
            x, y = random.randrange(0, size), random.randrange(0, size)
        board[x][y] = 'B'
        bomb_pos.append((x, y))

    # print_board(board)
    bomb_pos.sort()
    # print(bomb_pos)

    score = 0
    for i in range(size):
        for j in range(size):
            no = 0
            if board[i][j] != 'B':
                for pos in range(len(dir)):
                    a = i + dir[pos][0]
                    b = j + dir[pos][1]
                    if a >= 0 and a < size and b >= 0 and b < size and board[a][b] == 'B':
                        no += 1
                board[i][j] = str(no)
                score += no

    # print_board(board)
    # print(score)
    return board, bomb_pos, score


def print_board(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            print(board[i][j], end='  ')
        print()
    print()


class Board:
    def __init__(self, screen, size=15):
        self.board, self.bomb_pos, self.total_score = get_board(size)
        self.bombs = len(self.bomb_pos)
        self.size = size
        self.screen = screen
        self.marks = []
        self.open = [[False for i in range(self.size)] for j in range(self.size)]
        self.score = 0
        
    def reset_board(self, size=15):
        self.board, self.bomb_pos, self.total_score = get_board(size)
        self.marks = []
        self.open = [[False for i in range(self.size)] for j in range(self.size)]
        self.score = 0

    def show_board(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.open[i][j]:
                    pygame.draw.rect(self.screen, DARKGRAY, ((i * SQUARE), (j * SQUARE) + XTRA, SQUARE, SQUARE))
                    pygame.draw.rect(self.screen, LIGHTGRAY, ((i * SQUARE), (j * SQUARE) + XTRA, SQUARE, SQUARE), 3)
                    if self.board[i][j] != '0' and self.board[i][j] != 'B':
                        x = (i * SQUARE) + SQUARE // 2
                        y = (j * SQUARE) + XTRA + SQUARE // 4
                        draw_text(screen, str(self.board[i][j]), 8, x, y, RED)
                elif (i, j) in self.marks:
                    pygame.draw.rect(self.screen, LIGHTGRAY, ((i * SQUARE), (j * SQUARE) + XTRA, SQUARE, SQUARE))
                    pygame.draw.rect(self.screen, DARKGRAY, ((i * SQUARE), (j * SQUARE) + XTRA, SQUARE, SQUARE), 3)
                    x = (i * SQUARE) - 1 + SQUARE // 2
                    y = (j * SQUARE) + XTRA - 1 + SQUARE // 4
                    draw_text(screen, 'M', 10, x, y, RED)
                else:
                    pygame.draw.rect(self.screen, LIGHTGRAY, ((i * SQUARE), (j * SQUARE) + XTRA, SQUARE, SQUARE))
                    pygame.draw.rect(self.screen, DARKGRAY, ((i * SQUARE), (j * SQUARE) + XTRA, SQUARE, SQUARE), 3)


    def inBound(self, a, b):
        if a >= 0 and a < self.size and b >= 0 and b < self.size:
            return True
        return False

    def open_cells(self, x, y):
        que = [(x, y)]
        dir = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        self.open[x][y] = True
        self.score += int(self.board[x][y])
        while len(que):
            x, y = que[0]
            for pos in dir:
                a, b = x + pos[0], y + pos[1]
                if self.inBound(a, b) and not self.open[a][b] and self.board[a][b] != 'B':
                    if self.board[a][b] == '0':
                        que.append((a, b))
                    self.open[a][b] = True
                    self.score += int(self.board[a][b])
            que.pop(0)


    def move(self, x, y, mark=False):
        if self.open[x][y]:
            return False
        if mark == True:
            if (x, y) in self.marks:
                self.marks.remove((x, y))
                self.bombs += 1
            elif self.bombs > 0:
                self.marks.append((x, y))
                self.bombs -= 1

        else:
            if (x, y) in self.marks:
                return False
            if self.board[x][y] == 'B':
                for pos in self.bomb_pos:
                    a = pos[0] * SQUARE + SQUARE // 2
                    b = pos[1] * SQUARE + XTRA + SQUARE // 2
                    pygame.draw.rect(self.screen, LIGHTGRAY, ((pos[0] * SQUARE) + 3, (pos[1] * SQUARE) + XTRA + 3, SQUARE - 5, SQUARE - 5))
                    pygame.draw.circle(self.screen, BLACK, (a, b), 5)
                return True
            if self.board[x][y] == '0':
                self.open_cells(x, y)
            else:
                self.open[x][y] = True
                self.score += int(self.board[x][y])

        return False



b = Board(screen, 20)
running, gameover = True, False
while running:

    if not gameover:
        screen.fill(BLACK)
        b.show_board()
        draw_grid(screen, BLACK)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_r]:
        b.reset_board()
        gameover = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not gameover and event.type == pygame.MOUSEBUTTONDOWN:
            x = (event.pos[0]) // SQUARE
            y = (event.pos[1] - XTRA) // SQUARE
            # print(x, y)
            if event.button == 1:
                gameover = b.move(x, y)
            else:
                gameover = b.move(x, y, mark=True)

    draw_text(screen, "MINES: {}".format(b.bombs), 10, 30, 10, WHITE)
    draw_text(screen, "SCORE: {}".format(b.score), 10, WIDTH - 40, 10, WHITE)

    if b.total_score == b.score:
        WINNER = True
        gameover = True

    if gameover:
        if WINNER:
            text = "YOU WIN!!"
        else:
            text = "YOU LOSE!!"
        draw_text(screen, text, 20, WIDTH//2, 10, WHITE)

    pygame.display.flip()


