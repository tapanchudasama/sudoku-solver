import pygame
from solver import is_valid
import time

# Colors
primary = (255,255,255)
secondary = (0,0,0)
wrong = (225,64,64)
right = (255,221,0)
black = (0, 0, 0)
lines=(9,216,121)

pygame.font.init()
sudokus = []

sudokus.append([
    [7, 8, 0, 4, 0, 0, 1, 2, 0],
    [6, 0, 0, 0, 7, 5, 0, 0, 9],
    [0, 0, 0, 6, 0, 1, 0, 7, 8],
    [0, 0, 7, 0, 4, 0, 2, 6, 0],
    [0, 0, 1, 0, 5, 0, 9, 3, 0],
    [9, 0, 4, 0, 6, 0, 0, 0, 5],
    [0, 7, 0, 3, 0, 0, 0, 1, 2],
    [1, 2, 0, 0, 0, 7, 4, 0, 0],
    [0, 4, 9, 2, 0, 6, 0, 0, 7]
])

sudokus.append([
    [0, 0, 0, 0, 0, 7, 0, 5, 0],
    [9, 5, 1, 2, 0, 0, 4, 7, 0],
    [7, 8, 0, 0, 4, 3, 1, 2, 0],
    [0, 0, 0, 0, 2, 0, 0, 0, 8],
    [8, 0, 7, 4, 6, 0, 0, 9, 5],
    [2, 4, 9, 8, 3, 0, 7, 0, 0],
    [0, 0, 4, 3, 0, 0, 6, 0, 0],
    [0, 6, 0, 1, 0, 0, 9, 0, 0],
    [3, 0, 0, 0, 0, 4, 0, 0, 2],
])


class Board():
    board = sudokus[0]

    def __init__(self, rows, cols, width, height, window):
        self.rows = rows
        self.cols = cols
        self.cubes = [[Cube(self.board[i][j], i, j, width, height)
                       for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.selected = None
        self.window = window
        self.current_state = self.board

    # Setup the sudoku board
    def draw_board(self):
        gap = self.width // 9
        # Draw lines
        for i in range(self.rows+1):
            if i % 3 == 0:
                thickness = 8
            else:
                thickness = 1
            # Draw horizontal lines
            pygame.draw.line(self.window, lines, (0, i*gap),
                             (self.width, i*gap), thickness)
            # Draw vertical lines
            pygame.draw.line(self.window, lines, (i * gap, 0),
                             (i * gap, self.height), thickness)

        # Put numbers in Cube
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw_cube(self.window)

    # Update the board with the applied changes
    def update_board(self):
        self.current_state = [
            [self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    # Returns the cube coordinates of clicked cube
    def click(self, pos):
        if(pos[0] < self.width and pos[1] < self.height):
            gap = self.width//9
            x = pos[0]//gap
            y = pos[1]//gap
            return (y, x)
        else:
            return None

    # Select the cube
    def select(self, row, col):
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False
        self.cubes[row][col].selected = True
        self.selected = (row, col)

    # Deselect the cube
    def deselect(self, row, col):
        self.cubes[row][col].selected = False
    # Set cube to 0

    def clear(self):
        i, j = self.selected
        self.cubes[i][j].set(0)
        self.update_board()
        pygame.display.update()

    def place(self, val):
        i, j = self.selected
        self.cubes[i][j].set(val)
        self.update_board()
        pygame.display.update()

    def solve_ui(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if(self.cubes[i][j].value == 0):
                    for k in range(1, 10):
                        if(is_valid(self.current_state, i, j, k)):
                            self.cubes[i][j].set(k)
                            self.update_board()
                            self.cubes[i][j].draw_number(self.window, True)
                            pygame.display.update()
                            pygame.time.delay(100)
                            if(self.solve_ui()):
                                return True
                            self.cubes[i][j].set(0)
                            self.update_board()
                            self.cubes[i][j].draw_number(self.window, False)
                            pygame.display.update()
                            pygame.time.delay(100)
                    return False
        return True

    # Display time taken to solve
    def display_time(self, start):
        font = pygame.font.SysFont("comicsans", 30)
        text = font.render("Time taken to solve:" +
                           str(time.process_time()-start), 1, secondary)
        self.window.blit(text, (20, 610))
        pygame.display.update((0, self.height, self.width, 620))

    def empty(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.current_state[i][j] = 0
                self.cubes[i][j].value = 0
                self.update_board()
        pygame.display.update()


class Cube():
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.row = row
        self.temp = 0
        self.col = col
        self.width = width
        self.height = height
        self.selected = None

    # Put numbers in sudoku
    def draw_cube(self, window):
        font = pygame.font.SysFont('comicsans', 50)
        gap = self.width//9
        x = self.col*gap
        y = self.row*gap
        text = font.render(str(self.value), 1, secondary, primary)
        window.blit(text, (x+(gap//2 - text.get_width()//2),
                           y+(gap//2 - text.get_height()//2)))
        if self.selected:
            pygame.draw.rect(window, black, (x, y, gap, gap), 4)

    # Draw each number as the UI solves the sudoku
    def draw_number(self, window, correct=True):
        font = pygame.font.SysFont('comicsans', 50)
        gap = self.width//9
        x = self.col*gap
        y = self.row*gap
        pygame.draw.rect(window, black, (x, y, gap, gap), 4)

        text = font.render(str(self.value), 1, secondary, primary)
        window.blit(text, (x+(gap//2 - text.get_width()//2),
                           y+(gap//2 - text.get_height()//2)))

        if(correct):
            pygame.draw.rect(window, right, (x, y, gap, gap), 4)
        else:
            pygame.draw.rect(window, wrong, (x, y, gap, gap), 4)

    def set(self, val):
        self.value = val

# Setup the window
def create_board(window, board):
    window.fill(primary)
    board.draw_board()


def main():
    SCREEN_WIDTH = 600
    SCREEN_HEIGHT = 650
    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.flip()
    pygame.display.set_caption('Sudoku Solver')
    board = Board(9, 9, 600, 600, window)
    running = True
    key_pressed = None
    start = 0
    flag = False
    while running:
        for event in pygame.event.get():
            if(flag == False):
                pygame.display.update()
            if(event.type == pygame.QUIT):
                running = False
            if(event.type == pygame.KEYDOWN):
                if(event.key == pygame.K_1):
                    key_pressed = 1
                    board.place(key_pressed)
                if(event.key == pygame.K_2):
                    key_pressed = 2
                    board.place(key_pressed)
                if(event.key == pygame.K_3):
                    key_pressed = 3
                    board.place(key_pressed)
                if(event.key == pygame.K_4):
                    key_pressed = 4
                    board.place(key_pressed)
                if(event.key == pygame.K_5):
                    key_pressed = 5
                    board.place(key_pressed)
                if(event.key == pygame.K_6):
                    key_pressed = 6
                    board.place(key_pressed)
                if(event.key == pygame.K_7):
                    key_pressed = 7
                    board.place(key_pressed)
                if(event.key == pygame.K_8):
                    key_pressed = 8
                    board.place(key_pressed)
                if(event.key == pygame.K_9):
                    key_pressed = 9
                    board.place(key_pressed)
                if(event.key == pygame.K_BACKSPACE):
                    board.clear()
                    key_pressed = None
                if(event.key == pygame.K_ESCAPE):
                    board.empty()
                    key_pressed = None
                if(event.key == pygame.K_SPACE):
                    start = time.process_time()
                    pygame.display.update()
                    board.solve_ui()
                    board.display_time(start)
                    key_pressed = None
                    flag = True

            if (event.type == pygame.MOUSEBUTTONDOWN):
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if (clicked):
                    if(not board.cubes[clicked[0]][clicked[1]].selected):
                        board.select(clicked[0], clicked[1])
                    else:
                        board.deselect(clicked[0], clicked[1])
            create_board(window, board)


main()
