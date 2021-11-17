
import pygame
import sys
import math

# RGB Values
BLUE = (0,0,255)
BLACK  = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

game_end = False # Variable which controls the while loop of the game interface.
COLUMN_COUNT = 7
ROW_COUNT = 6

# Board Setup for the game.
BOARD =[
[0,0,0,0,0,0,0],
[0,0,0,0,0,0,0],
[0,0,0,0,0,0,0],
[0,0,0,0,0,0,0],
[0,0,0,0,0,0,0],
[0,0,0,0,0,0,0]]

# Printing the board.
def print_board(board):
    print()
    for k in range(len(board)):
        print(board[k])

# Dropping the piece in vacant column.
def move(board, position, symbol):
    global BOARD
    for i in range(len(board)-1, -1, -1):
        if board[i][position] == 0:
            board[i][position] = symbol
            board = BOARD
            break

# Checking whether the column is already full or not.
def board_valid(board, position):
    for i in range(len(board)-1, -1, -1):
        if board[i][position] == 0:
            return True
            break
    else:
        return False

# Defining a function to check whether any combiantion for the win is possible or not.
def win(board):
    for i in range(len(board)):
        # Iterating over rows to determine a win.
        for j in range(4):
            if (board[i][j] == board[i][j+1] == board[i][j+2] == board[i][j+3]) == True and board[i][j] != 0:
                return True
        # Iterating over columns to determine a win.
        for j in range(3):
            if (board[j][i] == board[j+1][i] == board[j+2][i] == board[j+3][i]) == True and board[j][i] != 0:
                return True

    for i in range(3):
        # Checking for a combination in negative sloped diagonal.
        for j in range(4):
            if (board[i][j] == board[i+1][j+1] == board[i+2][j+2] == board[i+3][j+3]) == True and board[i][j] != 0:
                return True
        # Checking for a combination in positive sloped diagonal.
        for j in range(3,7):
            if (board[i][j] == board[i+1][j-1] == board[i+2][j-2] == board[i+3][j-3]) == True and board[i][j] != 0:
                return True

# Checking whether the game is tied or not.
def game_tie(board):
    temp_var = True
    for i in board:
        for j in i:
            if j == 0:
                temp_var = False
    return temp_var

# Printing the graphical board
def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            draw_position = (c*SQUARESIZE + SQUARESIZE/2, r*SQUARESIZE + SQUARESIZE + SQUARESIZE/2)
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            if board[r][c] == 0:
                pygame.draw.circle(screen, BLACK, draw_position, RADIUS)
            elif board[r][c] == 1:
                pygame.draw.circle(screen, RED, draw_position, RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, draw_position, RADIUS)
    pygame.display.update()

# Game Interface
pygame.init()
turn =  1
myfont = pygame.font.SysFont("monospace", 75)

SQUARESIZE = 100
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE
size = (width, height)
RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Connect 4")
print_board(BOARD)
draw_board(BOARD)
pygame.display.update()

while not game_end:
    # Exiting the window smoothly.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_end = True

        # Display of the circle on the above blank row before each turn when moving the mouse.
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn % 2 != 0:
                pygame.draw.circle(screen, RED, (posx, SQUARESIZE//2), RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (posx, SQUARESIZE//2), RADIUS)
        pygame.display.update()

        # Updating the board after the mouse button is pressed.
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))

            if turn % 2 == 0:
                player = 'Player 2'
                symbol = 2
            else:
                player = 'Player 1'
                symbol = 1

            posx = event.pos[0]
            player_choice = posx//SQUARESIZE

            if board_valid(BOARD, player_choice):
                move(BOARD, player_choice, symbol)
                print_board(BOARD)
                draw_board(BOARD)
                turn += 1
            else:
                print('Column Full')

            # If winning condition is satisfied update the screen, with player number.
            if win(BOARD):
                if turn % 2 != 0:
                    label = myfont.render("Player 2 wins!!", 1, YELLOW)
                else:
                    label = myfont.render("Player 1 wins!!", 1, RED)

                screen.blit(label, (20,10))
                pygame.display.update()
                pygame.time.wait(3000)
                print(f'\n{player} has won the game')
                game_end = True

            # If the game is draw, no winner even after the whole board is filled up.
            if game_tie(BOARD):
                label = myfont.render('Game Draw', 1, BLUE)
                screen.blit(label, (40,10))
                pygame.display.update()
                print('Game Draw')
                pygame.time.wait(3000)
                game_end = True


