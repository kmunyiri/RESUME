import pygame
import button


# Create display window
height = 500
width = 800

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Button Demo")

# Load Button Images
startImg = pygame.image.load("start3.png").convert_alpha()
exitImg = pygame.image.load("exit.png").convert_alpha()

# Load background
bg = pygame.image.load("future.jpg")

# Create button instances
start_button = button.Button(100, 125, startImg, 1)
exit_button = button.Button(450, 125, exitImg, 1)

# Game Loop
run = True
while run:
    screen.fill((0, 0, 0))
    screen.blit(bg, (0, 0))

    if start_button.draw(screen):
        print("Start")
    if exit_button.draw(screen):
        print("Exit")
        run = False
    # Event handler
    for event in pygame.event.get():
        # Quit Game
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()

pygame.quit()
