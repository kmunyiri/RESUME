import sys, pygame
import button

pygame.init()

size = width, height = 1500, 1000
speed = [2, 2]
black = 0, 0, 0

screen = pygame.display.set_mode(size)

ball = pygame.image.load("antand2.png")
ball = pygame.transform.scale(ball, (64, 64))

# Define font
font = pygame.font.SysFont("arialblack", 120)

# Define colors
textcol = (255, 255, 255)

# Button images
resume_img = pygame.image.load("button_resume.png").convert_alpha()
options_img = pygame.image.load("button_options.png").convert_alpha()
quit_img = pygame.image.load("button_quit.png").convert_alpha()

# Create button instances
resume_button = button.Button(575, 125, resume_img, 2)
options_button = button.Button(575, 375, options_img, 2)
quit_button = button.Button(575, 625, quit_img, 2)

# Background
bg = pygame.image.load("future.jpg")

# Game Variabeles
game_paused = False


def draw_text(text, font, col, x, y):
    img = font.render(text, True, col)
    screen.blit(img, (x, y))


# def play():
#
# def options():

def main_menu():
    pygame.display.set_caption("Menu")
    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(bg, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        pygame.display.update()


# ball = pygame.image.load(picture)
ballrect = ball.get_rect()

# Game Loop
run = True
while run:
    screen.fill((0, 0, 0))
    # main_menu()
    if game_paused:
        # Display Menu
        if resume_button.draw(screen):
            game_paused = False
        if quit_button.draw(screen):
            run = False
        if options_button.draw(screen):
            draw_text("NO", font, textcol, 50, 350)
    # Run the game
    else:

        # draw_text("HIT SPACE TO PAUSE", font, textcol, 50, 350)
        ballrect = ballrect.move(speed)
        if ballrect.left < 0 or ballrect.right > width:
            speed[0] = -speed[0]
        if ballrect.top < 0 or ballrect.bottom > height:
            speed[1] = -speed[1]
        screen.blit(ball, ballrect)
        pygame.display.flip()
    # event handler
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            game_paused = True
            # print("Pause")
        if event.type == pygame.QUIT:
            run = False
            sys.exit()



    # screen.fill(black)

    pygame.display.update()
