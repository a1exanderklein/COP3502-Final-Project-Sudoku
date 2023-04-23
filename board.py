import pygame, sys
from constants import *
from sudoku_generator import SudokuGenerator
from cell import Cell

pygame.init()
pygame.display.set_caption("Sudoku")

font = pygame.font.Font(None, 40)

class Board:
    solutionBoard = None #Winning Board
    userBoard = None #Board shown/edited by player
    blankBoard = None # used to reset the board
    def __init__(self, width, height, screen, difficulty):
        self.empty = []
        self.sketchedNums = [] #adding cell objects of sketches into a list
        self.changedNums = [] # a list of Cell objects that will be used for the reset function
        self.width = width
        self.height = height
        self.screen = screen
        self.difficulty = difficulty
        if self.difficulty == 'easy':
            self.sudoku = SudokuGenerator(9, 30)
            pass
        elif self.difficulty == 'medium':
            self.sudoku = SudokuGenerator(9, 40)
            pass
        elif self.difficulty == 'hard':
            self.sudoku = SudokuGenerator(9, 50)
            pass
        self.sudoku.fill_values()
        self.sudoku.get_board()
        self.solutionBoard = self.sudoku.print_board() #initializes solution board
        self.sudoku.remove_cells()
        self.userBoard = self.sudoku.get_board() #initializes user board
    #draws outline of grid
    def draw(self): 
        self.screen.fill(BG_COLOR)
        #draws bold horizontal lines for main 3x3 sections
        for i in range(1, BOARD_ROWS):
            pygame.draw.line(self.screen,
                            LINE_COLOR,
                            (0, i * SQUARE_SIZE),
                            (WIDTH, i * SQUARE_SIZE),
                            LINE_WIDTH)
        #draws bold vertical lines for main 3x3 sections
        for i in range(1, BOARD_COLS):
            pygame.draw.line(self.screen,
                            LINE_COLOR,
                            (i * SQUARE_SIZE, 0),
                            (SQUARE_SIZE * i, 600),
                            LINE_WIDTH)
        #draws mini horizontal lines in between 3x3 sections
        for i in range(1, SMALL_BOARD_ROWS):
            pygame.draw.line(self.screen,
                            LINE_COLOR,
                            (0, i * (SQUARE_SIZE / 3)),
                            (WIDTH, i * (SQUARE_SIZE / 3)),
                            SMALL_LINE_WIDTH)
        #draws mini vertical lines in between 3x3 sections
        for i in range(1, SMALL_BOARD_COLS):
            pygame.draw.line(self.screen,
                            LINE_COLOR,
                            (i * (SQUARE_SIZE / 3), 0),
                            ((SQUARE_SIZE / 3) * i, 600),
                            SMALL_LINE_WIDTH)
        #finds empty cells and draws them
        for i in range(9):
            for j in range(9):
                if self.userBoard[i][j] == 0:
                    emptyCell = [i, j]
                    self.empty.append(emptyCell)
                cell = Cell(self.userBoard[i][j], i, j, self.screen)
                cell.draw()
        #sketches numbers into the board
        for num in self.sketchedNums:
            num.sketch_draw() #uses cell class method

    def select(self, row, col): #ensures click is on the board
        if row != None and col != None and row <= 8 and col <= 8:
            return True
        else:
            return False
    def clear(self, cell):
        if cell in self.sketchedNums:
            cell.value = 0
    def sketch(self, row, col, value):
        sketch = Cell(value, row, col, self.screen)
        self.sketchedNums.append(sketch) #adds sketched number to list for later use
        self.changedNums.append(sketch) # so we know the locations of the changed values
    def place_number(self, row, col, value):
        if self.sudoku.board[row][col] == 0:
            self.sudoku.board[row][col] == value
        else:
            return None
    def reset_to_original(self):
        for i in self.sketchedNums:
            i.value = 0
    def is_full(self):
        for i in range(9):
            for j in range(9):
                if self.sudoku.board[i][j] == 0:
                    return False
                else:
                    continue
        return True
    def update_board(self):
        pass
    def find_empty(self):
        pass
    def check_board(self): #checks if the values match in the userBoard & solutionBoard
        for i in range(9):
            for j in range(9):
                if self.userBoard[i][j] != self.solutionBoard[i][j]:
                    return False
        return True