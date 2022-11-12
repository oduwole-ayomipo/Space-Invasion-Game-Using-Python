import pygame
import random
import math
from pygame import mixer

# initialize Pygame
pygame.init()

# Creating the gaming window
screen_size_x = 800
screen_size_y = 600
screen = pygame.display.set_mode((screen_size_x, screen_size_y))

# Adding a background image
background_image = pygame.image.load("res/img/Space BG II.png")
background_image_x = 0
background_image_y = 0

# Background sound
mixer.music.load("res/music/background.wav")
mixer.music.play(-1 )

# Renaming the Game
pygame.display.set_caption("Space Invasion")

# Adding a Game icon
icon = pygame.image.load("res/img/Space Logo.png")
pygame.display.set_icon(icon)

# Adding the spaceship
Spaceship = pygame.image.load("res/img/Space Jet.PNG")

# Adding the bullet
Space_bullet = pygame.image.load("res/img/Space Bullet.PNG")

# Setting the initial position of the jet
spaceship_x = 370
spaceship_y = 480
spaceship_x_movement = 0

# adding multiple alien
Space_alien = []
space_alien_x = []
space_alien_y = []
space_alien_x_movement = []
space_alien_y_movement = []
num_of_space_alien = 10

for i in range(num_of_space_alien):
    # Adding the Alien
    Space_alien.append(pygame.image.load("res/img/Space Alien.PNG"))

    # Setting the initial position of the Alien
    space_alien_x.append(random.randint(10, 720))
    space_alien_y.append(random.randint(50, 170))
    space_alien_x_movement.append(0.32)
    space_alien_y_movement.append(60)

# Setting the initial position of the bullet
space_bullet_x = 0
space_bullet_y = 480
space_bullet_x_movement = 0
space_bullet_y_movement = 1.8

# In the ready state, the bullet is inactive, it cannot be seen on the screen
# In the fire state, the bullet is active, its presence is visible on the screen and it is moving
space_bullet_state = "ready"

# Displaying the score of the player on the screen
score_value = 0
font = pygame.font.Font(None, 32)

# Game over text font
gameover_font = pygame.font.Font(None, 120)

# Game over text font
continue_font = pygame.font.Font(None, 28)


# Function to display game over text
def game_over(x, y):
    game_over_text = gameover_font.render("GAME OVER!", True, (150, 0, 0))
    screen.blit(game_over_text, (x, y))


# Function to display the spaceship on the screen
def score_display(x, y):
    score = font.render("SCORE: " + str(score_value), True, (0, 0, 0))
    screen.blit(score, (x, y))


# Function to display the spaceship on the screen
def spaceship(x, y):
    screen.blit(Spaceship, (x, y))


# Function to display the Space Alien on the screen
def space_alien(x, y, i):
    screen.blit(Space_alien[i], (x, y))


# Bullet function
def space_bullet(x, y):
    global space_bullet_state
    space_bullet_state = "fired"
    screen.blit(Space_bullet, (x + 20, y + 25))


# Collision Theory
def Collision(space_alien_x, space_alien_y, space_bullet_x, space_bullet_y):
    # If the distance between the alien and bullet is  less than or equals to 25, then a collision has occured
    distance = math.sqrt(math.pow((space_alien_x - space_bullet_x), 2) + math.pow((space_alien_y - space_bullet_y), 2))
    if distance < 25:
        return True
    else:
        return False


# Running gaming window loop

is_running = True
while is_running:

    # Displaying the background image
    screen.blit(background_image, (background_image_x, background_image_y))

    for events in pygame.event.get():

        # if statement to control the close button
        if events.type == pygame.QUIT:
            is_running = False

        # Arrow key control for spaceship
        if events.type == pygame.KEYDOWN:
            if events.key == pygame.K_RIGHT:
                spaceship_x_movement = +0.5
            if events.key == pygame.K_LEFT:
                spaceship_x_movement = -0.5

            # Spacebar control for the space bullet
            if events.key == pygame.K_SPACE:
                space_bullet_sound = mixer.Sound("res/music/laser.wav")
                space_bullet_sound.play()

                # coordinate of the space bullet
                space_bullet_x = spaceship_x
                space_bullet(space_bullet_x, space_bullet_y)

        # When the arrow key is released nothing happens
        elif events.type == pygame.KEYUP:
            if events.key == pygame.K_RIGHT or events.key == pygame.K_LEFT:
                spaceship_x_movement = 0

    # Spaceshp movement logic
    spaceship_x += spaceship_x_movement

    # Adding border to the spaceship
    if spaceship_x <= 10:
        spaceship_x = 10
    elif spaceship_x >= 720:
        spaceship_x = 720

    # Space bullet movement logic
    if space_bullet_state == "fired":
        space_bullet(space_bullet_x, space_bullet_y)
        space_bullet_y -= space_bullet_y_movement

    if space_bullet_y <= 45:
        space_bullet_y = 480
        space_bullet_state = "ready"

    # Controlling the automatic movement of the alien
    for i in range(num_of_space_alien):

        # Game over
        if space_alien_y[i] > 480:
            for j in range(num_of_space_alien):
                space_alien_y[j] = 20000000
            game_over(140, 250)
            mixer.music.stop()
            gameover_sound = mixer.Sound("res/music/gameover.wav")
            gameover_sound.play()

            break

        # Space alien movement logic
        space_alien_x[i] += space_alien_x_movement[i]
        if space_alien_x[i] <= 10:
            space_alien_x_movement[i] = 0.32
            space_alien_y[i] += space_alien_y_movement[i]

        elif space_alien_x[i] >= 745:
            space_alien_x_movement[i] = -0.32
            space_alien_y[i] += space_alien_y_movement[i]

        # Check for collision
        collision = Collision(space_alien_x[i], space_alien_y[i], space_bullet_x, space_bullet_y)
        if collision:
            collision_sound = mixer.Sound("res/music/annihilation.wav")
            collision_sound.play()
            space_bullet_y = 480
            space_bullet_state = "ready"
            score_value += 5
            print(score_value)
            space_alien_x[i] = random.randint(10, 720)
            space_alien_y[i] = random.randint(50, 170)

        space_alien(space_alien_x[i], space_alien_y[i], i)

    score_display(10, 10)
    spaceship(spaceship_x, spaceship_y)
    pygame.display.update()


# Code written by ODUWOLE AYOMIPO
