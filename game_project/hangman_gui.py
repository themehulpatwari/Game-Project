import random
from word import word_list
import sys
import pygame
from pygame.locals import *


ROWS = 2
COLS = 13
GAP = 20
SIZE = 40
BUTTONS = []

# RGB
WHITE = (255,255,255)
BLACK = (0,0,0)

# Function to print buttons on the pygame window
def draw_btns(buttons):
    for (button, letter) in buttons:
        btn_text = btn_font.render(letter, True, BLACK)
        btn_text_rect = btn_text.get_rect(center = (button.x + SIZE//2 , button.y + SIZE//2))
        pygame.draw.rect(screen, BLACK, button, 2)
        screen.blit(btn_text, btn_text_rect)

# Function to display the Correct guessed letters on screen
def display_guess(word, guessed):
    display_word = ''
    for letter in word:
        if letter in guessed:
            display_word += f"{letter} "
        else:
            display_word += "_ "

    text = letter_font.render(display_word, True, BLACK)
    screen.blit(text, (400, 200))

# Loading the png images in a list
IMAGES = []
for i in range(7):
    image = pygame.image.load(f"Assets\\hangman{i}.png")
    IMAGES.append(image)

# Adding the letter as well as it's position in the list BUTTONS
temp_var = 0
for row in range(ROWS):
    for col in range(COLS):
        x = ((GAP * col) + GAP) + (SIZE * col) + 50
        y = ((GAP * row) + GAP) + (SIZE * row) + 350
        box = pygame.Rect(x,y,SIZE,SIZE)
        letter = chr(65 + temp_var)
        BUTTONS.append([box, letter])
        temp_var += 1

# Game Interface
pygame.init()
WIDTH, HEIGHT = (900, 700)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman")

HANGMAN_BG = pygame.transform.scale(pygame.image.load("Assets\\hangman.jpg"),(WIDTH, HEIGHT))

# Font
btn_font = pygame.font.SysFont('arial', 30)
letter_font = pygame.font.SysFont('arial', 60)
game_font = pygame.font.SysFont('arial', 80)

WORD = (random.choice(word_list)).upper()
GUESSED = []
guess = 0
game_over = False
exit_game = False

while not game_over:
    pygame.init()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_game = True
            game_over = True

        if event.type == MOUSEBUTTONDOWN:
            clicked_pos = event.pos

            for button, letter in BUTTONS:
                if button.collidepoint(clicked_pos):
                    GUESSED.append(letter)

                    if letter not in WORD:
                        guess += 1
                    if guess == 6:
                        game_over = True

                    # Removing button when it is clicked
                    BUTTONS.remove([button, letter])

    # Setting up the main screen with hangman image, buttons and guessed words
    screen.blit(HANGMAN_BG, (0,0))
    screen.blit(IMAGES[guess], (150,100))
    draw_btns(BUTTONS)
    display_guess(WORD, GUESSED)
    pygame.display.update()

    correct_guess = ''
    for i in WORD:
        if i in GUESSED:
            correct_guess += i

    if correct_guess == WORD:
        display_text = 'You Win :) !!!'
        game_over = True
    else:
        display_text = 'You Lose :('

    if game_over  and exit_game == False:
        game_over_text = game_font.render(display_text, True, BLACK)
        game_over_text_rect = game_over_text.get_rect(center = (WIDTH//2,HEIGHT//2))

        screen.blit(HANGMAN_BG, (0,0))
        screen.blit(game_over_text, game_over_text_rect)

        label = game_font.render(f"Correct Word = {WORD}", 1, BLACK)
        screen.blit(label, (40,80))
        pygame.display.update()

        pygame.time.delay(3000)

# libpng warning: iCCP: known incorrect sRGB profile
# Please ignore the above warning, it is not a problem and it will not cause any problem.
