import random
import pygame
import button
import time

pygame.init()

size = width, height = 500, 300

# Create a screen
screen = pygame.display.set_mode(size)

# Create Background
# background = pygame.image.load("BK.jpeg")

# Load objects/options
rock = pygame.image.load("rocknew.png")
paper = pygame.image.load("papernew.png")
cut = pygame.image.load("cutnew.png")
cut = pygame.transform.rotate(cut, 90)

rps = pygame.image.load("RPS.png")
rps = pygame.transform.scale(rps, (250, 150))
# Create button instances
rock_b = button.Button(25, 75, rock, 0.05)
paper_b = button.Button(200, 75, paper, 0.25)
cut_b = button.Button(350, 75, cut, 0.06)
# rps_b = button.Button(125, 90, rps, 1)

# Surface
surface = pygame.display.get_surface()

# Font
font = pygame.font.Font('freesansbold.ttf', 32)
welcome_font = pygame.font.Font('freesansbold.ttf', 20)
chose_font = pygame.font.Font('freesansbold.ttf', 20)
end_font = pygame.font.Font('freesansbold.ttf', 20)
click_font = pygame.font.Font('freesansbold.ttf', 20)

# Definitions
game = ['R', 'P', 'S']
winner = 0
w = 0
lost = 0
t = 0
state = "start"
start_key = 0
score = 0
num_games = 3


def print_score(x, y):
    print("The current score is ", x, " to ", y, ".")


# Intialize random number generator with system time
random.seed()

# Game Loop
running = True
while running:
    screen.fill((139, 125, 107))
    # screen.blit(background, (0, 0))

    # Randomly choose a option for the computer
    user_choice = ""
    comp_choice = random.choice(game)

    if state == "start":
        welcome = welcome_font.render("Welcome to the Rock, Paper, Scissors game", True, (255, 255, 255))
        screen.blit(welcome, (30, 35))
        click = click_font.render("Click anywhere when you are ready", True, (255, 255, 255))
        screen.blit(click, (50, 260))
        screen.blit(rps, (125, 100))

        if start_key:
            state = "main"

    if state == "end":
        end = end_font.render("You won: " + str(w) + " times", True, (255, 255, 255))
        screen.blit(end, (30, 35))
        end = end_font.render("You lost: " + str(lost) + " times", True, (255, 255, 255))
        screen.blit(end, (30, 70))
        end = end_font.render("You tied: " + str(t) + " times", True, (255, 255, 255))
        screen.blit(end, (30, 105))
        if w < lost:
            end = end_font.render("SHAME ON YOU", True, (255, 255, 255))
            screen.blit(end, (30, 175))

        end = end_font.render("Thank you for playing", True, (255, 255, 255))
        screen.blit(end, (30, 140))
    if state == "main":
        # welcome = welcome_font.render("Welcome to the Rock, Paper, Scissors game", True, (255, 255, 255))
        chose = chose_font.render("Choose Rock, Paper, or Scissors", True, (255, 255, 255))
        # screen.blit(welcome, (30, 35))
        screen.blit(chose, (100, 250))
        if rock_b.draw(screen):
            user_choice = "R"
        if paper_b.draw(screen):
            user_choice = "P"
        if cut_b.draw(screen):
            user_choice = "S"

        if score == num_games:
            state = "end"

        if user_choice == 'R':
            if comp_choice == 'P':
                print('The you chose ' + user_choice)
                print('The computer chose ' + comp_choice)
                print("You lost to a machine!")
                lost += 1
                score += 1
                user_choice = ""
                print_score(w, lost)
            elif comp_choice == 'S':
                print('The you chose ' + user_choice)
                print('The computer chose ' + comp_choice)
                print("You won!")
                w += 1
                score += 1
                print_score(w, lost)
        if user_choice == 'P':
            if comp_choice == 'S':
                print('The you chose ' + user_choice)
                print('The computer chose ' + comp_choice)
                print("You lost to a machine!")
                lost += 1
                score += 1
                print_score(w, lost)
            elif comp_choice == 'R':
                print('The you chose ' + user_choice)
                print('The computer chose ' + comp_choice)
                print("You won!")
                w += 1
                score += 1
                print_score(w, lost)

        if user_choice == 'S':
            if comp_choice == 'R':
                print('The you chose ' + user_choice)
                print('The computer chose ' + comp_choice)
                print("You lost to a machine!")
                lost += 1
                score += 1
                # print_score(w, lost)
            elif comp_choice == 'P':
                print('The you chose ' + user_choice)
                print('The computer chose ' + comp_choice)
                print("You won!")
                w += 1
                score += 1
                print_score(w, lost)
        elif user_choice == comp_choice:
            print('The you chose ' + user_choice)
            print('The computer chose ' + comp_choice)
            print("Try again!")
            t += 1
            print_score(w, lost)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            start_key = 1

    pygame.display.update()
