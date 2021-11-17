import pygame
import os
pygame.font.init()
pygame.mixer.init()

# RGB Color Values
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0,0)
YELLOW = (255, 255, 0)

# Required Variables for the game
FPS = 60 # Frames per second
VEL = 4  # Speed of the spaceship
BULLETS_VEL = 8 # Speed of Bullet
MAX_BULLETS = 3 # Maximum Bullets allowed

# Size Initialisation
WIDTH, HEIGHT = (900,500)
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

WINDOW = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Space Shoot')
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT) # Border in middle

# Sound
BULLET_HIT_SOUND = pygame.mixer.Sound('Assets\\shoot1.mp3')
EXPLOSION_SOUND = pygame.mixer.Sound('Assets\\explosion.mp3')

# Font
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

# Pygame Event Initialisation
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

# Loading different images and storing them in a variable
YELLOW_SPACESHIP_IMAGE = pygame.image.load("Assets\\spaceship_yellow.png")
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
RED_SPACESHIP_IMAGE = pygame.image.load("Assets\\spaceship_red.png")
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), -90)
SPACE_BG = pygame.transform.scale(pygame.image.load("Assets\\space.png"),(WIDTH, HEIGHT))

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WINDOW.blit(SPACE_BG, (0,0)) # Background
    pygame.draw.rect(WINDOW, BLACK, BORDER) # Middle Border

    # Displaying the health
    red_health_text = HEALTH_FONT.render(f'Health: {str(red_health)}', 1, WHITE)
    yellow_health_text = HEALTH_FONT.render(f'Health: {str(yellow_health)}', 1, WHITE)
    WINDOW.blit(red_health_text,( WIDTH - red_health_text.get_width() - 10, 10))
    WINDOW.blit(yellow_health_text, (10, 10))

    # Displaying spaceship
    WINDOW.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WINDOW.blit(RED_SPACESHIP, (red.x, red.y))

    # Displaying Bullets
    for bullet in red_bullets:
        pygame.draw.rect(WINDOW, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WINDOW, YELLOW, bullet)
    pygame.display.update() # Updating the screen

# Moving the yellow spaceship with keys- W,A,S,D
def yellow_handle_movement(keys_pressed, yellow):
        if keys_pressed[pygame.K_a] and yellow.x - VEL > 0: # left
            yellow.x -= VEL
        if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x: # right
            yellow.x += VEL
        if keys_pressed[pygame.K_w] and yellow.y - VEL > 0: # up
            yellow.y -= VEL
        if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15: # down
            yellow.y += VEL

# Moving the red spaceship with keys- Up, Down, Left, Right
def red_handle_movement(keys_pressed, red):
        if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width: # left
            red.x -= VEL
        if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH: # right
            red.x += VEL
        if keys_pressed[pygame.K_UP] and red.y - VEL > 0 : # up
            red.y -= VEL
        if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15: # down
            red.y += VEL

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    # Movement of bullet(rectangle)
    for bullet in yellow_bullets:
        bullet.x += BULLETS_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)


    for bullet in red_bullets:
        bullet.x -= BULLETS_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

red_bullets = []
yellow_bullets = []

red_health = 10
yellow_health = 10

clock = pygame.time.Clock()
run = True
while run:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                yellow_bullets.append(bullet)
                BULLET_HIT_SOUND.play()

            if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                red_bullets.append(bullet)
                BULLET_HIT_SOUND.play()

        if event.type == RED_HIT:
            red_health -= 1
            EXPLOSION_SOUND.play()

        if event.type == YELLOW_HIT:
            yellow_health -= 1
            EXPLOSION_SOUND.play()

    keys_pressed = pygame.key.get_pressed()
    yellow_handle_movement(keys_pressed, yellow)
    red_handle_movement(keys_pressed, red)

    handle_bullets(yellow_bullets, red_bullets, yellow, red)

    draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)

    if red_health <= 0:
        winner_text = WINNER_FONT.render('Yellow Wins!', 1, WHITE)
        WINDOW.blit(winner_text, (WIDTH//2 - winner_text.get_width()//2, HEIGHT//2 - winner_text.get_height()//2))
        pygame.display.update()
        pygame.time.delay(3000)
        run = False

    if yellow_health <= 0:
        winner_text = WINNER_FONT.render('Red Wins!', 1, WHITE)
        WINDOW.blit(winner_text, (WIDTH//2 - winner_text.get_width()//2, HEIGHT//2 - winner_text.get_height()//2))
        pygame.display.update()
        pygame.time.delay(3000)
        run = False

