import pygame, sys
from constants import *
from board import Board
from cell import Cell
from button import Button
from button import *
import os

screen = pygame.display.set_mode((WIDTH, HEIGHT))

#sets up button positions
easy_button = Button(easy_image, (162,128))
medium_button = Button(medium_image, (162, 256))
hard_button = Button(hard_image, (162, 383))
restart_button = Button(restart_image, (162, 383))
exit_button = Button(exit_image,(162, 383))
reset_button = Button(reset_image,(75,603))
small_exit_button = Button(exit_small_image,(376,603))
small_restart_button = Button(restart_small_image,(225,603))

#sets up win/loss screens
loss_screen = pygame.image.load(os.path.join('Assets', 'sudoku.png'))
win_screen = pygame.image.load(os.path.join('Assets', 'win_screen.png'))

def pressedNum(key): #takes in key events and translates the key pressed into integers
    if key == pygame.K_1:
        return 1 
    elif key == pygame.K_2:
        return 2
    elif key == pygame.K_3:
        return 3
    elif key == pygame.K_4:
        return 4
    elif key == pygame.K_5:
        return 5
    elif key == pygame.K_6:
        return 6
    elif key == pygame.K_7:
        return 7
    elif key == pygame.K_8:
        return 8
    elif key == pygame.K_9:
        return 9

row = 0
col = 0
guess = 0
selected = [None, None]
original_board = ''

def arrowKey(key, row, col, selected): #used for arrow key movement
    if row == None and col == None:
        row, col = 0, 0
    if selected[0] == None:
        selected = [0, 0]
        return (row, col)
    if selected[1] == None:
        selected = [0, 0]
        return (row, col)
    if key == pygame.K_UP:
        if(row > 0):
            row -= 1
        return (row, col)
    elif key == pygame.K_DOWN:
        if(row < 8):
            row += 1
        return (row, col)
    elif key == pygame.K_LEFT:
        if(col > 0):
            col -= 1
        return (row, col)
    elif key == pygame.K_RIGHT:
        if(col < 8):
            col += 1
        return (row, col)
    else:
        return (row, col)

menu = True
game = True
endgame = False

while True:
    #shows user menu and allows them to select a difficulty
    while menu == True:
        screen.blit(background, (0, 0))
        screen.blit(easy_button.image, easy_button.rect)
        screen.blit(medium_button.image, medium_button.rect)
        screen.blit(hard_button.image, hard_button.rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if easy_button.rect.collidepoint(event.pos):
                    board = Board(WIDTH, HEIGHT, screen, 'easy')
                    game = True
                    menu = False
                if medium_button.rect.collidepoint(event.pos):
                    board = Board(WIDTH, HEIGHT, screen, 'medium')
                    game = True
                    menu = False
                if hard_button.rect.collidepoint(event.pos):
                    board = Board(WIDTH, HEIGHT, screen, 'hard')
                    game = True
                    menu = False

        pygame.display.update()

    while game == True:
        board.draw()
        screen.blit(small_exit_button.image, small_exit_button.rect)
        screen.blit(small_restart_button.image, small_restart_button.rect)
        screen.blit(reset_button.image, reset_button.rect)

        try:
            cell = Cell(board.userBoard[row][col], selected[0], selected[1], screen)
            cell.highlight()
        except TypeError or IndexError:
            pass

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN: #allows arrow key movement
                row, col = arrowKey(event.key, row, col, selected)
                selected = row , col
            if event.type == pygame.MOUSEBUTTONDOWN: #allows mouse movement
                x, y = event.pos
                row = int(y // (SQUARE_SIZE / 3))
                col = int(x // (SQUARE_SIZE / 3))
                print(row,col)
                selected = (row, col)
            if board.select(row, col) == True:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE: #if user presses backspace/delete in a sketch
                        if board.userBoard[selected[0]][selected[1]] == 0:
                            for sketches in board.sketchedNums:
                                if sketches.row == selected[0] and sketches.col == selected[1]:
                                    sketches.value = 0
                        else:
                            pass
                    if pressedNum(event.key) != None:
                        guess = pressedNum(event.key)
                        print(guess)
                        if board.userBoard[row][col] == 0: #if that cell isnt filled
                            if len(board.sketchedNums) >= 1: #checks for a number already sketched
                                for sketches in board.sketchedNums:
                                    if sketches.value != 0:
                                        if sketches.row == row and sketches.col == col:
                                            board.sketchedNums.remove(sketches) #removes the already sketched num
                                        sketches.value == guess #replaces with new sketch
                            else:
                                pass #lets you sketch in an empty box                        
                            board.sketch(row, col, guess)
                        else:
                            continue
                    #solidifies sketches    
                    if event.key == pygame.K_RETURN:
                        if len(board.sketchedNums) >= 0:
                            for sketches in board.sketchedNums:
                                if board.userBoard[sketches.row][sketches.col] == 0:
                                    board.userBoard[sketches.row][sketches.col] = sketches.value
                        board.sketchedNums = []        
            # created new var to avoid infinite loop in end game
            if board.select(row, col) == False and event.type == pygame.MOUSEBUTTONDOWN:
                    row = None
                    col = None
                    if small_exit_button.rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
                    if small_restart_button.rect.collidepoint(event.pos):
                        menu = True
                        game = False
                    if reset_button.rect.collidepoint(event.pos):
                        for i in range(len(board.changedNums)):
                            # gets the number of cell objects in board.changedNums
                            # then, gets the row and column for each item i in list changedNums
                            # changes the respective row and col in board.userBoard back to 0
                            board.userBoard[board.changedNums[i].row][board.changedNums[i].col] = 0   


            full = board.is_full()
            if full == True: #if the board is full check if user won/lost
                if board.check_board() == True:
                    #run win screen
                    print('win')
                    # win var is used for endgame conditions
                    win = True
                    screen.blit(win_screen, (0, 0))
                    screen.blit(exit_button.image, restart_button.rect)
                    endgame = True
                    game = False
                else:
                    #run loss screen
                    print('loss')
                    win = False
                    screen.blit(loss_screen, (0,0))
                    screen.blit(restart_button.image, restart_button.rect)
                    endgame = True
                    game = False    
        pygame.display.update()

    while endgame:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # since the buttons are in the same place I added the additional check for the win
            elif event.type == pygame.MOUSEBUTTONDOWN and not win:
                if restart_button.rect.collidepoint(event.pos):
                    menu = True
                    game = True
                    endgame = False
            elif event.type == pygame.MOUSEBUTTONDOWN and win:
                if exit_button.rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
