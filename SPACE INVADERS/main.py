import pygame
import random
import math
from pygame import mixer
import button
import sys

# Intialize pygame
pygame.init()

size = width, height = 800, 600

# Create a screen
screen = pygame.display.set_mode(size)

# Create Background
background = pygame.image.load("hyperspace.jpg")

# Title and Icon/Logos
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# Audio
pygame.mixer.init()
mixer.music.load("GAMEMUSIC.wav")
mixer.music.play(-1)
# Player
playerImg = pygame.image.load("SS2.png")

playerX = 370
playerY = 480
playerX_change = 0

# Enemy

# create a list for enemies
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# Bullet
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
# Ready state means you cannot see the bullet on the screen
# Fire means it is currently firing
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)

# give it x and y cordinates of where you want it
textX = 10
textY = 40

# Button images
resume_img = pygame.image.load("button_resume.png").convert_alpha()
options_img = pygame.image.load("button_options.png").convert_alpha()
quit_img = pygame.image.load("button_quit.png").convert_alpha()
quit_img2 = pygame.image.load("quitpix.png").convert_alpha()
start_img = pygame.image.load("startpix.png").convert_alpha()
on_img = pygame.image.load("ON.png").convert_alpha()
off_img = pygame.image.load("OFF.png").convert_alpha()
back_img = pygame.image.load("back.png").convert_alpha()

# Create button instances
resume_button = button.Button(300, 150, resume_img, 1)
options_button = button.Button(300, 275, options_img, 1)
quit_button = button.Button(300, 400, quit_img, 1)
quit_button2 = button.Button(300, 250, quit_img2, 1)
start_button = button.Button(300, 150, start_img, 1)
on_button = button.Button(225, 200, on_img, 1.5)
off_button = button.Button(425, 200, off_img, 1.5)
back_button = button.Button(325, 325, back_img, 1)

# Game States
menu_state = "main"
game_paused = False
start_menu = True
audio_state = False

# Game Over text
over_font = pygame.font.Font("freesansbold.ttf", 64)


def game_over_text():
    # Render text using font
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    # Blit to the screen
    screen.blit(over_text, (200, 250))


def show_score(x, y):
    # Render text using font
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    # Blit to the screen
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


# Calculates distance between bullet and the enemy and if it is below a certain threshold returns true, otherwise false.
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# def game_sound(cond):
#     # Background sound
#     if cond:


# Game Loop
running = True
playing = False
while running:
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))
    if start_menu:
        if start_button.draw(screen):
            start_menu = False
        if quit_button2.draw(screen):
            running = False

    elif game_paused:
        # Display Menu
        if menu_state == "main":
            if resume_button.draw(screen):
                game_paused = False
            if quit_button.draw(screen):
                running = False
            if options_button.draw(screen):
                menu_state = "options"
        if menu_state == "options":
            if on_button.draw(screen):
                mixer.music.unpause()
            if off_button.draw(screen):
                mixer.music.pause()
            if back_button.draw(screen):
                menu_state = "main"

    else:
        # Preventing Ship from going out of bounds
        playerX += playerX_change
        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736

        # Enemy Movement
        for i in range(num_of_enemies):
            # Game Over
            if enemyY[i] > 440:
                for j in range(num_of_enemies):
                    enemyY[j] = 2000
                game_over_text()
                break
            enemyX[i] += enemyX_change[i]
            # Left Boundary
            if enemyX[i] <= 0:
                enemyX_change[i] = 4
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = -4
                enemyY[i] += enemyY_change[i]
            # Collision
            collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                # reset bullet to starting point
                bulletY = 480
                bullet_state = "ready"
                score_value += 1
                # print(score_value)
                enemyX[i] = random.randint(0, 736)
                enemyY[i] = random.randint(50, 150)
                b_sound = mixer.Sound("explosion.wav")
                b_sound.play()
            enemy(enemyX[i], enemyY[i], i)
        # Bullet Movement
        if bulletY == 0:
            bulletY = 480
            bullet_state = "ready"

        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change
        player(playerX, playerY)
        show_score(textX, textY)

    # Loop through all the events in the game and check if button has been pressed
    # for event in pygame.event.get():
    #     if event.type == pygame.QUIT:
    #         running = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if a keystroke is pressed, check whether its a left or right arrow.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                # print("Left Arrow")
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                # print("Right Arrow")
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
                    b_sound = mixer.Sound("laser.wav")
                    b_sound.play()
            if event.key == pygame.K_TAB:
                game_paused = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                # print("Release")
                playerX_change = 0
    # Update Screen
    pygame.display.update()
