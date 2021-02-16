import math
import random

import pygame
from pygame import mixer

# initialize pygame (must write this line every time you are using pygame)
pygame.init()

# creating the screen (width, height)
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background2.jpg')

# Background Sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Title and icon
pygame.display.set_caption("Virus Invaders")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('fighterjet64.png.')
playerX = 370
playerY = 500
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('coronavirus.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(30, 150))
    enemyX_change.append(0.4)
    enemyY_change.append(40)

# Bullet
# Ready - You can't see the bullet on the screen
# Fire - Bullet is currently moving
bulletImg = pygame.image.load('syringe64.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 1
bullet_state = "ready"

# Score/font
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# Game Over text
over_font = pygame.font.Font('freesansbold.ttf', 64)


# Show score on screen
def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (194, 19, 19))
    screen.blit(over_text, (200, 250))
    over_text = over_font.render("COVID-19 HAS INVADED", True, (194, 19, 19))
    screen.blit(over_text, (23, 320))
    over_text = over_font.render("PLANET EARTH", True, (194, 19, 19))
    screen.blit(over_text, (135, 390))


# Function to draw player image with coordinates
def player(x, y):
    # blit means to draw
    screen.blit(playerImg, (x, y))


# Function to draw enemy
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


# Function to fire bullet
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    # +16 and +10 so it appears at center of spaceship and not top left corner
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:
    # Anything that you want to occur/appear continuously while game is running has to be inside the while running loop!
    # RGB - (Red, Green, Blue), every color is made of a combination of these. Google "color to rgb"
    screen.fill((2, 45, 69))

    # Background image
    screen.blit(background, (0, 0))

    # infinite loop that makes sure the game is always running and window doesn't close down unless close
    # button is pressed. Using pygame.event.get(), it loops through every event that occurs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # If keystroke is pressed, checks whether its right or left, must be inside 'for event' loop
        # KEYDOWN: checks when a key has been pressed
        # KEYUP: checks when a key has been released
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.8
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.8
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_Sound = mixer.Sound('laser.wav')
                    bullet_Sound.play()
                    # Get the current x coordinate of spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change

    # If statement to make sure spaceship doesnt leave window. Subtract pixel size of spaceship (64) by width (800)
    # for right side
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy Movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 420:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.4
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_Sound = mixer.Sound('explosion.wav')
            explosion_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(30, 150)
        # calling enemy function to draw enemy
        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # calling player function to draw player image
    player(playerX, playerY)
    # calling show score function
    show_score(textX, textY)
    # Must use this any time you make a change to the screen so it's constantly updating the screen
    pygame.display.update()
