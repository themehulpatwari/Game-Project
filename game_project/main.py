import pygame
from pygame.locals import *
import importlib
import sys

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600

# Setting up the screen for pygame
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Main Menu')
CONSOLE_BG = pygame.transform.scale(pygame.image.load("Assets\\console.jpg"),(SCREEN_WIDTH, SCREEN_HEIGHT))

# Font for text
font = pygame.font.SysFont('Constantia', 30)

#Color
BG = (200, 200, 200)
RED = (255, 0 ,0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

clicked = False
counter = 0

# Class which defines all the necessary fucntions for a button
class button():
    # RGB color
    button_col = (25, 190, 225)
    hover_col = (75, 225, 255)
    click_col = (50, 150, 255)
    text_col = (255, 255, 255)

    # Size of the button
    width = 180
    height = 40

    # Initialisation after/for attributing an object to the class
    def __init__(self, x, y, text):
        self.x = x
        self.y = y
        self.text = text

    # Drawing the button on screen
    def draw_button(self):
        pygame.init()
        global clicked
        action = False

        # Position of the mouse
        pos = pygame.mouse.get_pos()

        # defining the button as a rectangle for pygame
        button_rect = Rect(self.x, self.y, self.width, self.height)

        # The position of the mouse is in contact with the button
        if button_rect.collidepoint(pos):

            # If the button is pressed, change the color of button
            if pygame.mouse.get_pressed()[0] == 1:
                clicked  = True
                pygame.draw.rect(screen, self.click_col, button_rect)

            # The button is not clicked but the clicked variable is still True thus we have to change
            # that. This also ensures that for each and every action we ahve to click the mouse.
            elif pygame.mouse.get_pressed()[0] == 0 and clicked == True:
                clicked = False
                action = True

            # Button is not clicked but the mouse is hovering over it
            else:
                pygame.draw.rect(screen, self.hover_col, button_rect)
        else:
            pygame.draw.rect(screen, self.button_col, button_rect)

        # Extra design to make it look good
        pygame.draw.line(screen, WHITE, (self.x, self.y), (self.x + self.width, self.y), 2)
        pygame.draw.line(screen, WHITE, (self.x, self.y), (self.x, self.y + self.height), 2)
        pygame.draw.line(screen, BLACK, (self.x, self.y + self.height), (self.x + self.width, self.y + self.height), 2)
        pygame.draw.line(screen, BLACK, (self.x + self.width, self.y), (self.x + self.width, self.y + self.height), 2)

        # add text to the button
        text_img = font.render(self.text, True, self.text_col)
        text_len = text_img.get_width()
        screen.blit(text_img, (self.x + int(self.width / 2) - int(text_len / 2), self.y + 5))
        return action


def del_module(module_name):
    if f'{module_name}' in sys.modules:
            del sys.modules[f'{module_name}']

# Button
connect4 = button(75, 200, 'Connect 4')
quit = button(325, 200, 'Quit ?')
hangman = button(75, 350, 'Hangman')
space_shooter = button(325, 350, 'Space Shoot')

run = True


# Main Interface
while run:

    screen.blit(CONSOLE_BG, (0,0))

    if connect4.draw_button():
        import connect4_gui
        del_module('connect4_gui')
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    if quit.draw_button():
        pygame.quit()
        exit()
    if hangman.draw_button():
        import hangman_gui
        del_module('hangman_gui')
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    if space_shooter.draw_button():
        import space_shoot
        del_module('space_shoot')
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # If we quit the pygame window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Update the window
    pygame.display.update()

pygame.quit()
